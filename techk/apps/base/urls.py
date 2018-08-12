from django.conf.urls import url
from apps.base import views

urlpatterns = [
    url(r'^books/$', views.book_list),
    url(r'^books/(?P<id>[0-9]+)/$', views.book_detail),
    url(r'^categories/$', views.category_list),
    url(r'^categories/(?P<id>[0-9]+)/$', views.category_detail),
]