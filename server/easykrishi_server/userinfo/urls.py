from django.conf.urls import url
from userinfo.api_views.views import *

urlpatterns = [
			#url(r'^access-token/$', AccessTokenGenerate.as_view(),name='Access Token Generate'),
			url(r'^otp-create/$', OtpDetails.as_view(),name='Otp Details Creation'),
			url(r'^user-create/$', UserCreateView.as_view(),name='User Create'),
			url(r'^user-update/(?P<pk>\d+)/$', UserUpdateView.as_view(),name='user-update-view'),
			url(r'^user-people-create/$', PeopleCreateView.as_view(),name='user-people-create-view'),
			url(r'^user-people-update/(?P<pk>\d+)/$', PeopleDataUpdateView.as_view(),name='user-people-update-view'),
			url(r'^user-people-list/$', UserContactList.as_view(),name='user-people-list-view'),
			url(r'^leaders-list/$', GetLeadersListView.as_view(),name='leaders-list-view'),
			url(r'^user-leader-update/$', ChangeLeaderView.as_view(),name='user-leader-update'),
			url(r'^people-form-details-update/$',PeopleFormUpdateView.as_view(),name='people-form-details-update-view'),
			url(r'^other-details-list/(?P<people>\d+)/$', getOtherInfoList.as_view(),name='other-details-list-view'),
]


"""
	Template Views 
"""
from userinfo.template_views.views import *
urlpatterns += [
			url(r'^home/$', DashboardView,name='Dashboard  View'),
			url(r'^people-list/$', people_contact_list),			
			url(r'^people-choose-list/(?P<people>\d+)/$', PeopleChooseList.as_view(),name='people choose View'),
			url(r'^people-ordered-list/(?P<people>\d+)/$', people_order_list),
			url(r'^people-sell-list/(?P<people>\d+)/$', people_selling_list),
			url(r'^download/$',download_xlsx_file),
			url(r'^hierarchical_details/$',find_people_hierarchical_details),

			url(r'^exportOrders/(?P<val>[\w\-]+)/(?P<product>[\w\-]+)/(?P<date>[\w\-]+)/$', exportOrders,name='exportOrders-list'),
]
"""
Synchronizing Urls
"""
urlpatterns += [
			
			url(r'^people-sync-view/$', UserPeopleSynchronization.as_view(),name='people-synchronizarion'),
			url(r'^form-sync-view/$', FormSyncView.as_view(),name='form-sync-view'),			
]

"""
	Password Related Views
"""
urlpatterns += [			
			url(r'^change-password/$', ChangePasswordView,name='change-password'),
			url(r'^reset-password/$', resetPasswordView,name='reset-password'),			
]



