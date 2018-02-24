from userinfo.models import *
from groups.models import *
from table import Table
from table.columns import Column
from table.columns import LinkColumn, Link,ImageLink
from table.columns import CheckboxColumn
from table.utils import A
from userinfo.template_views import *

class UserGroupTable(Table):

	name = LinkColumn(field='name',header=u'Name', links=[Link(text=A('name'), viewname='group-members-list-view', args=(A('id',),))], header_attrs={'width': '1%'})
	created_date = Column(field='created_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	class Meta:
		model = UserGroup
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"

# class GroupmemberTable(Table):
# 	member__first_name = LinkColumn(field='member__first_name',header=u'Member Name', links=[Link(text=A('member__first_name'), viewname='choose View', args=(A('member_id',),A('user_group_id',),))])
# 	user_group__name = Column(field='user_group__name', header=u'Group Name', attrs={'class': 'custom'})
# 	member__mobile_number = Column(field='member__mobile_number', header=u'Mobile Number', attrs={'class': 'custom'})
# 	member__aadhar_number = Column(field='member__aadhar_number', header=u'QR Code', attrs={'class': 'custom'})
# 	created_date = Column(field='created_date', header=u'Added Date', attrs={'class': 'custom'})
# 	class Meta:
# 		model = Groupmember
# 		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"

class ProductbuyingdetailsTable(Table):
	people__first_name = Column(field='people__first_name', header=u'Member Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_qty = Column(field='product_qty', header=u'Product Quantity', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_measurement = Column(field='measurement', header=u'Product Measurement', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_price = Column(field='product_price', header=u'Product Price', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_required_date = Column(field='product_required_date', header=u'Required Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	class Meta:
		model = Productbuyingdetails
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"

class BuyProductListTable(Table):
	product_name = LinkColumn(field='product_name',header=u'Product Name',header_attrs={'width': '1%'}, links=[Link(text=A('product_name'), viewname='people-product-buy-list', args=(A('product_image',),A('create_date',),))])
	#product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '10px'})	
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	dcount = Column(field='dcount', header=u'Count', attrs={'class': 'custom'}, header_attrs={'width': '1%'})


class SellProductListTable(Table):
	product_name = LinkColumn(field='product_name',header=u'Product Name',header_attrs={'width': '1%'}, links=[Link(text=A('product_name'), viewname='people-product-sell-list', args=(A('product_image',),A('create_date',),))])
	#product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	dcount = Column(field='dcount', header=u'Count', attrs={'class': 'custom'}, header_attrs={'width': '1%'})



class ProductsellingdetailsTable(Table):

	people__first_name = Column(field='people__first_name', header=u'Member Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_qty = Column(field='product_qty', header=u'Product Quantity', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_measurement = Column(field='measurement', header=u'Product Measurement', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_price = Column(field='product_price', header=u'Product Price', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	product_harvest_date = Column(field='product_harvest_date', header=u'Available Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	class Meta:
		model = Productsellingdetails
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"		


class UserleadersTable(Table):
#'leader__name','user__mobile_number','user__aadhar_number','create_date','last_modified'
	user__name = LinkColumn(field='user__name',header=u'Member Name', links=[Link(text=A('user__name'), viewname='leaders Group List Template View', args=(A('user_id',),))])
	user__mobile_number = Column(field='user__mobile_number', header=u'Mobile Number', attrs={'class': 'custom'})
	user__aadhar_number = Column(field='user__aadhar_number', header=u'QR Code', attrs={'class': 'custom'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'})
	class Meta:
		model = Userleaders
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"


class UserGroupLeaderTable(Table):
	name = LinkColumn(field='name',header=u'Group Name', links=[Link(text=A('name'), viewname='leaders-members-list-view', args=(A('id',),))])
	created_date = Column(field='created_date', header=u'Created Date', attrs={'class': 'custom'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'})
	class Meta:
		model = UserGroup
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"

class GroupmemberLeaderTable(Table):
	member__first_name = LinkColumn(field='member__first_name',header=u'Member Name', links=[Link(text=A('member__first_name'), viewname='leaders-member_schoose_view', args=(A('member_id',),A('user_group_id',),))])
	#member__first_name = Column(field='member__first_name', header=u'Member Name', attrs={'class': 'custom'})
	user_group__name = Column(field='user_group__name', header=u'Group Name', attrs={'class': 'custom'})
	member__mobile_number = Column(field='member__mobile_number', header=u'Mobile Number', attrs={'class': 'custom'})
	member__aadhar_number = Column(field='member__aadhar_number', header=u'QR Code', attrs={'class': 'custom'})
	created_date = Column(field='created_date', header=u'Added Date', attrs={'class': 'custom'})
	class Meta:
		model = Groupmember
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"


class GroupmemberTable(Table):
	member__first_name = LinkColumn(field='member__first_name',header=u'Member Name', links=[Link(text=A('member__first_name'), viewname='choose View', args=(A('member_id',),A('user_group_id',),))])
	member__last_name = Column(field='member__last_name', header=u'Last Name')
	member__latitude = Column(field='member__latitude', header=u'Latitude')
	member__longitude = Column(field='member__longitude', header=u'Longitude')
	member__house_number = Column(field='member__house_number', header=u'House Number')
	member__village = Column(field='member__village', header=u'Village')
	member__sub_district_or_mandal = Column(field='member__sub_district_or_mandal', header=u'Mandal')
	member__district = Column(field='member__district', header=u'District')
	member__city_name = Column(field='member__city_name', header=u'City Name')
	member__state_name = Column(field='member__state_name', header=u'State Name')
	member__country_name = Column(field='member__country_name', header=u'Country Name')
	member__pincode = Column(field='member__pincode', header=u'Pincode')
	user_group__name = Column(field='user_group__name', header=u'Group Name')
	member__mobile_number = Column(field='member__mobile_number', header=u'Mobile Number')
	member__aadhar_number = Column(field='member__aadhar_number', header=u'QR Code')
	created_date = Column(field='created_date', header=u'Added Date')
	class Meta:
		model = Groupmember
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"

