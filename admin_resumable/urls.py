from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_resumable/$', views.admin_resumable, name='admin_resumable'),
    url(r'^admin_resumable_restore/$', views.admin_resumable_restore, name='admin_resumable_restore'),
    url(r'^admin_resumable_set/$', views.admin_resumable_set, name='admin_resumable_set'),
    url(r'^admin_resumable_delete/$', views.admin_resumable_delete, name='admin_resumable_delete'),
]
