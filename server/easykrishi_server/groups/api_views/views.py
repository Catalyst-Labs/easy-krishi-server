from django.contrib.auth.models import Group
from userinfo.models import *
from groups.models import *
from easykrishi.lsettings.permissions import IsAuthenticatedOrCreate,HasGroupPermission,TokenHasScope
from .group_serializers import *

from rest_framework import generics
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import Application,AccessToken,RefreshToken
import datetime
from dateutil import relativedelta as rdelta
from dateutil.relativedelta import relativedelta
from easykrishi.lsettings.actionlog import actionLogUpdate
import pdb
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from easykrishi.lsettings.paginationclass import LinkHeaderPagination
from rest_framework.pagination import PageNumberPagination
from userinfo.api_views.views import getFormsInformation

class UserGroupCreateView(generics.CreateAPIView):
	"""
		Here,we are creating group for people.

		URL:{domainname}/groups/api/v1/user-group-create/
		action:{POST}
		sample:
		{	
			"name":"name",
			"create_by":1,
			"offline_id":1,
			"leader":1,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	model = UserGroup
	serializer_class = UserGroupSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']

class UserGroupUpdateView(generics.RetrieveUpdateDestroyAPIView):
	"""
		Here,we can update the details of an User Group Details

		URL:{domainname}/groups/api/v1/user-group-update/{pk}/
		action:{PUT,DELETE,GET}
		sample:
		{	
			"name":"name",
			"create_by":1,
			"offline_id":1,
			"leader":1,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	model = UserGroup
	serializer_class = UserGroupSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','PUT','DELETE']
	required_scopes = ['groups']

	def validate_requestdata(self,queryset):
		if len(queryset) != 0:
			if queryset[0].create_by.id != self.request.user.id:
				raise serializers.ValidationError({"errors":"Invalid User Request."})
			return True
		return True

	def get_queryset(self):
		queryset = UserGroup.objects.filter(id=self.kwargs.get('pk'))
		self.validate_requestdata(queryset)
		actionLogUpdate(self,self.request,"UserGroup")
		return queryset

	def delete(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		if queryset.exists():
			UserGroup.objects.filter(id=self.kwargs.get('pk')).delete()			
			return Response({"response":"Successfully Removed"},status=status.HTTP_200_OK)
		else:
			return Response({"response":"Invalid User Group Selection"},status=status.HTTP_400_BAD_REQUEST)

class UserGroupListView(generics.ListAPIView):
	"""
		Here,we are Listing All Groups Based On User.

		URL:{domainname}/groups/api/v1/user-group-list-count/
		action:{GET}
	"""
	model = UserGroup
	serializer_class = UserGroupSerializer
	pagination_class = LinkHeaderPagination 
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']

	def get_queryset(self):
		actionLogUpdate(self,self.request,"UserGroup")
		return UserGroup.objects.filter(create_by=self.request.user.id).order_by('-id')

class GroupMembersListview(generics.ListAPIView):
	"""
		ere,we can Add People/Contact To The Group and also we can remove from the group.

		URL :{domainname}/groups/api/v1/group-members-list/{group}
		action :{GET}		
	"""
	model = Groupmember
	serializer_class = GroupMembersListSerializer
	
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']

	def checkGroup(self,group):
		group = UserGroup.objects.filter(id=group,create_by=self.request.user.id).first()
		if group is None:
			raise serializers.ValidationError({"errors":"WARNING:Requested User accessing Other User Created Groups Information."})
		return True
	
	def get_queryset(self):
		self.checkGroup(self.kwargs.get('group'))
		actionLogUpdate(self,self.request,"UserGroup")
		return Groupmember.objects.filter(user_group=self.kwargs.get('group'),create_by=self.request.user.id).order_by('-id')

class AddorMembersToGroup(APIView):
	"""
		Here,we can Add People/Contact To The Group and also we can remove from the group.

		URL :{domainname}/groups/api/v1/add-remove-member/
		action :{POST}
		sample:
		For Adding People To Group:
			{
				"user_group":1,				
				"people":[{"offline_id":1,"first_name":"name","last_name":"","mobile_number":4141402365}],
				"flag":0 or other,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}
		For Removing Members From Group:
			{
				"user_group":1,
				"member":[1,2,3],				
				"flag":0 or other,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}

		if flag == 0 : we are adding members to the group 
		other than "0" we are removing members from the group
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def checkGroup(self,group):
		group = UserGroup.objects.filter(id=group,create_by=self.request.user.id).first()
		if group is None:
			raise serializers.ValidationError({"errors":"WARNING:Requested User accessing Other User Created Groups Information."})
		return True
	
	def post(self,request,format=None):
		user = self.request.user
		self.checkGroup(request.data['user_group'])
		group = request.data['user_group']
		if request.data['flag'] == 0:
			bulk_list = []
			user_people_list = []
			if 'people' in request.data:
				for data in request.data['people']:
					offline_id = 0
					if 'offline_id' in data:
						offline_id = data['offline_id']
					people = People.objects.filter(mobile_number=data['mobile_number']).first()
					if people is None:
						people = People.objects.create(offline_id=offline_id,mobile_number=data['mobile_number'],first_name=data['first_name'],last_name=data['last_name'],create_by=user,modified_by=user)					
					if UserPeople.objects.filter(user=self.request.user.id,people=people.id).count() == 0:
						user_people_list.append(UserPeople(offline_id=offline_id,nick_name=data['first_name'],user=self.request.user,people=people))
					if Groupmember.objects.filter(member=people.id,user_group=group).count() == 0:
						bulk_list.append(Groupmember(offline_id=offline_id,member=people,name=data['first_name'],create_by=self.request.user,user_group=UserGroup(id=group)))				
				Groupmember.objects.bulk_create(bulk_list)
				UserPeople.objects.bulk_create(user_people_list)
				actionLogUpdate(self,request,"UserGroup")
				return Response({"response":"Successfully Added"},status=status.HTTP_200_OK)
				pass
			else:
				return Response({"errors":"Probelem with Request Parameters.",},status=status.HTTP_400_BAD_REQUEST)
		else:
			Groupmember.objects.filter(member__in=request.data['member'],create_by=self.request.user.id,user_group=group).delete()
			return Response({"response":"Successfully Removed"},status=status.HTTP_200_OK)

class AddProductbuyingdetailsView(generics.CreateAPIView):
	"""
		Here,POST Method is Allowed to Create an Product From People.
		If People want to buy one Product group together from Organization.
		Based On the Demand,people will get discount.

		URL :{domainname}/groups/api/v1/buy-product-create/?access_token=xxxx
		action :{POST}
		sample:
			{
				"product_name": "rice",
				"product_image": FILE,
				"offline_id":1,
				"product_qty": "12",
				"product_price": 1.0,
				"measurement" : "units",
				"product_required_date": "2016-05-26",
				"alternate_address": "Bangalore",
				"user_group": 1,
				"user":1,
				"people": 6,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}		
	"""
	model = Productbuyingdetails
	serializer_class = ProductbuyingdetailsSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

class ProductbuyingdetailsUpdateView(generics.RetrieveUpdateDestroyAPIView):
	"""
		Here,GET,PUT and DELETE Method's are allowed To Perform actions.
		By This,we can update,delete and retrive information of an Existing Record.
		

		URL :{domainname}/groups/api/v1/buy-product-update/{pk}/?access_token=xxxx
		action :{PUT}
		sample:
			{
				"product_name": "rice",
				"offline_id":1,
				"product_image": FILE,
				"product_qty": "12",
				"product_price": 1.0,
				"measurement" : "units",
				"product_required_date": "2016-05-26",
				"alternate_address": "Bangalore",
				"user_group": 1,
				"user":1,
				"people": 6,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}
	"""
	model = Productbuyingdetails
	serializer_class = ProductbuyingdetailsSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['PUT','DELETE','GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('pk'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have Access of This Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productbuyingdetails")
		return Productbuyingdetails.objects.filter(user=self.request.user.id,id=self.kwargs.get('pk'))

	def delete(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		if queryset.exists():
			Productbuyingdetails.objects.filter(id=self.kwargs.get('pk')).delete()			
			return Response({"response":"Successfully Removed"},status=status.HTTP_200_OK)
		else:
			return Response({"response":"Invalid Product Selection"},status=status.HTTP_400_BAD_REQUEST)

class ProductbuyingdetailsListView(generics.ListAPIView):
	"""
		Here,GET Method is allowed to List Out All Product Details Of People with Respect to Group and People

		URL :{domainname}/groups/api/v1/buy-product-list/{people}/{usergroup}/?access_token=xxxx
		action :{GET}
	"""
	model = Productbuyingdetails
	serializer_class = ProductbuyingdetailsSerializer
	pagination_class = LinkHeaderPagination
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('people'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access of this Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productbuyingdetails")
		return Productbuyingdetails.objects.filter(user=self.request.user.id,people=self.kwargs.get('people'),user_group=self.kwargs.get('usergroup')).order_by('-id')


class AddProductsellingdetailsView(generics.CreateAPIView):
	"""
		Here,POST Method is Allowed to Create an Product From People.
		If People want to Sell one Product group together from People.
		Based On the Demand,people will get good price.


		URL :{domainname}/groups/api/v1/sell-product-create/?access_token=xxxx
		action :{POST}
		sample:
			{
				"product_name": "rice",
			    "product_image": "http://localhost:8000/groups/api/v1/sell-product-create/products/sell/cde39da9-028d-4795-b5f9-f95c4f2f3ece.png",
			    "product_qty": "12",
			    "offline_id":1,
			    "product_price": 1.0,
			    "measurement" : "units",
			    "product_harvest_date": "2016-05-26",
			    "alternate_address": "Bangalore",			    
			    "user_group": 1,
			    "user":1,
			    "people": 6,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}
	"""
	model = Productsellingdetails
	serializer_class = ProductsellingdetailsSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

class ProductsellingdetailsUpdateView(generics.RetrieveUpdateDestroyAPIView):
	"""
		Here,GET,PUT and DELETE Method's are allowed To Perform actions.
		By This,we can update,delete and retrive information of an Existing Record.
		

		URL :{domainname}/groups/api/v1/sell-product-update/{pk}/?access_token=xxxx
		action :{PUT}
		sample:
			{
				"product_name": "rice",
				"product_image": FILE,
				"product_qty": "12",
				"product_price": 1.0,
				"measurement" : "units",
				"product_harvest_date": "2016-05-26",
				"alternate_address": "Bangalore",
				"user_group": 1,
				"offline_id":1,
				"user":1,
				"people": 6,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
			}
	"""
	model = Productsellingdetails
	serializer_class = ProductsellingdetailsSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['PUT','DELETE','GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('pk'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have Access Of This Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productsellingdetails")
		return Productsellingdetails.objects.filter(user=self.request.user.id,id=self.kwargs.get('pk'))

	def delete(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		if queryset.exists():
			Productsellingdetails.objects.filter(id=self.kwargs.get('pk')).delete()			
			return Response({"response":"Successfully Removed"},status=status.HTTP_200_OK)
		else:
			return Response({"response":"Invalid Product Selection"},status=status.HTTP_400_BAD_REQUEST)

class ProductsellingdetailsListView(generics.ListAPIView):
	"""
		Here,GET Method is allowed to List Out All Product Details Of People with Respect to Group and People

		URL :{domainname}/groups/api/v1/sell-product-list/{people}/{usergroup}/?access_token=xxxx
		action :{GET}
	"""
	model = Productsellingdetails
	serializer_class = ProductsellingdetailsSerializer
	pagination_class = LinkHeaderPagination
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('people'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access of this Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productsellingdetails")
		return Productsellingdetails.objects.filter(user=self.request.user.id,people=self.kwargs.get('people'),user_group=self.kwargs.get('usergroup')).order_by('-id')

class ContactProductbuyingdetailsListView(generics.ListAPIView):
	"""
		Here,GET Method is allowed to List Out All Product Details Of User.

		URL :{domainname}/groups/api/v1/contact-buy-product-list/{people}/?access_token=xxxx
		action :{GET}
	"""
	model = Productbuyingdetails
	serializer_class = ProductbuyingdetailsSerializer
	pagination_class = LinkHeaderPagination
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('people'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access of this Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productbuyingdetails")
		return Productbuyingdetails.objects.filter(user=self.request.user.id,people=self.kwargs.get('people')).order_by('-id')


class ContactProductsellingdetailsListView(generics.ListAPIView):
	"""
		Here,GET Method is allowed to List Out All Product Details Of People.

		URL :{domainname}/groups/api/v1/contact-sell-product-list/{people}/?access_token=xxxx
		action :{GET}
	"""
	model = Productsellingdetails
	serializer_class = ProductsellingdetailsSerializer
	pagination_class = LinkHeaderPagination
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('people'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access of this Contact Products."})
		else:
			return True

	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"Productsellingdetails")		
		return Productsellingdetails.objects.filter(user=self.request.user.id,people=self.kwargs.get('people')).order_by('-id')
"""
	Synchronizing Offline Data From Mobile to Server
	GroupsAndMembers --->
"""
from django.db import transaction
class GroupsAndMembers(APIView):
	"""
		Here,we will add Groups and along with members to DB .
		If user is added some products ,we are inserting into DB By using View
		URL:{domainname}/groups/api/v1/groups-sync-view/
		sampleINPUT:
		{
		    "add_data": [
		        {
		            "group_name": "name",
		            "offline_id": 1,
		            "members": [
		                {
		                    "first_name": "first_name",
		                    "last_name": "last_name",
		                    "mobile_number": 789456123,
		                    "created_date":"2016-06-02 10:16:29",
		                    "offline_id": 1,
		                    "product_buy_list": [
		                        {
		                            "product_name": "rice",
		                            "offline_id": 1,
		                            "product_image":"image",
		                            "product_qty": "12",
		                            "product_price": 1,
		                            "measurement": "units",
		                            "product_required_date": "2016-05-26",
		                            "alternate_address": "Bangalore",
		                            "create_date":"2016-01-01"
		                        }
		                    ],
		                    "product_sell_list": [
		                        {
		                            "product_name": "rice",
		                            "offline_id": 2,
		                            "product_image":"image",
		                            "product_qty": "12",
		                            "product_price": 1,
		                            "measurement": "units",
		                            "product_harvest_date": "2016-05-26",
		                            "alternate_address": "Bangalore",
		                            "create_date":"2016-01-01"
		                        }
		                    ]
		                }
		            ]
		        }
		    ],
		    "remove_data": [
		        {
		            "group_name": "name",
		            "members": [
		                456123
		            ]
		        }
		    ],
		    "device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
		}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def addPeople(self,members,user,now,group):
		"""
		"""		
		user_people_list = []
		people_id_list = []
		bulk_list = []
		product_buy_list = []
		product_sell_list = []
		for data in members:
			offline_id = 0
			if 'offline_id' in data:
				offline_id = data['offline_id']
			people = People.objects.filter(mobile_number=data['mobile_number']).first()
			if people is None:
				people = People.objects.create(date_joined=data['created_date'],offline_id=offline_id,mobile_number=data['mobile_number'],first_name=data['first_name'],last_name=data['last_name'],create_by=user,modified_by=user)
				user_people_list.append(UserPeople(created_date=data['created_date'],offline_id=offline_id,nick_name=data['first_name'],user=self.request.user,people=people))
				bulk_list.append(Groupmember(created_date=data['created_date'],offline_id=offline_id,member=people,name=data['first_name'],create_by=self.request.user,user_group=group))
			else:
				if UserPeople.objects.filter(user=self.request.user.id,people=people.id).count() == 0:
					user_people_list.append(UserPeople(created_date=data['created_date'],offline_id=offline_id,nick_name=data['first_name'],user=self.request.user,people=people))
				else:
					UserPeople.objects.filter(user=self.request.user.id,people=people.id).update(nick_name=data['first_name'])
				if Groupmember.objects.filter(member=people.id,user_group=group.id).count() == 0:
					bulk_list.append(Groupmember(created_date=data['created_date'],offline_id=offline_id,member=people,name=data['first_name'],create_by=self.request.user,user_group=group))				
				else:
					Groupmember.objects.filter(member=people.id,user_group=group.id).update(name=data['first_name'])
			product_image = ''
			people_id_list.append(people.id)
			if 'product_buy_list' in data:
				for buy in data['product_buy_list']:
					if 'offline_id' in buy:
						offline_id = buy['offline_id']
					if 'product_image' in buy:
						product_image = buy['product_image']
					if Productbuyingdetails.objects.filter(offline_id=offline_id,people=people.id).exists():
						continue
					else:
						product_buy_list.append(Productbuyingdetails(product_image=product_image,user=user,people=people,user_group=group,offline_id=offline_id,product_name=buy['product_name'],create_date=buy['create_date'],product_price=buy['product_price'],product_qty=buy['product_qty'],measurement=buy['measurement'],alternate_address=buy['alternate_address'],product_required_date=buy['product_required_date']))

			if 'product_sell_list' in data:
				for sell in data['product_sell_list']:
					if 'offline_id' in sell:
						offline_id = sell['offline_id']
					if 'product_image' in sell:
						product_image = sell['product_image']
					if Productsellingdetails.objects.filter(offline_id=offline_id,people=people.id).exists():
						continue
					else:
						product_sell_list.append(Productsellingdetails(product_image=product_image,user=user,people=people,user_group=group,offline_id=offline_id,product_name=sell['product_name'],create_date=sell['create_date'],product_price=sell['product_price'],product_qty=sell['product_qty'],measurement=sell['measurement'],alternate_address=sell['alternate_address'],product_harvest_date=sell['product_harvest_date']))
		
		Groupmember.objects.bulk_create(bulk_list)
		UserPeople.objects.bulk_create(user_people_list)
		Productsellingdetails.objects.bulk_create(product_sell_list)
		Productbuyingdetails.objects.bulk_create(product_buy_list)
		return people_id_list
	
	def checkGroup(self,d,now,user):
		"""
			Checking Group Details
		"""				
		group = UserGroup.objects.filter(name=d['group_name'],create_by=user.id).first()
		if group is None:
			group = UserGroup.objects.create(name=d['group_name'],create_by=user,leader=user,offline_id=d['offline_id'])
		else:
			UserGroup.objects.filter(id=group.id).update(last_modified=now)
		return group

	def addData(self,data):
		"""
			Here,adding Members to group and along with products.
		"""
		res_data = []
		user_id = self.request.user.id
		user = self.request.user
		date = datetime.date.today()
		now = datetime.datetime.now()
		for d in data:
			res_grp_obj = {}
			group = self.checkGroup(d,now,user)
			res_grp_obj['id'] = group.id
			res_grp_obj['offline_id'] = group.offline_id
			res_grp_obj['name'] = group.name
			res_grp_obj['create_by'] = group.create_by.id
			res_grp_obj['leader'] = group.leader_id
			res_grp_obj['created_date'] = group.created_date
			res_grp_obj['last_modified'] = group.last_modified
			res_grp_obj['count'] = Groupmember.objects.filter(user_group=group.id).count()
			res_grp_obj['member_ids'] = []
			if 'members' in d:
				res_grp_obj['member_ids'] = self.addPeople(d['members'],user,now,group)
			res_grp_obj['members'] = GroupMembersSyncSerializer(Groupmember.objects.filter(user_group=group.id,member__in=res_grp_obj['member_ids']),many=True).data
			res_data.append(res_grp_obj)
		return res_data

	def removeData(self,request_data):
		for data in request_data:
			group = UserGroup.objects.filter(name=data['group_name'],create_by=self.request.user.id).first()
			if group is not None:
				Groupmember.objects.filter(member__mobile_number__in=data['members'],user_group=group.id,create_by=self.request.user.id).delete()
		return {"response":"successfully Removed","data":[]}
	
	@transaction.atomic
	def post(self,request,format=None):
		"""
			Here,adding and remove members from group
		"""		
		data = request.data		
		if 'add_data' in data:
			res_data = self.addData(data['add_data'])
			actionLogUpdate(self,request,"UserGroup")
			actionLogUpdate(self,request,"UserPeople")
			actionLogUpdate(self,request,"Groupmember")				
			return Response({"response":"successfully added",'form_data':getFormsInformation(),"data":res_data},status=status.HTTP_200_OK)
		if 'remove_data' in data:
			rt_data = self.removeData(data['remove_data'])
			actionLogUpdate(self,request,"UserPeople")
			actionLogUpdate(self,request,"Groupmember")
			return Response(rt_data,status=status.HTTP_200_OK)

class productEditBuyList(APIView):
	"""
		URL:{domainname}/groups/api/v1/buy-edit-list/
		{
			"buy_edit_list":[
							{
									"id" : 1,
									"offline_id":1,
									"product_name": "rice",									
									"product_qty": "12",
									"product_price": 1.0,
									"measurement" : "units",
									"product_required_date": "2016-05-26",
									"alternate_address": "Bangalore",
									"user_group": 1,
									"user":1,
									"people": 6,
									"create_date":"2016-01-01"
							}

				],
				"device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
		}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']
	@transaction.atomic
	def post(self,request,format=None):		
		now = datetime.datetime.now()		
		for data in request.data['buy_edit_list']:
			if 'id' in data and 'user' in data:
				if int(self.request.user.id) == int(data['user']):
					Productbuyingdetails.objects.filter(id=data['id'],user=data['user']).update(product_qty=data['product_qty'],measurement=data['measurement'],product_price=data['product_price'],alternate_address=data['alternate_address'],last_modified=now,product_required_date=data['product_required_date'],product_name=data['product_name'],offline_id=data['offline_id'])
		actionLogUpdate(self,request,"Productbuyingdetails")
		return Response({"response":"Successfully Updated",'form_data':getFormsInformation()},status=status.HTTP_200_OK)

class productEditSellList(APIView):
	"""
		URL:{domainname}/groups/api/v1/sell-edit-list/
		{
			"sell_edit_list":[
							{
									"id" : 1,
									"offline_id":1,
									"product_name": "rice",									
									"product_qty": "12",
									"product_price": 1.0,
									"measurement" : "units",
									"product_harvest_date": "2016-05-26",
									"alternate_address": "Bangalore",
									"user_group": 1,
									"user":1,
									"people": 6,
									"create_date":"2016-01-01"
							}

				],
				"device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
		}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']
	@transaction.atomic
	def post(self,request,format=None):
		now = datetime.datetime.now()

		for data in request.data['sell_edit_list']:
			if 'id' in data and 'user' in data:
				if int(self.request.user.id) == int(data['user']):
					Productsellingdetails.objects.filter(id=data['id']).update(product_qty=data['product_qty'],measurement=data['measurement'],product_price=data['product_price'],alternate_address=data['alternate_address'],last_modified=now,product_harvest_date=data['product_harvest_date'],product_name=data['product_name'],offline_id=data['offline_id'])
		actionLogUpdate(self,request,"Productsellingdetails")
		return Response({"response":"Successfully Updated",'form_data':getFormsInformation()},status=status.HTTP_200_OK)

from userinfo.api_views.user_serializers import FormsInformationSerializer
class GetUserFullData(APIView):
	"""
	URL:{domainname}/groups/api/v1/user-full-data/
	
	{
	"device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
	}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']
	def post(self,request,format=None):
		obj = {}
		obj['forms_data'] = FormsInformationSerializer(FormsInformation.objects.filter(),many=True).data
		obj['people_data'] = UserPeopleListSerializer(UserPeople.objects.filter(user=self.request.user.id),many=True).data
		obj['groups_data'] = GroupListSerializer(UserGroup.objects.filter(create_by=self.request.user.id),many=True).data
		obj['form_data'] = getFormsInformation()
		actionLogUpdate(self,request,"FormsInformation")
		actionLogUpdate(self,request,"UserPeople")
		actionLogUpdate(self,request,"UserGroup")
		return Response(obj,status=status.HTTP_200_OK)