from django.shortcuts import render, render_to_response
from django.conf import settings
from django.views.generic import TemplateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group
from userinfo.models import *
from groups.models import *
from easykrishi.lsettings.templatepagination import Paginator
from groups.api_views.group_serializers import *
import pdb
import datetime
from django.contrib.auth.decorators import login_required

class TChooseList(ListView):
	"""
		Here,we will get Group Members Based On Selected Group
		action:{GET}
		URL :{domainname}/groups/api/v1/choose-list/{people}/{group}
	"""
	model = Groupmember
	template_name = 'app/dist/html/table/choose.html'
	paginator_class = Paginator
	paginate_by = settings.PAGENATE_BY

	def get_queryset(self):
		return Groupmember.objects.filter(member=self.kwargs.get('people'),user_group=self.kwargs.get('group'))

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(TChooseList, self).dispatch(*args, **kwargs)

from groups.tables import *
def get_groups_list_queryset(request):				
	return UserGroup.objects.filter(create_by=request.user.id)

@login_required(login_url="/login/")
def groups_list(request):
	"""
		Here,we are display User Group List.
		action:{GET}
		URL :{domainname}/groups/api/v1/group-list/
	"""
	info_data = []
	query_set = get_groups_list_queryset(request)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('name','created_date','last_modified','id')
	groups_list_data = UserGroupTable(query_set_values)
	# return render(request, "table/grouplist.html/", {'groups_list_data': groups_list_data,'info_data':info_data})
	return render(request, "app/dist/html/table/grouplist.html/", {'groups_list_data': groups_list_data,'info_data':info_data})
####################################################################################
def get_groups_member_list_queryset(request,group):
	return Groupmember.objects.filter(user_group=group)

@login_required(login_url="/login/")
def groups_member_list(request,group):
	"""
		Here,we will get Group Members Based On Selected Group
		action:{GET}
		URL :{domainname}/groups/api/v1/members-list/{group}/
	"""
	info_data = []
	query_set = get_groups_member_list_queryset(request,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('member__first_name','user_group__name','member__mobile_number','member__aadhar_number','member__last_name','member__latitude','member__longitude','member__house_number','member__village','member__sub_district_or_mandal','member__district','member__city_name','member__state_name','member__country_name','member__pincode','created_date','member_id','user_group_id')
	groups_member_list_data = GroupmemberTable(query_set_values)
	return render(request, "app/dist/html/table/groupmemberslist.html/", {'groups_member_list_data': groups_member_list_data,'info_data':info_data})

####################################################################################
def get_group_order_list_queryset(people,group):
	return Productbuyingdetails.objects.filter(people=people,user_group=group)

@login_required(login_url="/login/")
def group_order_list(request,people,group):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/user-ordered-list/{people}/{group}
	"""
	info_data = []
	query_set = get_group_order_list_queryset(people,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_required_date','create_date','last_modified')
	group_order_list_data = ProductbuyingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/orderedlist.html/", {'group_order_list_data': group_order_list_data,'info_data':info_data})    
#================================
def get_group_selling_list_queryset(people,group):
	return Productsellingdetails.objects.filter(people=people,user_group=group)

@login_required(login_url="/login/")
def group_selling_list(request,people,group):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/user-sell-list/{people}/{group}
	"""
	info_data = []
	query_set = get_group_selling_list_queryset(people,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_harvest_date','create_date','last_modified')
	group_selling_list_data = ProductsellingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/sellinglist.html/", {'group_selling_list_data': group_selling_list_data,'info_data':info_data})  

################################################################################################
def get_leader_list_queryset(queryset):
	"""
	"""
	user_list = [i['user'] for i in queryset]
	q_set = [i for i in queryset]
	i = 0
	while i == 0:
		querylist = Userleaders.objects.filter(leader__in=user_list).values('id','user','user__name','leader__name','user__mobile_number','user__aadhar_number','create_date','last_modified','user_id')
		if len(querylist) == 0:
			break
		user_list = [i['user'] for i in querylist]
		q_set += [i for i in querylist]
	return q_set

@login_required(login_url="/login/")
def leader_list(request):
	"""
		Here,we will get Leaders who will under this requested user.
		action:{GET}
		URL :{domainname}/groups/api/v1/leaders-list/
	"""
	info_data = []
	model_query = Userleaders.objects.filter(leader=request.user.id).values('id','user','user__name','leader__name','user__mobile_number','user__aadhar_number','create_date','last_modified','user_id')
	query_set = get_leader_list_queryset(model_query)
	if query_set:
		info_data = query_set[0]
	leader_list_data = UserleadersTable(query_set)
	return render(request, "app/dist/html/table/leaders/leaders.html/", {'leader_list_data': leader_list_data,'info_data':info_data})
##################################################################################################
def get_leader_group_list_queryset(request,leader):				
		return UserGroup.objects.filter(create_by=leader)

@login_required(login_url="/login/")
def leader_group_list(request,leader):
	"""
		Here,we are display Leaders Group List.
		action:{GET}
		URL :{domainname}/groups/api/v1/leaders-group-list/{leader}
	"""
	info_data = []
	query_set = get_leader_group_list_queryset(request,leader)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('id','name','created_date','last_modified')
	leader_group_list_data = UserGroupLeaderTable(query_set_values)
	return render(request, "app/dist/html/table/leaders/leadersgrouplist.html/", {'leader_group_list_data': leader_group_list_data,'info_data':info_data})

##################################################################################################
def get_leader_group_member_list_queryset(request,group):				
	return Groupmember.objects.filter(user_group=group)

@login_required(login_url="/login/")
def leader_group_member_list(request,group):
	"""
		Here,we will get Group Members Based On Selected Leader Group
		action:{GET}
		URL :{domainname}/groups/api/v1/leaders-members-list/{group}/
	"""
	info_data = []
	query_set = get_leader_group_member_list_queryset(request,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('id','member__first_name','user_group__name','member__mobile_number','member__aadhar_number','created_date','member_id','user_group_id')
	group_member_list_data = GroupmemberLeaderTable(query_set_values)
	return render(request, "app/dist/html/table/leaders/leadergroupmemberslist.html/", {'group_member_list_data': group_member_list_data,'info_data':info_data})

class TLeaderChooseList(ListView):
	"""
		Here,we will get Group Members Based On Selected Group
		action:{GET}
		URL :{domainname}/groups/api/v1/choose-list/{people}/{group}
	"""
	model = Groupmember
	template_name = 'app/dist/html/table/leaders/choose.html'
	paginator_class = Paginator
	paginate_by = settings.PAGENATE_BY

	def get_queryset(self):
		return Groupmember.objects.filter(member=self.kwargs.get('people'),user_group=self.kwargs.get('group'))

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(TLeaderChooseList, self).dispatch(*args, **kwargs)

####################################################################################
def get_leaders_order_list_queryset(people,group):
	return Productbuyingdetails.objects.filter(people=people,user_group=group)

@login_required(login_url="/login/")
def leaders_order_list(request,people,group):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/leaders-ordered-list/{people}/{group}
	"""
	info_data = []
	query_set = get_leaders_order_list_queryset(people,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_required_date','create_date','last_modified')
	leaders_order_list_data = ProductbuyingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/leaders/orderedlist.html/", {'leaders_order_list_data': leaders_order_list_data,'info_data':info_data})    
#================================
def get_leaders_selling_list_queryset(people,group):
	return Productsellingdetails.objects.filter(people=people,user_group=group)

@login_required(login_url="/login/")
def leaders_selling_list(request,people,group):
	"""
		Here,we will get People Ordered Product List Bassed On  Group and People.
		action:{GET}
		URL :{domainname}/groups/api/v1/leaders-sell-list/{people}/{group}
	"""
	info_data = []
	query_set = get_leaders_selling_list_queryset(people,group)
	if query_set:
		info_data = query_set.first()
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_harvest_date','create_date','last_modified')
	leaders_selling_list_data = ProductsellingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/leaders/sellinglist.html/", {'leaders_selling_list_data': leaders_selling_list_data,'info_data':info_data})  


def getUserLeaderPeople(request):
	model_query = Userleaders.objects.filter(leader=request.user.id).values('id','user')
	query_set = [i['user'] for i in get_leader_list_queryset(model_query)]
	if request.user.id not in query_set:
		query_set.append(request.user.id)
	return query_set

from django.db.models.query import QuerySet
from django.db.models import Count
@login_required(login_url="/login/")
def getGroupByProductBuyList(request):
	"""
		HERE,we can get the details of People Ordered Details By Product and Date.
		URL:{domainname}/groups/view/product-buy-list/
	"""
	people_list = [p.people_id for p in UserPeople.objects.filter(user__in=getUserLeaderPeople(request))]
	queryset = Productbuyingdetails.objects.filter(people__in=people_list)#.values('product_name','create_date').annotate(dcount=Count('create_date'))	
	group_by_result = queryset.values('product_name','create_date').annotate(dcount=Count('create_date'))
	results = []
	for r in group_by_result:
		for q in queryset:
			if q.product_name == r['product_name']:
				r['product_image'] = q.product_image
				break
		r['create_date'] = r['create_date'].strftime('%Y-%m-%d')
		results.append(r)
	data = BuyProductListTable(results)
	return render(request, "app/dist/html/table/product_list.html/", {'data': data})  

@login_required(login_url="/login/")
def getGroupByProductSellList(request):
	"""
		HERE,we can get the details of People Produced Details By Product and Date.
		URL:{domainname}/groups/view/product-sell-list/
	"""
	people_list = [p.people_id for p in UserPeople.objects.filter(user__in=getUserLeaderPeople(request))]	
	queryset = Productsellingdetails.objects.filter(people__in=people_list)
	group_by_result = queryset.values('product_name','create_date').annotate(dcount=Count('create_date'))
	results = []
	for r in group_by_result:
		for q in queryset:
			if q.product_name == r['product_name']:
				r['product_image'] = q.product_image
				break
		r['create_date'] = r['create_date'].strftime('%Y-%m-%d')
		results.append(r)
	data = SellProductListTable(results)
	return render(request, "app/dist/html/table/product_sell_list.html/", {'data': data})  

# query = Productsellingdetails.objects.filter(people__in=people_list).query
# query.group_by = ['create_date','product_name']
# results = QuerySet(query=query, model=Productsellingdetails).order_by('-create_date').values('product_name','create_date')

@login_required(login_url="/login/")
def getPeopleBuyProductList(request,product,date):
	"""
		URL:{domainname}/groups/view/people-product-buy-list/{product}/{date}
	"""
	str_date = date
	date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	query_set = Productbuyingdetails.objects.filter(product_image=product,create_date=date)
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_required_date','create_date','last_modified')
	data = ProductbuyingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/people_product_buy_list.html/", {'data': data,'info_data':query_set_values,'get':{'product':product,'date':str_date}})

@login_required(login_url="/login/")
def getPeopleSellProductList(request,product,date):
	"""
		URL:{domainname}/groups/view/people-product-sell-list/{product}/{date}
	"""
	str_date = date
	date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	query_set = Productsellingdetails.objects.filter(product_image=product,create_date=date)
	query_set_values = query_set.values('people__first_name','product_name','product_qty','product_price','measurement','product_harvest_date','create_date','last_modified')
	data = ProductsellingdetailsTable(query_set_values)
	return render(request, "app/dist/html/table/people_product_sell_list.html/", {'data': data,'info_data':query_set_values,'get':{'product':product,'date':str_date}})

