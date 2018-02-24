from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth import views


router = routers.DefaultRouter()

urlpatterns = [
    # Examples:
    # url(r'^$', 'easykrishi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^', include(admin.site.urls)),
	url(r'^admin/', include(admin.site.urls)),	
#------------------------------Common Urls For Rest Framework and Oauth2_provider --------------------------------
	#url(r'^rest-api/', include('rest_framework_docs.urls')),
	url(r'^docs/', include('rest_framework_swagger.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-docs/', include('rest_framework_docs.urls', namespace='rest_framework')),
	url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
]


from .views import loginFunction,index
urlpatterns += patterns('',
	url(r'^admin/login/$', views.login, {'template_name': 'app/index.html'}),
	url(r'^login/$', index),
	#url(r'^$', views.login, {'template_name': 'app/index.html'}),
	#url(r'^home/', TemplateView.as_view(template_name='app/home.html')),
	url(r'^admin/logout/$','django.contrib.auth.views.logout',{'template_name': 'app/index.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/'}),
	url(r'^$', loginFunction),
)



#--------------------Start of Angular URLs--------------------------------------------------------------------------#
urlpatterns += patterns('',
	
	url(r'^user/api/v1/', include('userinfo.urls')),
	url(r'^groups/api/v1/', include('groups.urls')),
	url(r'^user/view/', include('userinfo.urls')),
	url(r'^groups/view/', include('groups.urls')),	
)



