# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

<<<<<<< HEAD
=======
    path('test', views.test, name='test'),

>>>>>>> daa2dc75db70d263e520af5f6066ef8f442c1638
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
