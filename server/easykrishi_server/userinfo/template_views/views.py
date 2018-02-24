from django.shortcuts import render, render_to_response
from django.template import Context, Template,RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.template.loader import get_template
from django.shortcuts import render,redirect
from easykrishi.lsettings.templatepagination import Paginator
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.models import User,Group
from userinfo.models import *
from groups.models import *

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

from xlsxwriter.workbook import Workbook
import io
import datetime
from django.db.models import Count

def DashboardView(request):
	"""
		Here,we are checking is user is login or not.
		If user is already login into the app ,we are redirect to home page or else requesting login page
		action:{GET}
		URL :{domainname}/user/api/v1/home/
	"""
	model = People
	template_name = 'app/dist/html/index.html'
	if request.user.is_authenticated():
		# if request.user.is_superuser:
		# 	return HttpResponseRedirect('/admin/')
		# else:
		people_by_user = UserPeople.objects.filter(user=request.user.id)
		total_people_by_user = people_by_user.count()
		user_location = People.objects.filter(id__in=[i.people_id for i in people_by_user]).exclude(Q(aadhar_number='') | Q(latitude=None) | Q(longitude=None)).values('id','latitude','longitude','village','first_name','mobile_number')
		location_data  = json.dumps(list(user_location), cls=DjangoJSONEncoder)			
		verified_user = people_by_user.exclude(Q(people__aadhar_number='') | Q(people__state_name=None))			
		today_reg_people = people_by_user.filter(created_date=datetime.date.today()).count()
		
		hierarchical_data_query = verified_user.values('people__state_name').annotate(dcount=Count('people__state_name'))
		
		return render_to_response('app/dist/html/index.html', {'request':request,'json_location_data':location_data,'total':total_people_by_user,'today':today_reg_people,'state_query':hierarchical_data_query,'state_data':12})

	else:
		return HttpResponseRedirect('/login/')

@login_required(login_url="/login/")
class PeopleChooseList(ListView):
	"""
		Here,we will get Group Members Based On Selected Group
		action:{GET}
		URL :{domainname}/groups/api/v1/choose-list/{people}/{group}
	"""
	model = UserPeople
	template_name = 'app/dist/html/table/people_buy_sell/choose.html'
	paginator_class = Paginator
	paginate_by = settings.PAGENATE_BY

	def get_queryset(self):
		return UserPeople.objects.filter(people=self.kwargs.get('people'))


def get_leaders_list_data(queryset):
	"""
	"""
	user_list = [i['user'] for i in queryset]
	q_set = [i for i in queryset]
	i = 0
	while i == 0:
		querylist = Userleaders.objects.filter(leader__in=user_list).values('id','user','user__name','leader__name','user__mobile_number','user__aadhar_number','create_date','last_modified')
		if len(querylist) == 0:
			break
		user_list = [i['user'] for i in querylist]
		q_set += [i for i in querylist]
	return q_set

def xlsx_file_write_and_download(model_data,header_data,xlsx_file_name):
	"""
	"""
	output = io.BytesIO()
	row = 1
	work_book = Workbook(output)
	work_sheet = work_book.add_worksheet(xlsx_file_name) 
	if model_data:
		date_format = work_book.add_format()
		date_format.set_num_format('dd/mm/yyyy hh:mm AM/PM') 
		work_sheet.set_row(0, 25)
		bold_format = work_book.add_format({'bold': True})
		for data in model_data:
			for col, item in enumerate(header_data):
				work_sheet.write(0, col,    item['value'].upper(),bold_format)
				work_sheet.set_column('B:Z', 20)
				if isinstance(data[item['key']], datetime.date) == True : #check if col is Date Time
					work_sheet.write(row, col, data[item['key']], date_format)
				else:
					work_sheet.write(row, col,    data[item['key']])

			row += 1  
	else:
		alignment_format = work_book.add_format()
		alignment_format.set_align('center')
		alignment_format.set_align('vcenter')
		work_sheet.set_row(0, 70)
		work_sheet.set_column('A:A', 30)
		work_sheet.write(0, 0, "No data for "+xlsx_file_name,alignment_format)
	work_book.close()
	# construct response
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename="+xlsx_file_name+".xlsx"
	return response

@login_required(login_url="/login/")
def download_xlsx_file(request):
	"""
	Function for download xlsx file.
	"""	
	"""--------------------------------"""	
	if request.GET['page']=='contact':
		#'people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode'
		model_query = UserPeople.objects.filter(user=request.user.id).exclude(people__aadhar_number=request.user.aadhar_number,people__mobile_number=request.user.mobile_number).values('id','nick_name','people__first_name','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','people__mobile_number','people__aadhar_number','created_date','date_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"QR Code","key":"people__aadhar_number"},{"value":"House Number","key":"people__house_number"},{"value":"Village","key":"people__village"},{"value":"Mandal","key":"people__sub_district_or_mandal"},{"value":"Disrict","key":"people__district"},{"value":"City Name","key":"people__city_name"},{"value":"State Name","key":"people__state_name"},{"value":"Country Name","key":"people__country_name"},{"value":"Pincode","key":"people__pincode"},{"value":"created date","key":"created_date"},{"value":"date modified","key":"date_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"contact_list")
	###==========================================###
	elif request.GET['page']=='peopleOrder':
		if 'people' in request.GET:
			model_query = Productbuyingdetails.objects.filter(people=request.GET['people']).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_required_date','create_date','last_modified')
		if 'product' in request.GET and 'date' in request.GET:
			date = datetime.datetime.strptime(request.GET['date'], "%Y-%m-%d").date()
			product = request.GET['product']
			model_query = Productbuyingdetails.objects.filter(product_name=product,create_date=date).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_required_date','create_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"required date","key":"product_required_date"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"QR Code","key":"people__aadhar_number"},{"value":"House Number","key":"people__house_number"},{"value":"Village","key":"people__village"},{"value":"Mandal","key":"people__sub_district_or_mandal"},{"value":"Disrict","key":"people__district"},{"value":"City Name","key":"people__city_name"},{"value":"State Name","key":"people__state_name"},{"value":"Country Name","key":"people__country_name"},{"value":"Pincode","key":"people__pincode"},{"value":"Added Date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"people_order_list")
	###==========================================###
	elif request.GET['page']=='peopleSelling':		
		if 'people' in request.GET:
			model_query = Productsellingdetails.objects.filter(people=request.GET['people']).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_harvest_date','alternate_address','create_date','last_modified')
		if 'product' in request.GET and 'date' in request.GET:
			date = datetime.datetime.strptime(request.GET['date'], "%Y-%m-%d").date()
			product = request.GET['product']
			model_query = Productsellingdetails.objects.filter(product_name=product,create_date=date).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_harvest_date','alternate_address','create_date','last_modified')
		#xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"product harvest date","key":"product_harvest_date"},{"value":"added date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		xlsx_header = [{"value":"#","key":"id"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"product harvest date","key":"product_harvest_date"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"QR Code","key":"people__aadhar_number"},{"value":"House Number","key":"people__house_number"},{"value":"Village","key":"people__village"},{"value":"Mandal","key":"people__sub_district_or_mandal"},{"value":"Disrict","key":"people__district"},{"value":"City Name","key":"people__city_name"},{"value":"State Name","key":"people__state_name"},{"value":"Country Name","key":"people__country_name"},{"value":"Pincode","key":"people__pincode"},{"value":"Added Date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"people_sell_list")

	###==========================================###
	elif request.GET['page']=='groupList':
		model_query = UserGroup.objects.filter(create_by=request.user.id).values('id','name','create_by__mobile_number','created_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"name","key":"name"},{"value":"mobile number","key":"create_by__mobile_number"},{"value":"create date","key":"created_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"group_list")

	###==========================================###

	elif request.GET['page']=='groupMemberList' and request.GET['group'] !='':
		#'member__house_number','member__village','member__sub_district_or_mandal','member__district','member__city_name','member__state_name','member__country_name','member__pincode'
		model_query = Groupmember.objects.filter(user_group=request.GET['group']).values('id','member__first_name','user_group__name','member__mobile_number','member__aadhar_number','member__house_number','member__village','member__sub_district_or_mandal','member__district','member__city_name','member__state_name','member__country_name','member__pincode','created_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"member__first_name"},{"value":"group name","key":"user_group__name"},{"value":"mobile number","key":"member__mobile_number"},{"value":"QR Code","key":"member__aadhar_number"},{"value":"House Number","key":"member__house_number"},{"value":"Village","key":"member__village"},{"value":"Mandal","key":"member__sub_district_or_mandal"},{"value":"Disrict","key":"member__district"},{"value":"City Name","key":"member__city_name"},{"value":"State Name","key":"member__state_name"},{"value":"Country Name","key":"member__country_name"},{"value":"Pincode","key":"member__pincode"},{"value":"added date","key":"created_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"group_member_list")	

	###==========================================###

	elif request.GET['page']=='groupOrderList' and request.GET['people'] != '' and request.GET['group'] != '':
		model_query = Productbuyingdetails.objects.filter(people=request.GET['people'],user_group=request.GET['group']).values('id','people__first_name','people__mobile_number','product_name','product_qty','product_price','alternate_address','create_date','last_modified','product_required_date')
		xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"required date","key":"product_required_date"},{"value":"added date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"group_order_list")

	###==========================================###

	elif request.GET['page']=='groupSellingList' and request.GET['people'] != '' and request.GET['group'] != '':
		model_query = Productsellingdetails.objects.filter(people=request.GET['people'],user_group=request.GET['group']).values('id','people__first_name','people__mobile_number','product_name','product_qty','product_price','product_harvest_date','alternate_address','create_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"available date","key":"product_harvest_date"},{"value":"added date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"group_selling_list")

	###==========================================###

	elif request.GET['page']=='leader':
		model_query = Userleaders.objects.filter(leader=request.user.id).values('id','user','user__name','leader__name','user__mobile_number','user__aadhar_number','create_date','last_modified')
		mmmm = get_leaders_list_data(model_query)
		xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"user__name"},{"value":"leader name","key":"leader__name"},{"value":"mobile number","key":"user__mobile_number"},{"value":"QR Code","key":"user__aadhar_number"},{"value":"create date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(mmmm,xlsx_header,"leaders_list")

	###==========================================###

	elif request.GET['page']=='leaderGroupList'  and request.GET['leader'] != '':
		model_query = UserGroup.objects.filter(create_by=request.GET['leader']).values('id','name','create_by__mobile_number','create_by__aadhar_number','created_date','last_modified')
		xlsx_header = [{"value":"leader name","key":"name"},{"value":"mobile number","key":"create_by__mobile_number"},{"value":"QR Code","key":"create_by__aadhar_number"},{"value":"create date","key":"created_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"leaders_group_list")

	###==========================================###

	elif request.GET['page']=='leaderGroupMemberList' and request.GET['group'] != '':
		model_query = Groupmember.objects.filter(user_group=request.GET['group']).values('id','member__first_name','user_group__name','member__mobile_number','member__aadhar_number','member__house_number','member__village','member__sub_district_or_mandal','member__district','member__city_name','member__state_name','member__country_name','member__pincode','created_date','last_modified')
		#xlsx_header = [{"value":"member name","key":"member__first_name"},{"value":"group name","key":"user_group__name"},{"value":"mobile number","key":"member__mobile_number"},{"value":"QR Code","key":"member__aadhar_number"},{"value":"added date","key":"created_date"},{"value":"last modified","key":"last_modified"}]
		xlsx_header = [{"value":"#","key":"id"},{"value":"member name","key":"member__first_name"},{"value":"group name","key":"user_group__name"},{"value":"mobile number","key":"member__mobile_number"},{"value":"QR Code","key":"member__aadhar_number"},{"value":"House Number","key":"member__house_number"},{"value":"Village","key":"member__village"},{"value":"Mandal","key":"member__sub_district_or_mandal"},{"value":"Disrict","key":"member__district"},{"value":"City Name","key":"member__city_name"},{"value":"State Name","key":"member__state_name"},{"value":"Country Name","key":"member__country_name"},{"value":"Pincode","key":"member__pincode"},{"value":"added date","key":"created_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"group_member_list")	

	###==========================================###
	else:
		header = ['#','state_name','first_name','mobile_number','date_joined','create_by__mobile_number']
		model_data = []
		return	xlsx_file_write_and_download(model_data,header,"file")

@login_required(login_url="/login/")
def exportOrders(request,val,product,date):
	"""
		URL:{domainname}/user/view/exportOrders/{{val}}/{{product_name}}/{{date}}
	"""
	date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	if int(val) == 1:
		model_query = Productbuyingdetails.objects.filter(product_image=product,create_date=date).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_required_date','create_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"required date","key":"product_required_date"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"QR Code","key":"people__aadhar_number"},{"value":"House Number","key":"people__house_number"},{"value":"Village","key":"people__village"},{"value":"Mandal","key":"people__sub_district_or_mandal"},{"value":"Disrict","key":"people__district"},{"value":"City Name","key":"people__city_name"},{"value":"State Name","key":"people__state_name"},{"value":"Country Name","key":"people__country_name"},{"value":"Pincode","key":"people__pincode"},{"value":"Added Date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"buy_order_list")
	else:
		model_query = Productsellingdetails.objects.filter(product_image=product,create_date=date).values('id','people__first_name','people__mobile_number','people__aadhar_number','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','product_name','product_qty','product_price','product_harvest_date','alternate_address','create_date','last_modified')
		xlsx_header = [{"value":"#","key":"id"},{"value":"product name","key":"product_name"},{"value":"product qty","key":"product_qty"},{"value":"product price","key":"product_price"},{"value":"product harvest date","key":"product_harvest_date"},{"value":"member name","key":"people__first_name"},{"value":"mobile number","key":"people__mobile_number"},{"value":"QR Code","key":"people__aadhar_number"},{"value":"House Number","key":"people__house_number"},{"value":"Village","key":"people__village"},{"value":"Mandal","key":"people__sub_district_or_mandal"},{"value":"Disrict","key":"people__district"},{"value":"City Name","key":"people__city_name"},{"value":"State Name","key":"people__state_name"},{"value":"Country Name","key":"people__country_name"},{"value":"Pincode","key":"people__pincode"},{"value":"Added Date","key":"create_date"},{"value":"last modified","key":"last_modified"}]
		return xlsx_file_write_and_download(model_query,xlsx_header,"sell_order_list")


@login_required(login_url="/login/")
def find_people_hierarchical_details(request):
	"""
	"""	
	model = People
	template_name = 'app/dist/html/index.html'
	if request.user.is_authenticated():
		# if request.user.is_superuser:
		# 	return HttpResponseRedirect('/admin/')
		# else:
		people_by_user = UserPeople.objects.filter(user=request.user.id)
		total_people_by_user = people_by_user.count()
		verified_user = people_by_user.exclude(Q(people__aadhar_number='') | Q(people__state_name=None) | Q(people__district=None) | Q(people__district=None) | Q(people__sub_district_or_mandal=None) | Q(people__village=None))
		user_location = People.objects.filter(id__in=[i.people_id for i in verified_user]).exclude(Q(aadhar_number='') | Q(latitude=None) | Q(longitude=None)).values('id','latitude','longitude','village','first_name','mobile_number')			
		
		today_reg_people = people_by_user.filter(created_date=datetime.date.today()).count()
		location_data  = json.dumps(list(user_location), cls=DjangoJSONEncoder)

		if request.GET['key'] == 'state':
			district_query = verified_user.filter(people__state_name =request.GET['state']).values('people__district').annotate(dcount=Count('people__district'))
			return render_to_response('app/dist/html/index.html', {'request':request,'json_location_data':location_data,'total':total_people_by_user,'today':today_reg_people,'district_query':district_query,'district_data':653})
		
		elif request.GET['key'] == 'district':
			mandal_query = verified_user.filter(people__district =request.GET['district']).values('people__sub_district_or_mandal').annotate(dcount=Count('people__sub_district_or_mandal'))
			return render_to_response('app/dist/html/index.html', {'request':request,'json_location_data':location_data,'total':total_people_by_user,'today':today_reg_people,'mandal_query':mandal_query,'mandal_data':653})
		
		elif request.GET['key'] == 'mandal':
			village_query = verified_user.filter(people__sub_district_or_mandal =request.GET['mandal']).values('people__village').annotate(dcount=Count('people__village'))
			return render_to_response('app/dist/html/index.html', {'request':request,'json_location_data':location_data,'total':total_people_by_user,'today':today_reg_people,'village_query':village_query,'village_user_data':653})
		
		elif request.GET['key'] == 'village':
			village_user_query = verified_user.filter(people__village =request.GET['village'])
			total_count = village_user_query.count()
			today_user_count = village_user_query.filter(created_date=datetime.date.today()).count()
			village_data = {'total_count':total_count,'today_user_count':today_user_count}
			
			return render_to_response('app/dist/html/index.html', {'request':request,'json_location_data':location_data,'total':total_people_by_user,'today':today_reg_people,'village_data':village_data,'village_user':653})					

	else:
		return HttpResponseRedirect('/login/')


from django.contrib.auth.hashers import make_password,check_password
@login_required(login_url="/login/")
def ChangePasswordView(request):
	if request.user.is_authenticated():
		if request.method == 'GET':
			return render_to_response('app/changepassword.html', {'request':request,'csrf_token':request.META.get('CSRF_COOKIE')})
		if request.method == 'POST':
			
			user = request.user
			old_password = None
			success = None
			if not user.check_password(request.POST['old_password']):
				old_password = {"errors":"Invalid Password."}
			
			if old_password is None:
				if request.POST['new_password1'] == request.POST['new_password2'] :
					user.set_password(request.POST['new_password1'])
					user.save()
					success = {"message":"Successfully Password is Changed"}
				else:
					old_password = {"errors":"Confirmation Password is not matching."}
			return render_to_response('app/changepassword.html', {'success':success,'request':request,'csrf_token':request.META.get('CSRF_COOKIE'),'old_password':old_password})		
	else:
		return HttpResponseRedirect('/login/')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def resetPasswordView(request):
	"""
	"""
	if request.method == 'POST':
		success = ''
		errors = ''
		response_kwargs = {}
		response_kwargs['content_type'] = 'application/json'
		if 'mobile_number' in request.POST:
			user = User.objects.filter(mobile_number=request.POST['mobile_number']).first()
			if user is not None:

				password = str(user.mobile_number) + user.aadhar_number[-4:]
				user.set_password(password)
				user.save()
				context = {'success':'Successfully your password reset to mobile number and last 4 digits of aadhar number.','csrf_token':request.META.get('CSRF_COOKIE'),'errors':errors}
				data = json.dumps(context)				
				return HttpResponse(data, **response_kwargs)				
			else:				
				errors = "Invalid Mobile Number."
				context = {'success':success,'csrf_token':request.META.get('CSRF_COOKIE'),'errors':errors}
				data = json.dumps(context)
				return HttpResponse(data, **response_kwargs)				
		else:
			errors = 'Please Enter Your Mobile Number'
			context = {'success':success,'csrf_token':request.META.get('CSRF_COOKIE'),'errors':errors}
			data = json.dumps(context)
			return HttpResponse(data, **response_kwargs)

##########################################################################
from userinfo.tables import *

def get_people_contact_list_queryset(request):
	return UserPeople.objects.filter(user=request.user.id)#.exclude(people__aadhar_number=request.user.aadhar_number,people__mobile_number=request.user.mobile_number)

@login_required(login_url="/login/")
def people_contact_list(request):
	"""
		Here,we are displaying user contacts information
		action:{GET}
		URL :{domainname}/user/api/v1/people-list/
	"""
	info_data = []
	query_set = get_people_contact_list_queryset(request)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__mobile_number','people__aadhar_number','people__first_name','people__last_name','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','created_date','date_modified','people_id')
	people_contact_list_data = UserPeopleTable(query_set_values)
	return render(request, "app/dist/html/table/peoplelist.html/", {'people_contact_list_data': people_contact_list_data,'info_data':info_data})

################################################################################################
def get_people_order_list_queryset(request,people):
	return Productbuyingdetails.objects.filter(user=request.user.id,people=people)

@login_required(login_url="/login/")
def people_order_list(request,people):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/people-ordered-list/{people}/
	"""
	info_data = []
	query_set = get_people_order_list_queryset(request,people)

	if query_set:
		info_data = query_set.first()
	
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_required_date','create_date','last_modified')	
	people_order_list_data = ProductbuyingdetailsTable(query_set_values)	
	return render(request, "app/dist/html/table/people_buy_sell/orderedlist.html/", {'people_order_list_data': people_order_list_data,'info_data':info_data})    
###############################################################################################
def get_people_selling_list_queryset(request,people):
	return Productsellingdetails.objects.filter(user=request.user.id,people=people)

@login_required(login_url="/login/")
def people_selling_list(request,people):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/people-sell-list/{people}
	"""
	info_data = []
	query_set = get_people_selling_list_queryset(request,people)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_harvest_date','create_date','last_modified')
	people_selling_list_data = ProductsellingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/people_buy_sell/sellinglist.html/", {'people_selling_list_data': people_selling_list_data,'info_data':info_data})

#mobile_number,aadhar_number,first_name,last_name,house_number,village,sub_district_or_mandal,district,city_name,state_name,country_name,pincode,date_joined,last_modified
#people__mobile_number,people__aadhar_number,people__first_name,people__last_name,people__house_number,people__village,people__sub_district_or_mandal,people__district,people__city_name,people__state_name,people__country_name,people__pincode,people__date_joined,people__last_modified
#'people__mobile_number','people__aadhar_number','people__first_name','people__last_name','people__house_number','people__village','people__sub_district_or_mandal','people__district','people__city_name','people__state_name','people__country_name','people__pincode','people__date_joined','people__last_modified'
