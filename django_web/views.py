# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template.context import RequestContext
from forms import LoginForm
# Create your views here.

@login_required
def index(request):
    #return render_to_response('index.html')
    return render(request,'index.html',{'user':request.user})

def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(request.GET['next'])
        else:
            #return HttpResponseRedirect('/login/?next=%s' %request.GET['next'],{'form':form})
            form = LoginForm()
            return render_to_response('login.html',{'form':form,'pass_wrong':True})
    else:
        form = LoginForm()
        return render_to_response('login.html',{'form':form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
