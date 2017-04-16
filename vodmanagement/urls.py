from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from . import views
urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^$',views.homepage,name='homepage'),
    url(r'^gallery/$',views.gallery,name='gallery'),
    url(r'^list/$',views.listing,name='list'),
]