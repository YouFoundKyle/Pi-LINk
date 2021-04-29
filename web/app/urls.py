# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    path('', views.net_overview, name='home'),

    path('explorer', views.explorer, name='explorer'),

    path('mqtt', views.mqtt_overview, name='mqtt_overview'),

    path('network', views.net_overview, name='network_overview'),

    path('dns', views.dns, name='dns'),
    
    path('device/<requested_ip>', views.device, name='device'),

    re_path(r'^.*\.*', views.pages, name='pages'),
]
