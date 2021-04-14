# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests
import json, os


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dev_overview(request):

    context = {}
    context['segment'] = 'index'
    if os.path.exists("/etc/pilink/web/lease_DB.json"):
        with open("/etc/pilink/web/lease_DB.json") as df:
            dev_data = json.loads(df)
    context['lease_data'] = dev_data
    html_template = loader.get_template('dev_overview.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dns(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('dns_dashboard.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def test(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'chart-apex.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
