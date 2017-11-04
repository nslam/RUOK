from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^process/$', views.process),
    url(r'^start/$', views.start),
    url(r'^stop/$', views.stop),
]