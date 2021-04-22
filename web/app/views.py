# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests
import json, os
from datetime import datetime, timedelta
from .functionality.util import get_port_info, get_device_info

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def net_overview(request):

    context = {}
    context['segment'] = 'index'
    if os.path.exists("/etc/pilink/web/lease_DB.json"):
        with open("/etc/pilink/web/lease_DB.json") as df:
            dev_data = json.load(df)
    context['lease_data'] = dev_data
    port_dicts = []
    port_count = {}
    for key, val in dev_data.items():
        ports = val["port_usage"]
        port_dicts.extend(ports)
    for port in port_dicts:
        if port["port_id"] in port_count.keys():
            port_count[port["port_id"]] += 1
        else:
            port_count[port["port_id"]] = 1
    context['port_info'] = port_count
    html_template = loader.get_template('network_overview.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def device(request, requested_ip):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
            return HttpResponseRedirect('/device_overview/')

    device_info = get_device_info(requested_ip)

    context = {}
    context['segment'] = 'device'
    context['ip'] = requested_ip
    context[ 'type' ] = 'camera'
    context[ 'mac' ] = device_info['MAC']
    context[ 'open_ports' ] = device_info['port_list']
    context[ 'port_info' ] = {}
    
    for port in context['open_ports']:
        context[ 'port_info' ][port]  = get_port_info(port)
    
    html_template = loader.get_template('device_overview.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dns(request):
    context = {}
    context['segment'] = 'dns'

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


## For Explorer
yesterday = (datetime.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
today = datetime.today().strftime("%Y-%m-%d")
tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
explorer_context = {'time_sort': 'time_sort_down', 'topic_sort': None, 'metric_sort': None,
 'values_sort': None, 'today': today, 'tomorrow': tomorrow, 'qstart': yesterday, "qend": today, 'error': ''}
global last_sort
last_sort = None

def explorer(request):
    global last_sort
    context = {}
    context['segment'] = 'explorer'

    if 'trip_qstart' in request.POST:
        explorer_context['qstart'] = request.POST.getlist('trip_qstart')[0]
        explorer_context['qend'] = request.POST.getlist('trip_qend')[0]

    try:
        # Formatting API url
        wattPre = 'http://192.168.1.123:9090/api/v1/query_range?query=watts'
        tempPre = 'http://192.168.1.123:9090/api/v1/query_range?query=temperature'

        startDT = datetime.strptime(explorer_context['qstart'], '%Y-%m-%d')
        endDT = datetime.strptime(explorer_context['qend'], '%Y-%m-%d')
        start_utc = str(int(startDT.timestamp()))
        end_utc = str(int(endDT.timestamp()))
        suffix = '&start=' + start_utc + '&end=' + end_utc + '&step=60s'

        watt = requests.get(wattPre + suffix).json()
        temp = requests.get(tempPre + suffix).json()
        wattTemp = watt['data']['result'] + temp['data']['result']
        mqtt_list = []
        explorer_context['error'] = ''
        for i in range(len(wattTemp)):
            msg_values = dict(wattTemp[i]['values'])
            topic = wattTemp[i]['metric']['topic']
            msg_values = [(datetime.utcfromtimestamp(key).strftime('%Y-%m-%d %H:%M:%S'), topic, topic.rsplit("/", 1)[1], int(value)) for key, value in msg_values.items()]
            mqtt_list += msg_values
    except:
        explorer_context['error'] = 'Please try a another range of dates!'
    
    if (last_sort == None or 'trip_qstart' in request.POST) and explorer_context['error'] == '':
        explorer_context['time_sort'] = 'time_sort_down'
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        last_sort = sorted(mqtt_list)

    if 'time_sort_down' in request.POST:
        explorer_context['time_sort'] = 'time_sort_up'
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort(reverse=True)
    elif 'time_sort_up' in request.POST:
        explorer_context['time_sort'] = 'time_sort_down'
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort()
    elif 'topic_sort_down' in request.POST:
        explorer_context['topic_sort'] = 'topic_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort(key=lambda x: x[1], reverse=True)
    elif 'topic_sort_up' in request.POST:
        explorer_context['topic_sort'] = 'topic_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['metric_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort(key=lambda x: x[1])
    elif 'metric_sort_down' in request.POST:
        explorer_context['metric_sort'] = 'metric_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort(key=lambda x: x[2], reverse=True)
    elif 'metric_sort_up' in request.POST:
        explorer_context['metric_sort'] = 'metric_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['values_sort'] = None
        last_sort.sort(key=lambda x: x[2])
    elif 'values_sort_down' in request.POST:
        explorer_context['values_sort'] = 'values_sort_up'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        last_sort.sort(key=lambda x: x[3], reverse=True)
    elif 'values_sort_up' in request.POST:
        explorer_context['values_sort'] = 'values_sort_down'
        explorer_context['time_sort'] = None
        explorer_context['topic_sort'] = None
        explorer_context['metric_sort'] = None
        last_sort.sort(key=lambda x: x[3])
    elif 'search' in request.POST:
        search = request.POST.getlist('search')[0]
        filtered = filter(lambda x: search in x[1], last_sort)
        last_sort = list(filtered)

    paginator = Paginator(tuple(last_sort), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['mqtt'] = page_obj

    context['time_sort'] = explorer_context['time_sort']
    context['topic_sort'] = explorer_context['topic_sort'] 
    context['metric_sort'] = explorer_context['metric_sort'] 
    context['values_sort'] = explorer_context['values_sort']
    context['today'] = explorer_context['today']
    context['tomorrow'] = explorer_context['tomorrow']
    context['qstart'] = explorer_context['qstart']
    context['qend'] = explorer_context['qend']
    context['error'] = explorer_context['error']
    
    html_template = loader.get_template('explorer.html')
    return HttpResponse(html_template.render(context, request))
