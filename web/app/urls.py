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

    path('dns2', views.dns, name='dns2'),

    path('dns', views.dns_dashboard, name='dns'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
