from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from shops import views

urlpatterns = patterns('',
    #shop
    url(r'^shop/$', views.shops),
    url(r'^(?P<shop_id>\d+)/shop/$', views.myshop),

    #bag
    url(r'^current/bag/$', views.badbag),
    url(r'^(?P<user_id>\d+)/current/bag/$', views.curbag),
    url(r'^(?P<user_id>\d+)/ready/bag/$', views.readybag),
    url(r'^(?P<user_id>\d+)/deal/bag/$', views.dealbag),
    url(r'^(?P<user_id>\d+)/fail/bag/$', views.failbag),
    url(r'^(?P<user_id>\d+)/today/bag/$', views.todbag),
    url(r'^(?P<user_id>\d+)/bftoday/bag/$', views.bftodbag),
    #food
    url(r'^(?P<user_id>\d+)/all/food/$', views.allfood),
    url(r'^(?P<user_id>\d+)/add/food/$', views.addfood),
    url(r'^(?P<user_id>\d+)/mdf/(?P<food_id>\d+)/food/$', views.mdffood),
)
