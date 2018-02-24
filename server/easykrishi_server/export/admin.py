from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib.admin import helpers, validation, widgets
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import string_concat, ugettext as _, ungettext
from django.db.models import Count
from django.contrib.admin.utils import (NestedObjects, flatten_fieldsets, get_deleted_objects,lookup_needs_distinct, model_format_dict, quote, unquote,)
import pdb
import datetime


@admin.register(OrderedProducts)
class ProductsellingdetailsAdmin(admin.ModelAdmin):
	list_display = ('product_name','create_date')
	enable_change_view = False
	#actions = [export_as_csv_action("CSV Export", fields=['id'])]
	
	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request):
		return False

	def changelist_view(self, request, extra_context=None):
		"""
		The 'change list' admin view for this model.
		"""
		opts = self.model._meta
		app_label = opts.app_label		

		list_display = self.get_list_display(request)
		list_display_links = self.get_list_display_links(request, list_display)
		list_filter = self.get_list_filter(request)
		search_fields = self.get_search_fields(request)

		# Check actions to see if any are available on this changelist
		actions = self.get_actions(request)
		# if actions:
		# 	# Add the action checkboxes if there are any actions available.
		# 	list_display = ['action_checkbox'] + list(list_display)

		ChangeList = self.get_changelist(request)
		try:
			cl = ChangeList(request, self.model, list_display,list_display_links, list_filter, self.date_hierarchy,search_fields, self.list_select_related, self.list_per_page,self.list_max_show_all, self.list_editable, self)		
		except IncorrectLookupParameters:			
			if ERROR_FLAG in request.GET.keys():
				return SimpleTemplateResponse('admin/invalid_setup.html', {
					'title': _('Database error'),
				})
			return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

		formset = cl.formset = None
		media = []
		action_form = None		
		queryset = Productbuyingdetails.objects.all()
		group_by_result = queryset.values('product_name','create_date').annotate(dcount=Count('product_name'))
				
		for r in group_by_result:
			for q in queryset:
				if q.product_name == r['product_name'] and q.create_date == r['create_date']:
					r['product_image'] = q.product_image
					r['id'] = q.id
				continue
			r['create_date_st'] = r['create_date'].strftime('%Y-%m-%d')

		cl.result_list = group_by_result
		cl.result_count = len(group_by_result)
		
		selection_note_all = ungettext('%(total_count)s selected',
			'All %(total_count)s selected', cl.result_count)

		context = dict(
			self.admin_site.each_context(request),
			module_name=force_text(opts.verbose_name_plural),
			selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
			selection_note_all=selection_note_all % {'total_count': cl.result_list},
			title=cl.title,
			is_popup=cl.is_popup,
			to_field=cl.to_field,
			cl=cl,
			media=media,
			list_display=self.get_list_display(request),
			has_add_permission=self.has_add_permission(request),
			opts=cl.opts,
			action_form=action_form,
			actions_on_top=self.actions_on_top,
			actions_on_bottom=self.actions_on_bottom,
			actions_selection_counter=self.actions_selection_counter,
			preserved_filters=self.get_preserved_filters(request),
		)
		
		context.update(extra_context or {})
		request.current_app = self.admin_site.name		

		return TemplateResponse(request, self.change_list_template or [
			'admin/%s/%s/product_buy_list.html' % (app_label, opts.model_name),
			'admin/%s/product_buy_list.html' % app_label,
			'admin/product_buy_list.html'
		], context)
	pass

	def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
		opts = self.model._meta
		app_label = opts.app_label
		IS_POPUP_VAR = '_popup'
		TO_FIELD_VAR = '_to_field'
		to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
		obj = self.get_object(request, unquote(object_id), to_field)

		list_display = ('product_name','user','people','product_qty','measurement','product_price','product_required_date','create_date','last_modified')
		list_display_links = None#self.get_list_display_links(request, list_display)
		list_filter = self.get_list_filter(request)
		search_fields = self.get_search_fields(request)

		# Check actions to see if any are available on this changelist
		actions = self.get_actions(request)		
		# if actions:
		# 	# Add the action checkboxes if there are any actions available.
		# 	list_display = ['action_checkbox'] + list(list_display)

		ChangeList = self.get_changelist(request)
		try:
			cl = ChangeList(request, self.model, list_display,list_display_links, list_filter, self.date_hierarchy,search_fields, self.list_select_related, self.list_per_page,self.list_max_show_all, self.list_editable, self)		
		except IncorrectLookupParameters:			
			if ERROR_FLAG in request.GET.keys():
				return SimpleTemplateResponse('admin/invalid_setup.html', {
					'title': _('Database error'),
				})
			return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

		formset = cl.formset = None
		media = []
		if actions:
			action_form = self.action_form(auto_id=None)
			action_form.fields['action'].choices = self.get_action_choices(request)
		else:
			action_form = None

		action_form.fields['action'].choices.pop(1)	
		cl.result_list = Productbuyingdetails.objects.filter(product_name=obj.product_name,create_date=obj.create_date)
		 
		cl.result_count = len(cl.result_list)
		
		selection_note_all = ungettext('%(total_count)s selected',
			'All %(total_count)s selected', cl.result_count)

		context = dict(
			self.admin_site.each_context(request),
			module_name=force_text(opts.verbose_name_plural),
			selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
			selection_note_all=selection_note_all % {'total_count': cl.result_list},
			title=cl.title,
			is_popup=cl.is_popup,
			to_field=cl.to_field,
			cl=cl,
			export_url = "/user/view/exportOrders/1/"+str(obj.product_image)+"/"+(obj.create_date).strftime('%Y-%m-%d'),
			media=media,
			list_display=self.get_list_display(request),
			has_add_permission=self.has_add_permission(request),
			opts=cl.opts,
			action_form=action_form,
			actions_on_top=self.actions_on_top,
			actions_on_bottom=self.actions_on_bottom,
			actions_selection_counter=self.actions_selection_counter,
			preserved_filters=self.get_preserved_filters(request),
		)
		
		context.update(extra_context or {})
		request.current_app = self.admin_site.name


		return TemplateResponse(request, self.change_list_template or [
			'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
			'admin/%s/change_list.html' % app_label,
			'admin/change_list.html'
		], context)
	pass


@admin.register(SellProducts)
class ProductsellingdetailsAdmin(admin.ModelAdmin):
	list_display = ('product_name','create_date')
	enable_change_view = False

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request):
		return False



	def changelist_view(self, request, extra_context=None):
		"""
		The 'change list' admin view for this model.
		"""
		opts = self.model._meta
		app_label = opts.app_label		

		list_display = self.get_list_display(request)
		list_display_links = self.get_list_display_links(request, list_display)
		list_filter = self.get_list_filter(request)
		search_fields = self.get_search_fields(request)

		# Check actions to see if any are available on this changelist
		actions = self.get_actions(request)		
		ChangeList = self.get_changelist(request)
		try:
			cl = ChangeList(request, self.model, list_display,list_display_links, list_filter, self.date_hierarchy,search_fields, self.list_select_related, self.list_per_page,self.list_max_show_all, self.list_editable, self)		
		except IncorrectLookupParameters:			
			if ERROR_FLAG in request.GET.keys():
				return SimpleTemplateResponse('admin/invalid_setup.html', {
					'title': _('Database error'),
				})
			return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

		formset = cl.formset = None
		media = []
		action_form = None		
		queryset = Productsellingdetails.objects.all()
		group_by_result = queryset.values('product_name','create_date').annotate(dcount=Count('product_name'))
				
		for r in group_by_result:
			for q in queryset:
				if q.product_name == r['product_name'] and q.create_date == r['create_date']:
					r['product_image'] = q.product_image
					r['id'] = q.id
				continue
			r['create_date_st'] = r['create_date'].strftime('%Y-%m-%d')

		cl.result_list = group_by_result
		cl.result_count = len(group_by_result)
		
		selection_note_all = ungettext('%(total_count)s selected',
			'All %(total_count)s selected', cl.result_count)

		context = dict(
			self.admin_site.each_context(request),
			module_name=force_text(opts.verbose_name_plural),
			selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
			selection_note_all=selection_note_all % {'total_count': cl.result_list},
			title=cl.title,
			is_popup=cl.is_popup,
			to_field=cl.to_field,
			cl=cl,
			media=media,
			list_display=self.get_list_display(request),
			has_add_permission=self.has_add_permission(request),
			opts=cl.opts,
			action_form=action_form,
			actions_on_top=self.actions_on_top,
			actions_on_bottom=self.actions_on_bottom,
			actions_selection_counter=self.actions_selection_counter,
			preserved_filters=self.get_preserved_filters(request),
		)
		
		context.update(extra_context or {})
		request.current_app = self.admin_site.name

		return TemplateResponse(request, self.change_list_template or [
			'admin/%s/%s/product_buy_list.html' % (app_label, opts.model_name),
			'admin/%s/product_buy_list.html' % app_label,
			'admin/product_buy_list.html'
		], context)
	pass

	def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
		opts = self.model._meta
		app_label = opts.app_label
		IS_POPUP_VAR = '_popup'
		TO_FIELD_VAR = '_to_field'
		to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
		obj = self.get_object(request, unquote(object_id), to_field)

		list_display = ('product_name','user','people','product_qty','measurement','product_price','product_harvest_date','create_date','last_modified')
		list_display_links = None#self.get_list_display_links(request, list_display)
		list_filter = self.get_list_filter(request)
		search_fields = self.get_search_fields(request)

		# Check actions to see if any are available on this changelist
		actions = self.get_actions(request)		
		# if actions:
		# 	# Add the action checkboxes if there are any actions available.
		# 	list_display = ['action_checkbox'] + list(list_display)

		ChangeList = self.get_changelist(request)
		try:
			cl = ChangeList(request, self.model, list_display,list_display_links, list_filter, self.date_hierarchy,search_fields, self.list_select_related, self.list_per_page,self.list_max_show_all, self.list_editable, self)		
		except IncorrectLookupParameters:			
			if ERROR_FLAG in request.GET.keys():
				return SimpleTemplateResponse('admin/invalid_setup.html', {
					'title': _('Database error'),
				})
			return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

		formset = cl.formset = None
		media = []
		action_form = None		
		cl.result_list = Productsellingdetails.objects.filter(product_name=obj.product_name,create_date=obj.create_date)
		 
		cl.result_count = len(cl.result_list)
		
		selection_note_all = ungettext('%(total_count)s selected',
			'All %(total_count)s selected', cl.result_count)

		context = dict(
			self.admin_site.each_context(request),
			module_name=force_text(opts.verbose_name_plural),
			selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
			selection_note_all=selection_note_all % {'total_count': cl.result_list},
			title=cl.title,
			is_popup=cl.is_popup,
			to_field=cl.to_field,
			cl=cl,
			media=media,
			export_url = "/user/view/exportOrders/2/"+str(obj.product_image)+"/"+(obj.create_date).strftime('%Y-%m-%d'),
			list_display=self.get_list_display(request),
			has_add_permission=self.has_add_permission(request),
			opts=cl.opts,
			action_form=action_form,
			actions_on_top=self.actions_on_top,
			actions_on_bottom=self.actions_on_bottom,
			actions_selection_counter=self.actions_selection_counter,
			preserved_filters=self.get_preserved_filters(request),
		)
		
		context.update(extra_context or {})
		request.current_app = self.admin_site.name

		return TemplateResponse(request, self.change_list_template or [
			'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
			'admin/%s/change_list.html' % app_label,
			'admin/change_list.html'
		], context)
	pass
