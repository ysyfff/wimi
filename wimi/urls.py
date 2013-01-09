from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from users import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^users/', include('users.urls')),
    url(r'^shops/', include('shops.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
