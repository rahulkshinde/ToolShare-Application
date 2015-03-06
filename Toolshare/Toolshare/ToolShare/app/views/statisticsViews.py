#"""
#Name: statisticsView.py
#Description: This file is responsible for handling functionalities related to statistics.
#"""

import sys
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Tools
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
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
from django.db.models import Count
from app.views import borrowViews

#"""
#Method Name: MostActiveToolView
#Description: This file is responsible for displaying Tool Statistics
#"""
@login_required
def MostActiveToolView(request):
    assert isinstance(request, HttpRequest)
    user=Profile.objects.get(pk=request.user.id)
    users=Profile.objects.filter(sharezone=user.sharezone)
    print(users.count())
    tools = Tools.objects.filter(userID=users).order_by('-useCount')
    return render(
        request,
        'app/MostActiveTool.html',
        context_instance = RequestContext(request,
        {
            'title':'Tool Statistics',
            'year':datetime.now().year,
            'tools':tools,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
    )
#"""
#Method Name: MostActiveUserView
#Description: This file is responsible for displaying User Statistics
#"""
@login_required
def MostActiveUserView(request):
    assert isinstance(request, HttpRequest)
    user=Profile.objects.get(pk=request.user.id)
    requests = Profile.objects.filter(sharezone=user.sharezone).order_by('-LendCount')
    return render(
        request,
        'app/MostActiveUser.html',
        context_instance = RequestContext(request,
        {
            'title':'User Statistics',
            'year':datetime.now().year,
            'requests':requests,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
    )
