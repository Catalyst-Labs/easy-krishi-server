from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
	list_display = ('name','create_by','created_date','last_modified')
	pass
@admin.register(Groupmember)
class GroupmemberAdmin(admin.ModelAdmin):
	list_display = ('user_group','name','member','create_by','created_date','last_modified')
	pass
@admin.register(Productbuyingdetails)
class ProductbuyingdetailsAdmin(admin.ModelAdmin):
	list_display = ('product_name','user','people','product_qty','measurement','product_price','product_required_date','create_date','last_modified')
	pass
@admin.register(Productsellingdetails)
class ProductsellingdetailsAdmin(admin.ModelAdmin):
	list_display = ('product_name','user','people','product_qty','measurement','product_price','product_harvest_date','create_date','last_modified')
	pass

