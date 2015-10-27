from django.conf.urls import url

from . import search

urlpatterns = [
  url(r'^$', search.view, name='view'),
]

