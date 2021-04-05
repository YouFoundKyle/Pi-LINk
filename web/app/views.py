# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
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

def explorer(request):
    context = {}
    context['segment'] = 'explorer'
    
    temp_json = requests.get('http://192.168.1.123:9090/api/v1/query_range?query=temperature&start=1616993300&end=1617166100&step=20s').json()
    temp_values = dict(temp_json['data']['result'][0]['values'])
    temp_values = {datetime.utcfromtimestamp(key).strftime('%Y-%m-%d %H:%M:%S'): value for key, value in temp_values.items()}
    
    paginator = Paginator(tuple(temp_values.items()), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['temperature'] = page_obj

    html_template = loader.get_template('explorer.html')
    return HttpResponse(html_template.render(context, request))
