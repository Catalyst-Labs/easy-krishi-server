from userinfo.models import *
from groups.models import *
from table import Table
from table.columns import Column
from table.columns import LinkColumn, Link,ImageLink
from table.columns import CheckboxColumn
from table.utils import A
from userinfo.template_views import *

class UserPeopleTable(Table):

	people__first_name = LinkColumn(field='people__first_name',header=u'Name', links=[Link(text=A('people__first_name'), viewname='people choose View', args=(A('people_id',),))], header_attrs={'width':'20%'})
	people__last_name = Column(field='people__last_name', header=u'Last Name', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	user__mobile_number = Column(field='people__mobile_number', header=u'Mobile Number', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	user__aadhar_number = Column(field='people__aadhar_number', header=u'Aadhar Number', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__house_number = Column(field='people__house_number', header=u'House Number', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__village = Column(field='people__village', header=u'Village', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__sub_district_or_mandal = Column(field='people__sub_district_or_mandal', header=u'Mandal', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__district = Column(field='people__district', header=u'District', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__city_name = Column(field='people__city_name', header=u'City Name', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__state_name = Column(field='people__state_name', header=u'State Name', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	people__pincode = Column(field='people__pincode', header=u'Pincode', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	created_date = Column(field='created_date', header=u'Created Date', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	date_modified = Column(field='date_modified', header=u'Last Modified Date', attrs={'class': 'custom'}, header_attrs={'width':'20%'})
	class Meta:
		model = UserPeople
		info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"
		sort = [(0, 'asc'), (1, 'desc')]
		pagination = True



class ProductbuyingdetailsTable(Table):

	people__first_name = Column(field='people__first_name', header=u'Member Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_qty = Column(field='product_qty', header=u'Product Quantity', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_measurement = Column(field='measurement', header=u'Product Measurement', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_price = Column(field='product_price', header=u'Product Price', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	product_required_date = Column(field='product_required_date', header=u'Required Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	model = Productbuyingdetails
	info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"	


class ProductsellingdetailsTable(Table):

	people__first_name = Column(field='people__first_name', header=u'Member Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_name = Column(field='product_name', header=u'Product Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_qty = Column(field='product_qty', header=u'Product Quantity', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_measurement = Column(field='measurement', header=u'Product Measurement', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	product_price = Column(field='product_price', header=u'Product Price', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	product_harvest_date = Column(field='product_harvest_date', header=u'Available Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	model = Productsellingdetails
	info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"		

class UserGroupTable(Table):

	name = Column(field='name', header=u'Member Name', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	create_date = Column(field='create_date', header=u'Added Date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})
	last_modified = Column(field='last_modified', header=u'Last Modified date', attrs={'class': 'custom'}, header_attrs={'width': '1%'})	
	model = Productsellingdetails
	info_format = u"Total: _TOTAL_  First: _START_  Last: _END_"