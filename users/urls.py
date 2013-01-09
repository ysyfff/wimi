from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from users import views

urlpatterns = patterns('',
    #before  a user ogged in and a user logged out
    url(r'^login/$', views.sblogin),
    url(r'^logout/$', views.sblogout),
    url(r'^register/$', views.sbregister),

    #
    url(r'^(?P<user_id>\d+)/info/$', views.myinfo),
    url(r'^(?P<user_id>\d+)/mdfinfo/$', views.mdfinfo),
    url(r'^(?P<user_id>\d+)/mdfpwd/$', views.mdfpwd),
)
