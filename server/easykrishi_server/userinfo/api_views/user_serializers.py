from rest_framework import serializers
from django.db import transaction, models
from django.conf import settings
from userinfo.models import *
from groups.models import *
import pdb
from oauth2_provider.models import Application,AccessToken,RefreshToken
import datetime
from dateutil import relativedelta as rdelta
from dateutil.relativedelta import relativedelta
from easykrishi.lsettings.actionlog import actionLogUpdate,sendAutomaticCall
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from random import randint
import json
"""
Request URL :self.context['request'].build_absolute_uri()
"""
class UserMobileListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To List Out All Active Serializers.
	"""
	class Meta:
		model = User
		fields = ('id','name','is_active','first_name','last_name','mobile_number','aadhar_number','is_active')

class FormsInformationSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Get All 
	"""
	keys = serializers.SerializerMethodField()
	class Meta:
		model = FormsInformation
		fields = ('id','title','keys')
	def get_keys(self,obj):
		return FormKeysInformation.objects.filter(form=obj.id).values('form','key')


class PeopleSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Update and List Out Information of Contact/People.
	"""
	people_other_info = serializers.SerializerMethodField()
	class Meta:
		model = People

	def validate_peopleinstance(self,instance,user):
		people = UserPeople.objects.filter(people=instance.id,user=user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have This Contact in His People List."})
		else:
			return True

	def save(self, **kwargs):
		user = self.context['request'].user
		self.validate_peopleinstance(self.instance,user)
		validated_data = self.initial_data
		#if People.objects.filter(aadhar_number=validated_data['aadhar_number']).exclude(id=self.instance.id).count() > 0:
		#	raise serializers.ValidationError({"errors":"This Aaadhar Number is Already Used By Some One."})
		validated_data.pop('mobile_number')
		validated_data.pop('create_by')
		validated_data.pop('modified_by')
		user = self.context['request'].user
		People.objects.filter(id=self.instance.id).update(modified_by=user.id,district=validated_data['district'],aadhar_number=validated_data['aadhar_number'],latitude=validated_data['latitude'],longitude=validated_data['longitude'],house_number=validated_data['house_number'],village=validated_data['village'],state_name=validated_data['state_name'],sub_district_or_mandal=validated_data['sub_district_or_mandal'],country_name=validated_data['country_name'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],city_name=validated_data['city_name'],pincode=validated_data['pincode'])
		UserPeople.objects.filter(people=self.instance.id,user=user.id).update(nick_name=validated_data['first_name'])
		Groupmember.objects.filter(member=self.instance.id,create_by=user.id).update(name=validated_data['first_name'])
		
		if len(validated_data['aadhar_number'].lstrip().rstrip()) > 0:
			sendAutomaticCall(self.instance.mobile_number,1)
		other_info = self.initial_data.pop('other_info')
		other_info_list = []		
		actionLogUpdate(self,self.context['request'],"People",self.instance.id)
		return self.instance
		
	
	def get_people_other_info(self,obj):
		"""
			Get Extra Information Of This Contact.
		"""
		return []
		
class UserSerializer(serializers.ModelSerializer):
	"""	
		This Serializer is Used To Register an User with an App.
	"""
	user_info = serializers.SerializerMethodField()
	access_token = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('id','access_token','name','is_active','first_name','last_name','is_active','user_info')

	def get_access_token(self,obj):
		"""
		"""
		data = {}
		expire_seconds = oauth2_settings.user_settings['ACCESS_TOKEN_EXPIRE_SECONDS']
		scopes = oauth2_settings.user_settings['SCOPES']
		#application = Application.objects.get(name="ApplicationName")		
		expires = datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)
		user = obj
		if user:
			application = Application.objects.filter(user=user.id).first()
			if application is None:
				application = Application.objects.create(user=user, client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type=Application.GRANT_PASSWORD)			
			
			access_token = AccessToken.objects.create(user=user,application=application,token=generate_token(),expires=expires,scope=scopes)
			refresh_token = RefreshToken.objects.create(user=user,token=generate_token(),access_token=access_token,application=application)			
			data = {'user':user.id,'client_id':application.client_id,'client_secret':application.client_secret,'access_token': access_token.token,'token_type': 'Bearer','expires_in': expire_seconds,'refresh_token': refresh_token.token,'scope': scopes}
			return data
		else:
			return data

	def getDeviceInfo(self):
		device = {}
		if 'device_information' in self.initial_data:
			if 'device_id' in self.initial_data['device_information']:
				device = self.initial_data['device_information']['device_id']
		return device
	
	def create(self,validated_data):
		"""
			this method is used to register an user.
		"""	
		data = self.initial_data
		people = self.initial_data['people']		
		user = User.objects.filter(aadhar_number=self.initial_data['aadhar_number'],mobile_number=self.initial_data['mobile_number']).first()
		device = self.getDeviceInfo()
		if user is not None:
			User.objects.filter(id=user.id).update(device_information=json.dumps(device),last_modified=datetime.datetime.now(),first_name=data['first_name'],last_name=data['last_name'],name=data['name'])				
			people_instance = People.objects.filter(aadhar_number=user.aadhar_number,mobile_number=user.mobile_number).update(village=people['village'],sub_district_or_mandal=people['sub_district_or_mandal'],district=people['district'],city_name=people['city_name'],state_name=people['state_name'],country_name=people['country_name'],pincode=people['pincode'],latitude=people['latitude'],longitude=people['longitude'],house_number=people['house_number'],is_synced=True,first_name=data['first_name'],last_name=data['last_name'])
			return User.objects.filter(id=user.id).first()
		if User.objects.filter(mobile_number=self.initial_data['mobile_number']).exists():
			raise serializers.ValidationError({"errors":"Mobile Number Should be Unique."})
		if User.objects.filter(aadhar_number=self.initial_data['aadhar_number']).exists():
			raise serializers.ValidationError({"errors":"QR Number Should be Unique"})
		
		otp = Otpverification.objects.filter(mobile_number=data['mobile_number'],is_verified=True).first()
		if otp is not None:			
			user = User.objects.create(device_information=json.dumps(device),is_active=True,mobile_number=data['mobile_number'],aadhar_number=data['aadhar_number'],**validated_data)			
			password = str(user.mobile_number) + user.aadhar_number[-4:]
			user.set_password(password)
			user.save()
			offline_id = randint(1,1000)
			people_instance = People.objects.create(offline_id=offline_id,create_by=user,village=people['village'],sub_district_or_mandal=people['sub_district_or_mandal'],district=people['district'],city_name=people['city_name'],state_name=people['state_name'],country_name=people['country_name'],pincode=people['pincode'],latitude=people['latitude'],longitude=people['longitude'],house_number=people['house_number'],is_synced=True,mobile_number=data['mobile_number'],aadhar_number=data['aadhar_number'],first_name=data['first_name'],last_name=data['last_name'],modified_by=user)
			UserPeople.objects.create(offline_id=offline_id,nick_name=user.first_name,user=user,people=people_instance)			
			actionLogUpdate(self,self.context['request'],"User",user.id)
			actionLogUpdate(self,self.context['request'],"People",people_instance.id)
			sendAutomaticCall(user.mobile_number,1)
		else:
			raise serializers.ValidationError({"errors":"Otp Verification Failed."})		
		return user

	def validate_userinstance(self,instance):
		if int(self.context['request'].user.id) != int(instance.id):
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access to Update this information."})
		else:
			return True

	def update(self,instance,validated_data):
		self.validate_userinstance(instance)

		data = self.initial_data
		people = self.initial_data['people']
		User.objects.filter(id=instance.id).update(last_modified=datetime.datetime.now(),first_name=data['first_name'],last_name=data['last_name'],name=data['name'])				
		people_instance = People.objects.filter(aadhar_number=instance.aadhar_number,mobile_number=instance.mobile_number).update(village=people['village'],sub_district_or_mandal=people['sub_district_or_mandal'],district=people['district'],city_name=people['city_name'],state_name=people['state_name'],country_name=people['country_name'],pincode=people['pincode'],latitude=people['latitude'],longitude=people['longitude'],house_number=people['house_number'],is_synced=True,first_name=data['first_name'],last_name=data['last_name'])		
		actionLogUpdate(self,self.context['request'],"User",instance.id)		
		return User.objects.filter(id=instance.id).first()

	def get_user_info(self,obj):
		return PeopleSerializer(instance = People.objects.filter(create_by=obj.id).first()).data

class UserleadersSerializer(serializers.ModelSerializer):
	"""
		This Serializer is used to Create/Update User Leader Information.
	"""
	class Meta:
		model = Userleaders	

class UserleadersListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used to List Out User Leader Information
	"""
	user = UserSerializer()
	leader = UserSerializer()
	class Meta:
		model = Userleaders

class UserPeopleSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To See All People's/Contact's Of an User.
	"""
	people = PeopleSerializer()
	class Meta:
		model = UserPeople


