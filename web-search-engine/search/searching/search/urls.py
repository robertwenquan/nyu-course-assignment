from django.conf.urls import url

from . import search

urlpatterns = [
  url(r'^$', search.view, name='view'),
  url(r'^search$', search.result, name='result'),
]

