# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests
import json, os
from .functionality.port_types import get_port_info

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
    port_count = {}
    port_dicts = []
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
def device(request):
    context = {}
    context['segment'] = 'device'
    context['ip'] = '10.1.1.4'
    context[ 'type' ] = 'camera'
    context[ 'mac' ] = 'aa:bb:cc:dd:ee:ff'
    context[ 'open_ports' ] = [ '22','6100','7103']
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
