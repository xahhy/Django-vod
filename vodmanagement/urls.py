from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from . import views
urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^$',views.listing,name='homepage'),
    url(r'^gallery/$',views.gallery,name='gallery'),
    url(r'^list/$',views.listing,name='list'),
    url(r'^list/(?P<slug>[\w-]+)/$',views.listing,name='list-detail'),
    url(r'^(?P<slug>[\w-]+)/$',views.vod_detail, name='vod-detail'),
    url(r'^listlink/$',views.listinglink,name='listlink'),
]