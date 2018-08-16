from django.conf.urls import url
from django.views.generic import TemplateView

from apps.base import views

urlpatterns = [
	url(r'^api/books/$', views.book_list),
	url(r'^api/categories/(?P<id>[0-9]+)/books/', views.book_list),
	url(r'^api/books/(?P<id>[0-9]+)/$', views.book_detail),
	url(r'^api/categories/$', views.category_list),
	url(r'^api/categories/(?P<id>[0-9]+)/$', views.category_detail),
	url(r'^api/scraper/$', views.scrape_list),
	url(r'^$', TemplateView.as_view(template_name='index.html'))
]