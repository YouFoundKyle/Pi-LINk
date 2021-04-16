# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests
import json

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
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


## For Explorer
yesterday = (datetime.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
today = datetime.today().strftime("%Y-%m-%d")
tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
explorer_context = {'time_sort': 'time_sort_down', 'topic_sort': None, 'metric_sort': None,
 'values_sort': None, 'tomorrow': tomorrow, 'qstart': yesterday, "qend": today, "test": None}
global last_sort
last_sort = None

def explorer(request):
    global last_sort
    context = {}
    context['segment'] = 'explorer'

    # Formatting API url
    wattPre = 'http://192.168.1.152:9090/api/v1/query_range?query=watts'
    tempPre = 'http://192.168.1.152:9090/api/v1/query_range?query=temperature'

    startDT = datetime.strptime(explorer_context['qstart'], '%Y-%m-%d')
    endDT = datetime.strptime(explorer_context['qend'], '%Y-%m-%d')
    start_utc = str(int(startDT.timestamp()))
    end_utc = str(int(endDT.timestamp()))
    # We need to use suffix to have the API actually change
    suffix = '&start=' + start_utc + '&end=' + end_utc + '&step=20s'
    # Right now I'm using this hardcoded one because our test data is so weird
    suffix_test = '&start=' + '1618172204' + '&end=' + '1618191179' + '&step=20s'
    # I was using this to test the formatting to make sure it was correct, we dont need anymore
    explorer_context['test'] = wattPre + suffix

    watt = requests.get(wattPre + suffix_test).json()
    temp = requests.get(tempPre + suffix_test).json()
    wattTemp = watt['data']['result'] + temp['data']['result']
    mqtt_list = []
    for i in range(len(wattTemp)):
        msg_values = dict(wattTemp[i]['values'])
        topic = wattTemp[i]['metric']['topic']
        msg_values = [(datetime.utcfromtimestamp(key).strftime('%Y-%m-%d %H:%M:%S'), topic, topic.rsplit("/", 1)[1], int(value)) for key, value in msg_values.items()]
        mqtt_list += msg_values
    
    if 'time_sort_down' in request.POST:
        explorer_context['time_sort'] = 'time_sort_up'
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort(reverse=True)
        last_sort = mqtt_list
    elif 'time_sort_up' in request.POST:
        explorer_context['time_sort'] = 'time_sort_down'
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort()
        last_sort = mqtt_list
    elif 'topic_sort_down' in request.POST:
        explorer_context['topic_sort'] = 'topic_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort(key=lambda x: x[1], reverse=True)
        last_sort = mqtt_list
    elif 'topic_sort_up' in request.POST:
        explorer_context['topic_sort'] = 'topic_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort(key=lambda x: x[1])
        last_sort = mqtt_list
    elif 'metric_sort_down' in request.POST:
        explorer_context['metric_sort'] = 'metric_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort(key=lambda x: x[2], reverse=True)
        last_sort = mqtt_list
    elif 'metric_sort_up' in request.POST:
        explorer_context['metric_sort'] = 'metric_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['values_sort'] = None
        mqtt_list.sort(key=lambda x: x[2])
        last_sort = mqtt_list
    elif 'values_sort_down' in request.POST:
        explorer_context['values_sort'] = 'values_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        mqtt_list.sort(key=lambda x: x[3], reverse=True)
        last_sort = mqtt_list
    elif 'values_sort_up' in request.POST:
        explorer_context['values_sort'] = 'values_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        mqtt_list.sort(key=lambda x: x[3])
        last_sort = mqtt_list

    if 'trip_qstart' in request.POST:
        explorer_context['qstart'] = request.POST.getlist('trip_qstart')[0]
    if 'trip_qend' in request.POST:
        explorer_context['qend'] = request.POST.getlist('trip_qend')[0]

    if last_sort == None:
        last_sort = mqtt_list

    paginator = Paginator(tuple(last_sort), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['mqtt'] = page_obj

    context['time_sort'] = explorer_context['time_sort']
    context['topic_sort'] = explorer_context['topic_sort'] 
    context['metric_sort'] = explorer_context['metric_sort'] 
    context['values_sort'] = explorer_context['values_sort']
    context['tomorrow'] = explorer_context['tomorrow']
    context['qstart'] = explorer_context['qstart']
    context['qend'] = explorer_context['qend']
    context['test'] = explorer_context['test']
    
    html_template = loader.get_template('explorer.html')
    return HttpResponse(html_template.render(context, request))
