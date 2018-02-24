from rest_framework import serializers
from django.db import transaction, models
from django.conf import settings
from userinfo.api_views.user_serializers import PeopleSerializer
from userinfo.models import *
from groups.models import UserGroup,Groupmember,Productbuyingdetails,Productsellingdetails
import pdb
import ast
import datetime
from easykrishi.lsettings.actionlog import actionLogUpdate

class UserGroupTemplateSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Create/Update/Delete an Group
	"""
	count = serializers.SerializerMethodField()
	created_dt = serializers.SerializerMethodField()
	last_modified_dt = serializers.SerializerMethodField()
	class Meta:
		model = UserGroup

	def get_created_dt(self,obj):		
		return datetime.date(obj.created_date.year,obj.created_date.month,obj.created_date.day).strftime("%b %d, %Y")

	def get_last_modified_dt(self,obj):		
		d = datetime.datetime.strptime(str(obj.last_modified), "%Y-%m-%d %H:%M:%S")
		return d.strftime("%b %d,%Y, %I:%M %p")

	def get_count(self,obj):
		"""return lenth of group"""
		return Groupmember.objects.filter(user_group=obj.id).count()

	def create(self,validated_data):
		#pdb.set_trace()
		return UserGroup.objects.create(**validated_data)

class UserGroupSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Create/Update/Delete an Group
	"""
	count = serializers.SerializerMethodField()

	def validate_requestdata(self,attrs):
		if attrs['create_by'].id != self.context['request'].user.id:
			raise serializers.ValidationError({"errors":"Invalid User Request."})
		else:
			return True
	
	class Meta:
		model = UserGroup
	
	def get_count(self,obj):
		"""return lenth of group"""
		return Groupmember.objects.filter(user_group=obj.id).count()

	def create(self,validated_data):
		self.validate_requestdata(validated_data)
		group = UserGroup.objects.create(**validated_data)
		user = group.create_by		
		actionLogUpdate(self,self.context['request'],"UserGroup",group.id)
		return group

	def update(self,instance,validated_data):
		self.validate_requestdata(validated_data)
		if validated_data['create_by'].id != instance.create_by.id:
			raise serializers.ValidationError({"errors":"Invalid User Request."})
		UserGroup.objects.filter(id=instance.id).update(name=validated_data['name'],last_modified=datetime.datetime.now())
		return instance


class GroupMembersSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To add Contact to Group
	"""
	class Meta:
		model = Groupmember

class GroupMembersListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To List Out  Contact's/People's in a Group
	"""
	member = PeopleSerializer()
	class Meta:
		model = Groupmember

class ProductbuyingdetailsSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used TO Create an Record and Updating an Existing Record Of Productbuyingdetails .
	"""
	image_url = serializers.SerializerMethodField()
	class Meta:
		model = Productbuyingdetails
	def get_image_url(self,obj):
		return settings.IMAGE_BASE_URL+str(obj.product_image)

	def validate_peopleinstance(self,validated_data,instance=None):
		if self.context['request'].user.id != validated_data['user'].id:
			raise serializers.ValidationError({"errors":"Invalid User."})
		people = UserPeople.objects.filter(people=validated_data['people'].id,user=self.context['request'].user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have This Contact in His People List."})
		if instance is not None:
			if instance.user.id != self.context['request'].user.id:
				raise serializers.ValidationError({"errors":"Requested User Doesn't access to update this product."})
			return True
		return True

	def create(self,validated_data):
		self.validate_peopleinstance(validated_data)
		product = Productbuyingdetails.objects.create(**validated_data)
		actionLogUpdate(self,self.context['request'],"Productbuyingdetails",product.id)
		return product

	def update(self,instance,validated_data):
		self.validate_peopleinstance(validated_data,instance)
		validated_data['last_modified'] = datetime.datetime.now()
		Productbuyingdetails.objects.filter(id=instance.id).values().update(**validated_data)
		actionLogUpdate(self,self.context['request'],"Productbuyingdetails",instance.id)
		return Productbuyingdetails.objects.filter(id=instance.id).first()

class ProductsellingdetailsSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used TO Create an Record and Updating an Existing Record Of Productsellingdetails .
	"""
	image_url = serializers.SerializerMethodField()
	def get_image_url(self,obj):
		return settings.IMAGE_BASE_URL+str(obj.product_image)
	class Meta:
		model = Productsellingdetails

	def validate_peopleinstance(self,validated_data,instance=None):
		if self.context['request'].user.id != validated_data['user'].id:
			raise serializers.ValidationError({"errors":"Invalid User."})
		people = UserPeople.objects.filter(people=validated_data['people'].id,user=self.context['request'].user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have This Contact in His People List."})
		if instance is not None:
			if instance.user.id != self.context['request'].user.id:
				raise serializers.ValidationError({"errors":"Requested User Doesn't access to update this product."})
			return True
		return True

	def create(self,validated_data):
		self.validate_peopleinstance(validated_data)
		product = Productsellingdetails.objects.create(**validated_data)
		actionLogUpdate(self,self.context['request'],"Productsellingdetails",product.id)
		return product

	def update(self,instance,validated_data):
		self.validate_peopleinstance(validated_data,instance)
		validated_data['last_modified'] = datetime.datetime.now()
		Productsellingdetails.objects.filter(id=instance.id).values().update(**validated_data)
		actionLogUpdate(self,self.context['request'],"Productsellingdetails",instance.id)
		return Productsellingdetails.objects.filter(id=instance.id).first()

class PeopleSyncSerializer(serializers.ModelSerializer):
	"""
		It Will Give Group Member Details
	"""
	product_buy_list = serializers.SerializerMethodField()
	product_sell_list = serializers.SerializerMethodField()
	class Meta:
		model = People

	def get_product_buy_list(self,obj):		
		return Productbuyingdetails.objects.filter(create_date=datetime.date.today(),people=obj.id).values()

	def get_product_sell_list(self,obj):
		return Productsellingdetails.objects.filter(create_date=datetime.date.today(),people=obj.id).values()

class GroupMembersSyncSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To List Out  Contact's/People's in a Group
	"""
	member = PeopleSyncSerializer()
	class Meta:
		model = Groupmember

class PeopleListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Get Entire Information of People For requested User.
	"""
	forms = serializers.SerializerMethodField()
	class Meta:
		model = People

	def get_forms(self,obj):
		queryset = PeopleKeysDetails.objects.filter(people=obj.id).values('id','offline_id','value','people_id','form_id','form__title')
		arr = []
		for data in queryset:
			data['value'] = ast.literal_eval(data['value'])			
			arr.append(data)
		return arr

class UserPeopleListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To See All People's/Contact's Of an User.
	"""
	people = PeopleListSerializer()
	class Meta:
		model = UserPeople


class GroupMemberListSerializer(serializers.ModelSerializer):
	"""
		This Serializer is Used To Get Entire Information Of Group Members Based on Requested user.
	"""
	product_buy_list = serializers.SerializerMethodField()
	product_sell_list = serializers.SerializerMethodField()	
	member = serializers.SerializerMethodField()
	class Meta:
		model = Groupmember

	def get_product_buy_list(self,obj):
		return Productbuyingdetails.objects.filter(people=obj.member_id,user_group=obj.user_group_id).values()
	def get_product_sell_list(self,obj):
		return Productsellingdetails.objects.filter(people=obj.member_id,user_group=obj.user_group_id).values()
	def get_member(self,obj):
		queryset = People.objects.filter(id=obj.member_id).values()
		if len(queryset) > 0 :
			return queryset[0]
		return {}

class GroupListSerializer(serializers.ModelSerializer):
	"""
		This Serilaizer is Used To Get Entire Groups Information Based On Requested User.
	"""
	members = serializers.SerializerMethodField()
	count = serializers.SerializerMethodField()
	class Meta:
		model = UserGroup

	def get_members(self,obj):
		data = GroupMemberListSerializer(Groupmember.objects.filter(user_group=obj.id,create_by=obj.create_by.id),many=True).data
		return data

	def get_count(self,obj):
		"""return lenth of group"""
		return Groupmember.objects.filter(user_group=obj.id).count()
