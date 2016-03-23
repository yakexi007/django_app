# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template.context import RequestContext
from forms import UploadFileForm
import json
from salt import saltAPI,Redis
from mysql import mysql_insert
from models import history_data
from aliyun_cdn_api import main

@login_required
def check(request,check_id):
    if check_id == '1':
        return render(request,'check_file.html')
    elif check_id == '2':
        return render(request,'check_dir.html')
    elif check_id == '3':
        return render(request,'purge_cache.html')
    else:
        return HttpResponse("The Page Not Exit...")

@login_required
def check_dir_api(request):
    data = request.POST.getlist('data')
    info = '#'.join(data[-1].split('\r\n'))
    client = saltAPI()
    result = client.getDir(info)
    mysql_insert(request.user.username,'check_dir',data[0],data[1],result)
    return render(request,'message.html',{'content': result})

@login_required
def check_file_api(request):
    data = request.POST.getlist('data')
    info = '#'.join(data[-1].split('\r\n'))
    client = saltAPI()
    result = client.getMd5(info)
    mysql_insert(request.user.username,'check_file',data[0],data[1],result)
    return render(request,'message.html',{'content': result})

@login_required
def purge_api(request):
    data = request.POST.getlist('data')
    info = data[-1].split('\r\n')
    result = main(info)
    mysql_insert(request.user.username,'purge_cache',data[0],data[1],result)
    return render(request,'message.html',{'content': result})

@login_required
def history(request):
    data = history_data.objects.all()
    result = []
    for i in data:
        result.append([i.id,i.datetime,i.person,i.types,i.reason,eval(i.result)])
    return render(request,'history.html',{'data':result})

@login_required
def history_api(request):
    id = request.GET.get('id')
    data = history_data.objects.filter(id=id)
    get_data = {}
    for i in data:
        if i.types == 'purge_cache':
            result = eval(i.result)
            return HttpResponse(json.dumps(result))
        else:
            result = eval(i.result)
            for k,v in result.items():
                data = {}
                for k1,v1 in v.items():
                    if 'OK' != v1:
                        data[k1] = v1
                if 0 == len(data):
                    get_data[k] = {'result':'OK'}
                else:
                    get_data[k] = data
            return HttpResponse(json.dumps(get_data))
