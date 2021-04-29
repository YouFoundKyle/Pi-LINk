from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
import requests
import json, os
from datetime import datetime, timedelta
from .functionality.util import get_port_info, get_device_info, dump_device_info, dump_update_info
from .forms import DeviceForm, UpdateForm

def get_client_ip(request):
    return request.META.get('HTTP_HOST').split(':')[0].strip()

def get_device_ips():
    ips = []
    if os.path.exists("/etc/pilink/web/lease_DB.json"):
        with open("/etc/pilink/web/lease_DB.json") as df:
            lease_DB = json.load(df)
            for mac, info in lease_DB.items():
                if 'IP' in info.keys():
                    ips.append(info['IP'])
    return ips
            
@login_required(login_url="/login/")
def net_overview(request):
    context = {}
    context['segment'] = 'network'
    # if request.method == 'POST':
    #     updateInfo = UpdateForm(request.POST)
    #     if updateInfo.is_valid():
    #         print(updateInfo.cleaned_data)
    #         dump_update_info(updateInfo.cleaned_data)
    #     else:
    #         print("invalid")
    #         print(updateInfo.cleaned_data)
    #     return HttpResponseRedirect('/network')
    if os.path.exists("/etc/pilink/web/lease_DB.json"):
        with open("/etc/pilink/web/lease_DB.json") as df:
            dev_data = json.load(df)
        context['lease_data'] = dev_data
        port_dicts = []
        updates = {}
        port_count = {}
        context['devices'] = get_device_ips()
        for key, val in dev_data.items():
            if val["port_usage"]:
                port_dicts.extend(val["port_usage"])
            updates[key] = {"firmware":val["firmware"], "last_updated":val["last_updated"]}
        for port in port_dicts:
            if port["port_id"] in port_count.keys():
                port_count[port["port_id"]] += 1
            else:
                port_count[port["port_id"]] = 1
        context['port_info'] = port_count
        context['update_info'] = updates

        if os.path.exists("/etc/pilink/web/alerts.json"):
            with open("/etc/pilink/web/alerts.json") as df:
                alerts = json.load(df)
        context['alerts'] = alerts
        
        html_template = loader.get_template('network_overview.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def device(request, requested_ip):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        deviceInfo = DeviceForm(request.POST)
        if deviceInfo.is_valid():
            print(deviceInfo.cleaned_data)
            dump_device_info(deviceInfo.cleaned_data)
        return HttpResponseRedirect(f'/device/{requested_ip}')

    device_info = get_device_info(requested_ip)

    if 'unknown' in device_info.keys():
        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render({}, request))
        
    context = {}
    context['devices'] = get_device_ips()
    context[ 'segment' ] = 'device'
    context[ 'ip' ] = requested_ip
    context[ 'type' ] = device_info['type'] if 'type' in device_info.keys() else "Unknown"
    context[ 'mac' ] = device_info['MAC']
    context[ 'open_ports' ] = device_info['port_list']
    context[ 'deviceStatus' ] = device_info['device_status']
    context[ 'on_network' ] = True if device_info['lease_state'] == "active" else False
    
    info_keys = ['firmware', 'vendor', 'hostname', 'last_updated' ]

    for key in info_keys:
        context[ key ] = device_info[ key ]
    context[ 'port_info' ] = {}
    
    for port in context['open_ports']:
        context[ 'port_info' ][port]  = get_port_info(port)
    
    if 'pend_p' in device_info.keys():
        context['pendingPorts'] = device_info['pend_p']

    html_template = loader.get_template('device_overview.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dns(request):
    context = {}
    context['segment'] = 'dns'

    html_template = loader.get_template('dns_dashboard.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def mqtt_overview(request):
    user_ip = str(get_client_ip(request))

    context = {'ip' : user_ip}
    context['devices'] = get_device_ips()
    context['segment'] = 'mqtt_overview'

    html_template = loader.get_template( 'mqtt.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    context['devices'] = get_device_ips()
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
 'values_sort': None, 'today': today, 'tomorrow': tomorrow, 'qstart': yesterday, "qend": today, 'error': None}
global last_sort
last_sort = None

@login_required(login_url="/login/")
def explorer(request):
    global last_sort
    context = {}
    explorer_context['devices'] = get_device_ips()
    
    if 'trip_qstart' in request.POST:
        explorer_context['qstart'] = request.POST.getlist('trip_qstart')[0]
        explorer_context['qend'] = request.POST.getlist('trip_qend')[0]

    try:
        # Formatting API url
        ip = get_client_ip(request)
        wattPre = f'http://{ ip }:9090/api/v1/query_range?query=watts'
        tempPre = f'http://{ ip }:9090/api/v1/query_range?query=temperature'

        startDT = datetime.strptime(explorer_context['qstart'], '%Y-%m-%d')
        endDT = datetime.strptime(explorer_context['qend'], '%Y-%m-%d')
        start_utc = str(int(startDT.timestamp()))
        end_utc = str(int(endDT.timestamp()))
        suffix = '&start=' + start_utc + '&end=' + end_utc + '&step=60s'

        watt = requests.get(wattPre + suffix).json()
        temp = requests.get(tempPre + suffix).json()
        wattTemp = watt['data']['result'] + temp['data']['result']
        mqtt_list = []
        explorer_context['error'] = None
        for i in range(len(wattTemp)):
            msg_values = dict(wattTemp[i]['values'])
            topic = wattTemp[i]['metric']['topic']
            msg_values = [(datetime.utcfromtimestamp(key).strftime('%Y-%m-%d %H:%M:%S'), topic, topic.rsplit("/", 1)[1], int(value)) for key, value in msg_values.items()]
            mqtt_list += msg_values
    except:
        explorer_context['error'] = 'Please try a another range of dates!'
    
    if (last_sort == None or 'trip_qstart' in request.POST) and explorer_context['error'] == None:
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
    explorer_context['mqtt'] = page_obj
    explorer_context['segment'] = 'explorer'

    html_template = loader.get_template('explorer.html')
    return HttpResponse(html_template.render(explorer_context, request))
