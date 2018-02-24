from __future__ import unicode_literals

from django.db import models

from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.hashers import make_password,check_password
from oauth2_provider.models import Application,AccessToken,RefreshToken
import datetime
from dateutil import relativedelta as rdelta
from dateutil.relativedelta import relativedelta


# Create your models here.

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

	def _create_user(self, mobile_number, password,
					 is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		now = timezone.now()
		if not mobile_number:
			raise ValueError('The given email must be set')
		mobile_number = self.normalize_email(mobile_number)
		user = self.model(mobile_number=mobile_number,
						  is_staff=is_staff, is_active=True,
						  is_superuser=is_superuser, last_login=now,
						  date_joined=now, **extra_fields)		
		#password = mobile_number + self.aadhar_number[-4:]
		#user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, mobile_number, password=None, **extra_fields):
		return self._create_user(mobile_number, password, False, False,
								 **extra_fields)

	def create_superuser(self, mobile_number, password, **extra_fields):
		return self._create_user(mobile_number, password, True, True,
								 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	"""
		User Model Contains All Registered Users along with Aaadhar Numbers.
		Here,Mobile Number And Aaadhar Number Should be unique.
	"""
	mobile_number = models.BigIntegerField(unique=True)
	aadhar_number = models.CharField(max_length=45,unique=True)	
	name = models.CharField(max_length=100, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	
	is_staff = models.BooleanField(_('staff status'), default=False,
		help_text=_('Designates whether the user can log into this admin '
					'site.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('Designates whether this user should be treated as '
					'active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	last_modified = models.DateTimeField(auto_now=True)
	device_information = models.TextField(blank=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'mobile_number'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def __unicode__(self):
		return u'%s' % (str(self.mobile_number))

	def __str__(self):
		return str(self.mobile_number)

	def get_absolute_url(self):
		return "/users/%s/" % urlquote(self.mobile_number)

	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"Returns the short name for the user."
		return self.first_name



def updateClientDetails(sender, instance, **kwargs):
	if kwargs.get('created',None) == True:
		aadhar_number = instance.aadhar_number
		password = str(instance.mobile_number) + aadhar_number[-4:]
		instance.set_password(password)
		instance.save()
		if Application.objects.filter(user=instance.id).exists():
			pass
		else:
			Application.objects.create(user=instance, client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type=Application.GRANT_PASSWORD)
	pass

post_save.connect(updateClientDetails, sender=User)


class Userleaders(models.Model):
	"""
		This Model Descrobes,User's Leader information.
	"""	
	user = models.ForeignKey(User,related_name='user_related_to_user')
	leader = models.ForeignKey(User,related_name='user_related_to_leader')
	create_date = models.DateTimeField(auto_now=True)
	last_modified = models.DateTimeField(auto_now=True)
	


class People(models.Model):
	"""
		This Model Describes,User's Contacts.
		From These Contacts ,User will Create a Group along with members
	"""
	offline_id = models.BigIntegerField(default=0)
	mobile_number = models.BigIntegerField()
	aadhar_number = models.CharField(max_length=150, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	latitude = models.FloatField(default=0.0)
	longitude = models.FloatField(default=0.0)
	house_number = models.CharField(max_length=20, blank=True, null=True)
	village = models.CharField(max_length=100, blank=True, null=True)
	sub_district_or_mandal = models.CharField(max_length=100, blank=True, null=True)
	district = models.CharField(max_length=100, blank=True, null=True)
	city_name = models.CharField(max_length=100, blank=True, null=True)
	state_name = models.CharField(max_length=100, blank=True, null=True)
	country_name = models.CharField(max_length=100, blank=True, null=True)
	pincode = models.IntegerField(blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=False,default=timezone.now)
	last_modified = models.DateTimeField(auto_now=True)    
	is_synced = models.BooleanField(default=True)
	create_by = models.ForeignKey(User,related_name='created_user_reference')
	modified_by = models.ForeignKey(User,related_name='modified_by_user_reference')

	def __str__(self):
		return str(self.mobile_number)


class FormsInformation(models.Model):
	"""
		Here,Super Admin Save Forms Information.
		These Forms are displayed in mobile App

	"""
	title = models.CharField(max_length=250)
	create_by = models.ForeignKey(User,db_column='create_by')
	create_date = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class FormKeysInformation(models.Model):
	"""
		Here,we are saving only keys which are entered by user.
		Here we are avoiding duplicate values.......		
	"""
	form = 	models.ForeignKey(FormsInformation,related_name='forms_keys')
	key = models.CharField(max_length=250)	
	create_date = models.DateTimeField(auto_now_add=True)	
	create_by = models.ForeignKey(User,db_column='create_by')
	last_modified = models.DateTimeField(auto_now=True)

	# class Meta:
	# 	verbose_name = _('Other Information')
	# 	verbose_name_plural = _('Other Information')


class PeopleKeysDetails(models.Model):
	"""
		This Model Describes,Other information of People(Contact)
		Other Than People Model Information,we can Save Extra Data Here..
		Like Alternate Address or extra Mobile Numbers....
		Here,we are saving Key pair Information
	"""
	offline_id = models.BigIntegerField(default=0)
	form = 	models.ForeignKey(FormsInformation,related_name='people_forms_keys',on_delete=models.CASCADE)
	value = models.TextField(blank=True)
	people = models.ForeignKey(People,on_delete=models.CASCADE)
	create_by = models.ForeignKey(User,db_column='create_by')
	create_date = models.DateTimeField(auto_now_add=True)	
	last_modified = models.DateTimeField(auto_now=True)


class UserPeople(models.Model):
	"""
		This Model Contains Relation with people model and user model.
		people contacts having by multiple users.avoiding duplication of information of people details we are maintaing here.
	"""
	offline_id = models.BigIntegerField(default=0)
	nick_name = models.CharField(max_length=150)
	user = models.ForeignKey(User,related_name='User_people_id')
	people = models.ForeignKey(People,related_name='people_user_reference',on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u'%s' % (self.mobile_number)



class Otpverification(models.Model):
	"""
		This Model Describes,USERS OTP Verification Details.s
	"""
	mobile_number = models.BigIntegerField()
	otp_number = models.CharField(max_length=100)
	is_verified = models.BooleanField(default=False)
	create_date = models.DateField(auto_now_add=False,default=datetime.date.today)
	expired_date = models.DateField()

class ActionLog(models.Model):
	"""
		This Model is Used To MainTain a Log For Every Action .
		which contains action url and method along with user details and also location.
	"""
	device_id = models.TextField()
	model = models.CharField(max_length=250)
	index_id = models.IntegerField()
	create_by = models.ForeignKey(User,related_name='log_user_reference')
	action_url = models.CharField(max_length=250)
	action_method = models.CharField(max_length=100)
	created_date = models.DateField(auto_now_add=False,default=datetime.date.today)
	last_modified = models.DateTimeField(auto_now=True)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)

