from django.db import models
from userinfo.models import *
import os,uuid
import datetime

# Create your models here.

class UserGroup(models.Model):
	"""
		This Model Describes,User Created Groups.
		Name Describes,Name Of The Group
	"""
	offline_id = models.BigIntegerField(default=0)
	name = models.CharField(max_length=45)
	create_by = models.ForeignKey(User, db_column='create_by',related_name='created_user')
	leader = models.ForeignKey(User,related_name='group_leader')
	created_date = models.DateField(auto_now_add=False,default=datetime.date.today)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Groupmember(models.Model):
	"""
		This Model Describes,GroupMemebers Information.
		For Every Group ,atleast One Member Should be There.
	"""
	offline_id = models.BigIntegerField(default=0)
	user_group = models.ForeignKey(UserGroup,on_delete=models.CASCADE)
	member = models.ForeignKey(People,on_delete=models.CASCADE)
	create_by = models.ForeignKey(User, db_column='create_by')
	name = models.CharField(max_length=100, blank=True, null=True)
	created_date = models.DateTimeField(auto_now=True)
	last_modified = models.DateTimeField(auto_now=True)


def set_unique_image_for_buy(self,filename=None):
	"""
	function to determine where to save images.  assigns a uuid (random string) to each and places it
	in the images subdirectory below media.  by default, we assume the file is a .jpg
	"""	
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	# TODO: 'images' is hard coded    
	return os.path.join('products/buy', filename)

class Productbuyingdetails(models.Model):
	"""
		This Model Describes,Product Buying Information.
		If People want to buy an Product group together,they can enter the details here.
	"""
	offline_id = models.BigIntegerField(default=0)
	product_name = models.CharField(max_length=200)
	#product_image = models.ImageField(upload_to=set_unique_image_for_buy,blank=True)
	product_image = models.CharField(max_length=100, blank=True)
	product_qty = models.CharField(max_length=100, blank=True, null=True)
	measurement = models.CharField(max_length=100)
	product_price = models.FloatField(blank=True, null=True)
	alternate_address = models.CharField(max_length=250, blank=True, null=True)
	create_date = models.DateField(auto_now_add=False,default=datetime.date.today)
	last_modified = models.DateTimeField(auto_now=True)
	user_group = models.ForeignKey(UserGroup,on_delete=models.CASCADE)
	people = models.ForeignKey(People,on_delete=models.CASCADE)
	product_required_date = models.DateField(blank=True, null=True)
	user = models.ForeignKey(User,related_name= "user_people_buy_product")


def set_unique_image_for_sell(self,filename=None):
	"""
	function to determine where to save images.  assigns a uuid (random string) to each and places it
	in the images subdirectory below media.  by default, we assume the file is a .jpg
	"""    
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	# TODO: 'images' is hard coded    
	return os.path.join('products/sell', filename)

class Productsellingdetails(models.Model):
	"""
		This Model Describes,Product Selling Information.
		If People want to Sell an Product group together,they can enter the details here.
	"""
	offline_id = models.BigIntegerField(default=0)
	product_name = models.CharField(max_length=200)
	#product_image = models.ImageField(upload_to=set_unique_image_for_sell,blank=True)
	product_image = models.CharField(max_length=100, blank=True)
	product_qty = models.CharField(max_length=100)
	measurement = models.CharField(max_length=100)
	product_price = models.FloatField()
	product_harvest_date = models.DateField()
	alternate_address = models.CharField(max_length=250, blank=True, null=True)
	create_date = models.DateField(auto_now_add=False,default=datetime.date.today)
	last_modified = models.DateTimeField(auto_now=True)
	user_group = models.ForeignKey(UserGroup,on_delete=models.CASCADE)
	people = models.ForeignKey(People,on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name= "user_people_sell_product")
