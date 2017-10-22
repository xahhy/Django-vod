from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.cache import cache_page

from .views import *
cache_time = 1
urlpatterns = [
    url(r'^$', cache_page(cache_time)(VodListAPIView.as_view()), name='list'),
    url(r'^home/$', cache_page(cache_time)(HomeListAPIView.as_view()), name='home'),
    # url(r'^category/$', cache_page(60)(CategoryListAPIView.as_view()), name='category'),
    url(r'^category/$', cache_page(cache_time)(CategoryListAPIView.as_view()), name='category'),
    url(r'^year/$', cache_page(cache_time)(YearListAPIView.as_view()), name='year'),
    url(r'^region/$', cache_page(cache_time)(RegionListAPIView.as_view()), name='region'),
    url(r'^record/$', cache_page(cache_time)(RecordListAPIView.as_view()), name='record'),
    # url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>[\w-]+)/$', VodDetailAPIView.as_view(), name='detail'),

    # url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),

]
