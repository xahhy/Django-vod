from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import (
    VodListAPIView, HomeListAPIView, HomeOverViewAPIView,CategoryListAPIView,
    YearListAPIView, RegionListAPIView, VodDetailAPIView
)


cache_time = 10
urlpatterns = [
    url(r'^$', cache_page(cache_time)(VodListAPIView.as_view()), name='list'),
    url(r'^home/$', cache_page(cache_time)(HomeListAPIView.as_view()), name='home'),
    url(r'^home/overview$', cache_page(cache_time)(HomeOverViewAPIView.as_view()), name='home_overview'),
    url(r'^category/$', cache_page(cache_time)(CategoryListAPIView.as_view()), name='category'),
    url(r'^year/$', cache_page(cache_time)(YearListAPIView.as_view()), name='year'),
    url(r'^region/$', cache_page(cache_time)(RegionListAPIView.as_view()), name='region'),
    url(r'^(?P<id>[\w-]+)/$', cache_page(cache_time)(VodDetailAPIView.as_view()), name='detail'),
]
