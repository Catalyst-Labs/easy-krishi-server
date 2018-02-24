from django.contrib import admin
from .models import *
# Register your models here.
import pdb

class FormKeysInformationInline(admin.TabularInline):
	fields = ('key',)
	model = FormKeysInformation
	extra = 0	

class FormsInformationAdmin(admin.ModelAdmin):
	inlines = (FormKeysInformationInline, )
	list_display = ('title', 'create_by','create_date','last_modified')
	fields = ('title',)
	
	def save_model(self, request, obj, form, change):		
		obj.create_by = request.user
		obj.save()

	def save_formset(self, request, form, formset, change):		
		if formset.model == FormKeysInformation:
			instances = formset.save(commit=False)
			for instance in instances:
				instance.create_by = request.user
				instance.save()
		else:
			formset.save()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('mobile_number','aadhar_number','first_name','date_joined','last_modified','is_active')

@admin.register(Userleaders)
class UserLeadersAdmin(admin.ModelAdmin):
	list_display = ('user','leader','create_date','last_modified')

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
	list_display = ('mobile_number','aadhar_number','first_name','create_by','date_joined','last_modified')

@admin.register(PeopleKeysDetails)
class PeopleKeysDetailsAdmin(admin.ModelAdmin):
	list_display = ('people','form','value','create_by','create_date','last_modified')

@admin.register(UserPeople)
class UserPeopleAdmin(admin.ModelAdmin):
	list_display = ('nick_name','user','people','created_date','date_modified')

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
	list_display = ('create_by','device_id','model','action_method','created_date','last_modified')
admin.site.register(FormsInformation,FormsInformationAdmin)