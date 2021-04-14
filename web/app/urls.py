# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('test', views.test, name='test'),

    path('overview', views.overview, name='overview'),

    path('dns', views.dns, name='dns'),
    path('device', views.device, name='device'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
