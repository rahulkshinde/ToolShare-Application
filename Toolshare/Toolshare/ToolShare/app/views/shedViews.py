#"""
#Name: shedViews.py
#Description: This file is responsible for handling requests and rendering forms and templates related to shed
#"""
import sys
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Shed,Tools
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt ,csrf_protect
from django.contrib.auth.decorators import login_required
from app.forms import ShedForm
from app.forms import signUp
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from app.forms import forms
from app.forms import *
from django.contrib.auth.models import User
from app.views import borrowViews
#"""
#Method Name: createShed
#Description: This method is responsible for creation of shed based on user input
#"""
@login_required
def createShed(request):
        return render(
        request,
        'app/shed.html',
        context_instance = RequestContext(request,
        {
            'title':'shed',
            'message':'Your shed page.',
            'year':datetime.now().year,
            'forms':ShedForm,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
        )
#=====================Shed View        ===============================
#"""
#Method Name: ShedView
#Description: This method is responsible for displaying the shed creation form
#"""
@login_required
def ShedView(request):
    shedform =ShedForm(request.POST)
    userprofile = Profile.objects.get(pk = request.user.id)
    shareZoneId = userprofile.sharezone
    shedList = Shed.objects.filter(ShareZoneId=shareZoneId,Name=request.POST['Name1'])
    if len(shedList)>0:
        dup='yes'
    else:
        dup='no' 
    if shedform.is_valid(dup):
        shed=Shed()
        shed.Name=shedform.cleaned_data['Name1']
        shed.Address1=shedform.cleaned_data['Address1']
        shed.Address2=shedform.cleaned_data['Address2']
      
        try:
           user = Profile.objects.get(pk=request.user.id)
           shed.CordinatorUserId=user
        except ObjectDoesNotExist:
           user=0

        try:
           user = Profile.objects.get(pk=request.user.id)
           shed.ShareZoneId=user.sharezone
        except ObjectDoesNotExist:
           zone=0
        shed.save()
        userprofile = Profile.objects.get(pk = request.user.id)
        shed = Shed.objects.filter(ShareZoneId=userprofile.sharezone)
        return render(
            request,
            'app/shedTable.html',
            context_instance = RequestContext(request,
            {
                'title':'Shed Table',
                'year':datetime.now().year,
                'shed':shed,
                'requestscount':borrowViews.countfunction(request.user.id),
            })
        )
    else:
        return render(
        request,
        'app/shed.html',
        context_instance = RequestContext(request,
        {
            'title':'shed',
            'message':'Your shed page.',
            'year':datetime.now().year,
            'forms':shedform,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
        )

#"""
#Method Name: ShedTable
#Description: This method is responsible for displaying the shed list
#"""
@login_required
def shedTable(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    userprofile = Profile.objects.get(pk = request.user.id)
    shed = Shed.objects.filter(ShareZoneId=userprofile.sharezone)
    return render(
        request,
        'app/shedTable.html',
        context_instance = RequestContext(request,
        {
            'title':'Shed Table',
            'year':datetime.now().year,
            'shed':shed,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
    )
@csrf_protect
@csrf_exempt
@login_required
def readSheddetails(request,shedid):
            shed=Shed.objects.get(id=shedid)
            if(request.is_ajax() and request.method=='POST'):
                shed.Name=request.POST['name']
                shed.Address1=request.POST['Address1']
                shed.save()
            isowner=(shed.CordinatorUserId.username==request.user.username)
            tool=Tools.objects.filter(shedID=shed)
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/sheddetails.html',
                context_instance = RequestContext(request,
                {
                    'title':shed.Name,
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'shed':shed,
                    'tool':tool,
                    'toolcount':tool.count(),
                    'isowner':isowner,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
