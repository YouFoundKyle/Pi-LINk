# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    path('explorer', views.explorer, name='explorer'),

    # The home page
    path('', views.index, name='home'),

    path('mqtt_overview', views.mqtt_overview, name='mqtt_overview'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
