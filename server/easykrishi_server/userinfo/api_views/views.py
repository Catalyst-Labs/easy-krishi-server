from django.contrib.auth.models import Group
from userinfo.models import *
from groups.models import Groupmember
from easykrishi.lsettings.permissions import IsAuthenticatedOrCreate,HasGroupPermission,TokenHasScope
from .user_serializers import *
from rest_framework import serializers

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
import ast
import pdb
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from easykrishi.lsettings.paginationclass import LinkHeaderPagination
from easykrishi.lsettings.actionlog import actionLogUpdate,sendAutomaticCall
from rest_framework.pagination import PageNumberPagination





class AccessTokenGenerate(APIView):
	"""
		This Url is Used To Generate Access Token For User.

		URL:{domainname}/user/api/v1/access_token/
		action:{POST}
		sample:{"user":1,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}}
	"""	
	def post(self, request, format=None):
		"""
			Here,we are generating access_token if user is valid.		
		"""		
		expire_seconds = oauth2_settings.user_settings['ACCESS_TOKEN_EXPIRE_SECONDS']
		scopes = oauth2_settings.user_settings['SCOPES']
		#application = Application.objects.get(name="ApplicationName")		
		expires = datetime.datetime.now() + datetime.timedelta(seconds=expire_seconds)		

		user = User.objects.filter(id=request.data['user']).first()
		if user:
			application = Application.objects.filter(user=user.id).first()
			if application is None:
				application = Application.objects.create(user=user, client_type=Application.CLIENT_CONFIDENTIAL,authorization_grant_type=Application.GRANT_PASSWORD)
			
			# We delete the old one
			#AccessToken.objects.filter(user=user.id).delete()
			access_token = AccessToken.objects.create(user=user,application=application,token=generate_token(),expires=expires,scope=scopes)

			refresh_token = RefreshToken.objects.create(user=user,token=generate_token(),access_token=access_token,application=application)			
			token = {'user':user.id,'client_id':application.client_id,'client_secret':application.client_secret,'access_token': access_token.token,'token_type': 'Bearer','expires_in': expire_seconds,'refresh_token': refresh_token.token,'scope': scopes}	
			return Response(token,status=status.HTTP_200_OK)
		else:
			return Response({"errors":"Invalid User Request."},status=status.HTTP_400_BAD_REQUEST)


class OtpDetails(APIView):
	"""
		This Url is Used To Generate Otp Number For Every Mobile Number.

		URL:{domainname}/user/api/v1/otp_create/
		action:{POST}
		sample:{"mobile_number":9999999999,"otp_number":4564555,"is_verified":false/true,"expired_date":"2016-06-25",,"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}}
	"""
	def post(self, request, format=None):
		otp = Otpverification.objects.filter(mobile_number=request.data['mobile_number']).first()
		if otp is not None:
			otp.otp_number = request.data['otp_number']
			otp.expired_date = request.data['expired_date']
			otp.create_date = datetime.date.today()
			otp.is_verified = request.data['is_verified']
			otp.save()
		else:
			otp = Otpverification.objects.create(is_verified=request.data['is_verified'],expired_date=request.data['expired_date'],otp_number=request.data['otp_number'],mobile_number=request.data['mobile_number'])
			actionLogUpdate(self,request,"Otpverification")
		data = {"id":otp.id,"mobile_number":otp.mobile_number,"create_date":otp.create_date,"otp_number":otp.otp_number,"expired_date":otp.expired_date}
		return Response(data,status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
	"""
		This Class Is Used To Create an User From Mobile App.
		Here,validating mobile numbers with otp details.

		URL:{domainname}/user/api/v1/user-create/
		action:{POST}
		sample:
		{	
			"mobile_number":9999999999,
			"aadhar_number":"xxxxxx",
			"first_name":"xxxx",
			"last_name":"xxxx",
			"name":"xxxx",
			"people":{
						"latitude":74.16,
						"longitude":74.10,
						"house_number":"xxx",
						"village":"zzz",
						"sub_district_or_mandal":"zzz",
						"district":"zzz",
						"city_name":"zzz",
						"state_name":"zzz",
						"country_name":"zzz",
						"pincode":524124,
						"is_synced":true
					},"device_information":{"device_id":{},"latitude":"75.222","longitude":74.12}
		}
	"""
	model = User
	serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
	"""
		This Class Is Used To Update Information Of  an  Existing User From Mobile App.
		Here,validating mobile numbers with otp details.

		URL:{domainname}/user/api/v1/user-update/{pk}/
		action:{PUT,GET}
		sample:
		{	
			"mobile_number":9999999999,
			"aadhar_number":"xxxxxx",
			"first_name":"xxxx",
			"last_name":"xxxx",
			"name":"xxxx",
			"people":{
						"latitude":74.16,
						"longitude":74.10,
						"house_number":"xxx",
						"village":"zzz",
						"sub_district_or_mandal":"zzz",
						"district":"zzz",
						"city_name":"zzz",
						"state_name":"zzz",
						"country_name":"zzz",
						"pincode":524124,
						"is_synced":true
					},"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	model = User
	serializer_class = UserSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','PUT']
	required_scopes = ['groups']

	def validate_userinstance(self):
		if int(self.kwargs.get('pk')) != self.request.user.id:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have access to read this information."})
		else:
			return True

	def get_queryset(self):
		self.validate_userinstance()
		actionLogUpdate(self,self.request,"User")
		return User.objects.filter(id=self.kwargs.get('pk'))

class PeopleCreateView(APIView):
	
	"""
		This View Class is Used To Add People To User Contact's/People's.
		URL:{domainname}/user/api/v1/user-people-create/
		action:{POST}
		sample:
		{
			"people":[
				{
					"mobile_number":77777777,
					"first_name":"xxxx",
					"last_name":"xxxx",
					"offline_id":1
				},
				{
					"mobile_number":77777777,
					"first_name":"xxxx",
					"last_name":"xxxx",
					"offline_id":1
				}
			],
			"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}	
		
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {		 
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']
	
	def post(self,request,format=None):
		user = self.request.user
		user_people = []
		for data in request.data['people']:
			offline_id = 0
			if 'offline_id' in data:
				offline_id = data['offline_id']
			people = People.objects.filter(mobile_number=data['mobile_number']).first()
			if people is None:
				people = People.objects.create(offline_id = offline_id,mobile_number=data['mobile_number'],first_name=data['first_name'],last_name=data['last_name'],create_by=user,modified_by=user)
			if UserPeople.objects.filter(user=self.request.user.id,people=people.id).count() == 0:
				user_people.append(UserPeople(offline_id = offline_id,nick_name=data['first_name'],user=self.request.user,people=people))
		UserPeople.objects.bulk_create(user_people)
		actionLogUpdate(self,request,"People")
		return Response({"response":"Successfully Added."},status=status.HTTP_200_OK)

class PeopleDataUpdateView(generics.RetrieveUpdateDestroyAPIView):
	"""
		This View Class is Used To Add People To User Contact's/People's.
		

		URL:{domainname}/user/api/v1/user-people-update/{pk}/
		action:{GET,DELETE,PUT}
		sample:
		{
			"latitude":74.16,						
			"aadhar_number":"xxxxxx",
			"first_name":"xxxx",
			"last_name":"xxxx",
			"longitude":74.10,
			"house_number":"xxx",
			"village":"zzz",
			"sub_district_or_mandal":"zzz",
			"district":"zzz",
			"city_name":"zzz",
			"state_name":"zzz",
			"country_name":"zzz",
			"pincode":524124,
			"is_synced":true,
			"create_by":1,
			"modified_by":1,
			"mobile_number":12222222,
			"offline_id" : 20,
			"other_info":[
							{
								"key":"xxxxxx",
								"value":"xxxxx",
								"offiline_id":21,
							}
			],"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	model = People
	serializer_class = PeopleSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','PUT','DELETE']
	required_scopes = ['groups']

	def validate_peopleinstance(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('pk'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have This Contact in His People List."})
		else:
			return True
	def get_queryset(self):
		self.validate_peopleinstance()
		actionLogUpdate(self,self.request,"People",self.kwargs.get('pk'))
		return People.objects.filter(id=self.kwargs.get('pk'))

	def delete(self, request, *args, **kwargs):		
		queryset = self.get_queryset()
		#user_people = UserPeople.objects.filter(people=self.kwargs.get('pk')).exclude(user=self.request.user.id)
		if queryset.exists():
			UserPeople.objects.filter(people=self.kwargs.get('pk'),user=self.request.user.id).delete()			
			return Response({"response":"Successfully Removed"},status=status.HTTP_200_OK)
		else:
			return Response({"response":"Invalid Contact/People"},status=status.HTTP_400_BAD_REQUEST)

class UserContactList(generics.ListAPIView):
	"""
		This View is Used To Display All User Contacts/Peoples Information.
		URL:{domainname}/user/api/v1/user-people-list/
		action:{GET}
	"""
	model = UserPeople
	serializer_class = UserPeopleSerializer
	pagination_class = LinkHeaderPagination
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']
	def get_queryset(self):
		actionLogUpdate(self,self.request,"People")
		return UserPeople.objects.filter(user=self.request.user.id).order_by('-id')#.exclude(people__aadhar_number=self.request.user.aadhar_number,people__mobile_number=self.request.user.mobile_number)


class GetLeadersListView(generics.ListAPIView):
	"""
		This View is Used To Get User's List By User Input.
		URL:{domainname}/user/api/v1/leaders-list/?mobile-num=720/
		action:{GET}
	"""
	model = User
	serializer_class = UserMobileListSerializer	
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']

	def get_queryset(self):
		if 'mobile-num' in self.request.GET:
			if len(self.request.GET['mobile-num']) > 0:
				return User.objects.filter(is_active=True,mobile_number__icontains=self.request.GET['mobile-num']).exclude(id=self.request.user.id).order_by('-id')
			else:
				return User.objects.filter(is_active=True).exclude(id=self.request.user.id).order_by('-id')
		else:
			return User.objects.filter(is_active=True).exclude(id=self.request.user.id).order_by('-id')

class ChangeLeaderView(generics.CreateAPIView):
	"""
		This View is Used To Update His Leader information.If The Leader is not Present with Our DB ,we will Show Error to User.
		

		URL:{domainname}/user/api/v1/user-leader-update/
		action:{GET,POST}
		sample:{
				"user":18,
				"leader":"7895645613",
				"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	model = Userleaders
	serializer_class = UserleadersSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']

	def validate_data(self,request):
		if 'user' in request.data:
			if int(request.data['user']) != self.request.user.id:
				raise serializers.ValidationError({"errors":"Invalid User"})
			else:
				return True
		return True

	def create(self, request, *args, **kwargs):
		"""
		"""
		self.validate_data(request)	
		user = User.objects.filter(mobile_number=request.data['leader']).first()
		if user is not None:
			if user.id == self.request.user.id:
				return Response({"errors":"Sorry,We can not assign as a leader by himself."},status=status.HTTP_400_BAD_REQUEST)
			else:
				if user.is_active == False:
					return Response({"errors":"Requested leader is inactive"},status=status.HTTP_400_BAD_REQUEST)
				else:
					user_leader = Userleaders.objects.filter(user=self.request.user.id).first()
					if user_leader is not None:
						user_leader.leader = user
						user_leader.last_modified = datetime.datetime.now()				
						user_leader.save()
						actionLogUpdate(self,request,"Userleaders")
						return Response(UserleadersSerializer(instance=user_leader).data,status=status.HTTP_200_OK)
					else:
						user_leader = Userleaders.objects.create(user=self.request.user,leader=user,last_modified = datetime.datetime.now(),create_date=datetime.date.today())
						actionLogUpdate(self,request,"Userleaders")
					return Response(UserleadersSerializer(instance=user_leader).data,status=status.HTTP_200_OK)
		else:
			return Response({"errors":"Requested Leader Does Not Exist."},status=status.HTTP_400_BAD_REQUEST)

class getOtherInfoList(APIView):
	"""
		Here,GET Method is used to get All Other Details by this view.
		URL:{domainname}/user/api/v1/other-details-list/{people}/
	"""
	model = FormsInformation
	serializer_class = FormsInformationSerializer
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET']
	required_scopes = ['groups']
	
	def getPeopleObj(self):
		people = UserPeople.objects.filter(people=self.kwargs.get('people'),user=self.request.user.id).first()
		if people is None:
			raise serializers.ValidationError({"errors":"Requested User Doesn't Have This Contact in His People List."})
		else:
			return people

	def get_obj(self,obj):
		user = self.request.user
		people_obj = PeopleKeysDetails.objects.filter(people=self.kwargs.get('people'),form=obj['id']).first()
		if people_obj is None:
			keys = FormKeysInformation.objects.filter(form=obj['id']).values('key')
			for key in keys:
				key['value'] = ''
			return keys
		else:
			keys = FormKeysInformation.objects.filter(form=obj['id']).values('key')			
			value = ast.literal_eval(people_obj.value)			
			arr = []
			value_keys = [i['key'] for i in value]
			for key in keys:
				if key['key'] in value_keys:
					obj = {}
					obj['key'] = key['key']
					obj['value'] = ""
					for k in value:
						if key['key'] == k['key']:
							obj['value'] = k['value']
							break
					arr.append(obj)
				else:
					obj = {}
					obj['key'] = key['key']
					obj['value'] = ""
					arr.append(obj)				
			return arr
		return []

	def get(self,request,people,format=None):
		"""
			GET Forms  with People Answers
		"""
		people = self.getPeopleObj()
		forms = FormsInformation.objects.filter().values('id','title')
		data = []	
		for form in forms:
			data_obj = {}
			form['obj'] = self.get_obj(form)
			data.append(form)
		actionLogUpdate(self,self.request,"FormsInformation")
		return Response(data,status=status.HTTP_200_OK)	

class PeopleFormUpdateView(APIView):
	"""
		URL:{domainname}/user/api/v1/people-form-details-update/
		Sample input:
		{
			"form":1,
			"offline_id" : 1,
			"people":1,
			"obj" : [{"key":"key_value","value":"val"}],
			"device_information":{"device_id":"device id","latitude":"75.222","longitude":74.12}
		}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['POST','GET']
	required_scopes = ['groups']

	def post(self,request,format=None):
		data = request.data
		user = self.request.user
		people = UserPeople.objects.filter(people=data['people'],user=self.request.user.id).first()
		if people is None:
			return Response({"errors":"Requested User Doesn't Have This Contact in His People List."},status=status.HTTP_400_BAD_REQUEST)

		offline_id = 0
		if 'offline_id' in data:
			offline_id = data['offline_id']

		peopl_obj = PeopleKeysDetails.objects.filter(people=people.people.id,form=data['form']).first()
		if peopl_obj is not None:
			peopl_obj.value = data['obj']
			peopl_obj.save()
		else:
			PeopleKeysDetails.objects.create(offline_id=offline_id,create_by=user,value=data['obj'],people=people.people,form=FormsInformation(id=data['form']))
		actionLogUpdate(self,request,"PeopleKeysDetails")
		return Response({"response":"successfully Updated"},status=status.HTTP_200_OK)

"""
	People Synchronization From APP TO Server.
"""
from django.db import transaction

def getFormsInformation():
	"""
		return all forms along with keys
	"""
	return FormsInformationSerializer(FormsInformation.objects.filter(),many=True).data

class UserPeopleSynchronization(APIView):
	"""
	HERE,POST Method is Allowed to Synchrnize data from mobile to server by this api.
	

	URL :{domainname}/user/api/v1/people-sync-view/
	sample input:
	{"people_data":[{
	"latitude": 74.16,
	"aadhar_number": "789456",
	"first_name": "sree",
	"last_name": "p",
	"longitude": 74.10,
	"house_number": "41",
	"village": "bengaluru",
	"sub_district_or_mandal": "zzz",
	"district": "zzz",
	"city_name": "zzz",
	"state_name": "zzz",
	"country_name": "zzz",
	"pincode": 524124,
	"is_synced": true,
	"mobile_number": "78945665",
	"offline_id": 1,
	"date_joined":"2016-06-02 10:16:29"
	}, {
	    "latitude": 74.16,
	    "aadhar_number": "7894563",
	    "first_name": "srinivas",
	    "last_name": "p",
	    "longitude": 74.10,
	    "house_number": "41",
	    "village": "bengaluru",
	    "sub_district_or_mandal": "zzz",
	    "district": "zzz",
	    "city_name": "zzz",
	    "state_name": "zzz",
	    "country_name": "zzz",
	    "pincode": 524124,
	    "is_synced": true,
	    "mobile_number": "789456653",
	    "offline_id": 1,
	    "date_joined":"2016-06-02 10:16:29"

	}],
	"device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
	}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']
	
	@transaction.atomic
	def post(self,request,format=None):
		"""
		"""		
		user_id = self.request.user.id
		user = self.request.user
		now = datetime.datetime.now()
		date = datetime.date.today()
		user_people_list = []
		people_other_info_list = []
		people_list = []
		call_list = []
		for data in request.data['people_data']:
			"""----checking people information----"""
			people = People.objects.filter(mobile_number=data['mobile_number']).first()			
			if people is None:
				"""----adding people information----"""
				people = People.objects.create(date_joined=data['date_joined'],mobile_number=data['mobile_number'],district=data['district'],aadhar_number=data['aadhar_number'],latitude=data['latitude'],longitude=data['longitude'],house_number=data['house_number'],village=data['village'],state_name=data['state_name'],sub_district_or_mandal=data['sub_district_or_mandal'],country_name=data['country_name'],first_name=data['first_name'],last_name=data['last_name'],city_name=data['city_name'],is_synced=True,create_by=user,modified_by=user,pincode=data['pincode'],offline_id=data['offline_id'])
				user_people_list.append(UserPeople(offline_id = data['offline_id'],nick_name=data['first_name'],user=user,people=people))
			else:				
				#if len(people.aadhar_number.lstrip().rstrip()) != 0:					
				if len(data['aadhar_number'].lstrip().rstrip()) > 0:
					People.objects.filter(id=people.id).update(district=data['district'],aadhar_number=data['aadhar_number'],latitude=data['latitude'],longitude=data['longitude'],house_number=data['house_number'],village=data['village'],state_name=data['state_name'],sub_district_or_mandal=data['sub_district_or_mandal'],country_name=data['country_name'],first_name=data['first_name'],last_name=data['last_name'],city_name=data['city_name'],is_synced=True,modified_by=user_id,pincode=data['pincode'],offline_id=data['offline_id'])
				if UserPeople.objects.filter(user=self.request.user.id,people=people.id).count() == 0:
					"""----adding people information----"""
					user_people_list.append(UserPeople(offline_id = data['offline_id'],nick_name=data['first_name'],user=user,people=people))
				else:
					UserPeople.objects.filter(user=self.request.user.id,people=people.id).update(nick_name=data['first_name'])
				Groupmember.objects.filter(member=people.id,create_by=self.request.user.id).update(name=data['first_name'])
			people_list.append(people.id)
			if len(data['aadhar_number']) > 0 and data['is_synced'] == False:
				call_list.append(str(people.mobile_number))
			
		if len(user_people_list) > 0:
			UserPeople.objects.bulk_create(user_people_list)


		if len(call_list) > 0:
			sendAutomaticCall(','.join(call_list),1)
		actionLogUpdate(self,request,"People")

		people_data = UserPeopleSerializer(UserPeople.objects.filter(user=self.request.user.id,people__in=people_list),many=True).data
		return Response({"response":"successfully added",'form_data':getFormsInformation(),"data":people_data},status=status.HTTP_200_OK)





class FormSyncView(APIView):
	"""
		Here,POST METHOD is Allowed To Sync All Forms Of People.
		URL:{domainname}/user/api/v1/form-sync-view/
		SAMPLE:{
				"data":	[	
							{ "form":"agri", "offline_id" : 1, "people":9999999999, "obj" : [{"key":"key_value","value":"val"}] }
							,{ "form":"agri", "offline_id" : 1, "people":9999999999, "obj" : [{"key":"key_value","value":"val"}]}
						]
				,"device_information":{"device_id":{},"latitude":0.0,"longitude":0.0}
				}
	"""
	permission_classes = (HasGroupPermission,IsAuthenticatedOrCreate,TokenHasScope)
	required_groups = {
	 }
	actions = ['GET','POST']
	required_scopes = ['groups']
	def getPeople(self,people_id):
		people = UserPeople.objects.filter(user=self.request.user.id,people__mobile_number=people_id).first()
		
		if people is None:
			return people
		return people.people

	def getFormObj(self,data):		
		obj_data = None		
		keys = FormKeysInformation.objects.filter(form__title=data['form'])#.values('key','form')
		value = data['obj']
		arr = []		
		value_keys = [i['key'] for i in value]		
		for key in keys:
			if key.key in value_keys:
				obj = {}
				obj['key'] = key.key
				obj['value'] = ""
				for k in value:
					if key.key == k['key']:
						obj['value'] = k['value']
						break
				arr.append(obj)
			else:
				obj = {}
				obj['key'] = key.key
				obj['value'] = ""
				arr.append(obj)		
		if len(keys) == 0:
			return obj_data
		else:
			obj_data = {}
			obj_data['form'] = keys[0].form	
		obj_data['obj'] = arr				
		return obj_data
	
	@transaction.atomic
	def post(self,request,format=None):
		
		res_data = []
		data = []		
		people_keys= []		
		if 'data' in request.data:
			data = request.data['data']
		for d in data:
			res_obj = {}
			people = self.getPeople(d['people'])						
			if people is not None:
				form_obj = self.getFormObj(d)				
				if form_obj is not None:
					res_obj['people_mobile_number'] = people.mobile_number
					res_obj['people_id'] = people.id
					res_obj['form_id'] = form_obj['form'].id
					res_obj['form'] = form_obj['form'].title
					res_obj['obj'] = form_obj['obj']					
					res_data.append(res_obj)
					peopl_obj = PeopleKeysDetails.objects.filter(people=people.id,form=form_obj['form'].id).first()
					
					if peopl_obj is not None:						
						peopl_obj.value = form_obj['obj']
						peopl_obj.last_modified = datetime.datetime.now()
						peopl_obj.offline_id=d['offline_id']
						peopl_obj.save()
					else:
						people_keys.append(PeopleKeysDetails(offline_id=d['offline_id'],create_by=self.request.user,value=form_obj['obj'],people=people,form=form_obj['form']))
		PeopleKeysDetails.objects.bulk_create(people_keys)
		actionLogUpdate(self,request,"PeopleKeysDetails")
				
		return Response({"response":"Successfully Updated","res_data":res_data,'form_data':getFormsInformation()},status=status.HTTP_200_OK)
