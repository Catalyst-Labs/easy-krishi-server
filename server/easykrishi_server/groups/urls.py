from django.conf.urls import url
from groups.api_views.views import *

urlpatterns = [
			url(r'^user-group-create/$', UserGroupCreateView.as_view(),name='user-group-create '),			
			url(r'^user-group-update/(?P<pk>\d+)/$', UserGroupUpdateView.as_view(),name='user-update-view'),
			url(r'^user-group-list-count/$', UserGroupListView.as_view(),name='user-group-list-count-view'),
			url(r'^group-members-list/(?P<group>\d+)/$', GroupMembersListview.as_view(),name='group-members-list-view'),			
			url(r'^add-remove-member/$', AddorMembersToGroup.as_view(),name='add-remove-member-view'),
]

"""
	Product Related Url's
"""
urlpatterns += [
			url(r'^buy-product-create/$', AddProductbuyingdetailsView.as_view(),name='buy-product-create-view'),
			url(r'^buy-product-update/(?P<pk>\d+)/$', ProductbuyingdetailsUpdateView.as_view(),name='buy-product-update-view'),
			url(r'^buy-product-list/(?P<people>\d+)/(?P<usergroup>\d+)/$', ProductbuyingdetailsListView.as_view(),name='buy-product-create-view'),

			url(r'^contact-buy-product-list/(?P<people>\d+)/$', ContactProductbuyingdetailsListView.as_view(),name='contact-buy-product-create-view'),

			url(r'^sell-product-create/$', AddProductsellingdetailsView.as_view(),name='sell-product-create-view'),
			url(r'^sell-product-update/(?P<pk>\d+)/$', ProductsellingdetailsUpdateView.as_view(),name='sell-product-update-view'),
			url(r'^sell-product-list/(?P<people>\d+)/(?P<usergroup>\d+)/$', ProductsellingdetailsListView.as_view(),name='sell-product-list-view'),

			url(r'^contact-sell-product-list/(?P<people>\d+)/$', ContactProductsellingdetailsListView.as_view(),name='contact-sell-product-list-view'),
			url(r'^user-full-data/$', GetUserFullData.as_view(),name='user-full-data-view'),
			
]

"""
	Template Views 
"""
from groups.template_views.views import *
urlpatterns += [
			url(r'^choose-list/(?P<people>\d+)/(?P<group>\d+)/$', TChooseList.as_view(),name='choose View'),
			url(r'^group-list/$',groups_list,name='User Group List Template View'),
			url(r'^members-list/(?P<group>\d+)/$',groups_member_list,name='group-members-list-view'),
			url(r'^user-ordered-list/(?P<people>\d+)/(?P<group>\d+)/$', group_order_list),
			url(r'^user-sell-list/(?P<people>\d+)/(?P<group>\d+)/$', group_selling_list),
			url(r'^leaders-list/$', leader_list,name='group-leaders-list-view'),
			url(r'^leaders-group-list/(?P<leader>\d+)/$',leader_group_list,name='leaders Group List Template View'),
			url(r'^leaders-members-list/(?P<group>\d+)/$', leader_group_member_list,name='leaders-members-list-view'),
			url(r'^leaders-choose-list/(?P<people>\d+)/(?P<group>\d+)/$', TLeaderChooseList.as_view(),name='leaders-member_schoose_view'),
			url(r'^leaders-ordered-list/(?P<people>\d+)/(?P<group>\d+)/$', leaders_order_list),
			url(r'^leaders-sell-list/(?P<people>\d+)/(?P<group>\d+)/$', leaders_selling_list),
			url(r'^product-buy-list/$',getGroupByProductBuyList,name='user-product-buy-list-view'),
			url(r'^product-sell-list/$',getGroupByProductSellList,name='user-product-sell-list-view'),
			url(r'^people-product-buy-list/(?P<product>[\w\-]+)/(?P<date>[\w\-]+)/$', getPeopleBuyProductList,name='people-product-buy-list'),
			url(r'^people-product-sell-list/(?P<product>[\w\-]+)/(?P<date>[\w\-]+)/$', getPeopleSellProductList,name='people-product-sell-list'),
]

"""
	Groups Synchronization Views
"""
urlpatterns += [
				url(r'^groups-sync-view/$', GroupsAndMembers.as_view(),name='groups-sync-view'),
				url(r'^buy-edit-list/$', productEditBuyList.as_view(),name='buy-edit-list-view'),	
				url(r'^sell-edit-list/$', productEditSellList.as_view(),name='sell-edit-list-view'),		
]


