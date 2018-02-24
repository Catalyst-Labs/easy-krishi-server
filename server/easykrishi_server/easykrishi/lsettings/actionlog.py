from django.contrib.auth.models import Group
from userinfo.models import *
from django.conf import settings
import pdb
import requests
import json

"""
	Global Functions
"""
def sendAutomaticCall(numbers,val):
	"""
		Here,we are sending Inviting Call To Formars After Registration.
	"""
	URL = settings.CALL_URL+str(numbers)
	response = requests.request('GET',URL)
	res = json.loads(response.text)
	return True
def actionLogUpdate(self,request,model,indexid=None,action=None):
	"""	
		HERE,we are Maintaing a Log For Each and Every API Call By User.
	"""	
	url = request.build_absolute_uri()	
	if request.user.id is not None:
		user = request.user
	elif model == 'User':
		if indexid is not None:
			user = User(id=indexid)
		else:
			return True
	elif model == 'People':
		if indexid is not None:
			people_instance = People.objects.filter(id=indexid).first()
			if people_instance is not None:
				user = people_instance.modified_by
			else:
				return True
		else:
			return True
	else:
		return True		
	device_id = ""
	latitude = 0.0
	longitude = 0.0
	if action is None:
		action = request.META['REQUEST_METHOD']
	if action == "GET":		
		if 'device_id' in request.GET:
			device_id = request.GET['device_id']
		if 'latitude' in request.GET:
			latitude = request.GET['latitude']
		if 'longitude' in request.GET:
			longitude = request.GET['longitude']
		if len(device_id) ==0 or device_id is None:
			device_id = ""
		ActionLog.objects.create(model=model,index_id=0,action_method=action,create_by=request.user,action_url=url,device_id=device_id,latitude=float(latitude),longitude=float(longitude))
		return True
	else:
		if indexid is None:
			indexid = 0
		if 'device_information' in request.data:
			device_info = request.data['device_information']
			if 'device_id' in device_info:
				device_id = device_info['device_id']
			if 'latitude' in device_info:
				latitude = device_info['latitude']
			if 'longitude' in device_info:
				longitude = device_info['longitude']
			if len(device_id) ==0 or device_id is None:
				device_id = ""
			ActionLog.objects.create(model=model,index_id=indexid,action_method=action,create_by=user,action_url=url,device_id=device_id,latitude=float(latitude),longitude=float(longitude))
			return True
		return True
