#"""
#Name:borrowlViews
#Description: This file is responsible for rendering tool functionalities
#"""
import sys
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt ,csrf_protect
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from app.forms import forms
from app.forms import *
from app.models import *
from django.contrib.auth.models import User
from datetime import datetime

#"""
#Method Name: requesttool
#Description: This method is responsible for handling tool requests
#"""


@csrf_protect
@login_required
@csrf_exempt
def requesttool(request,toolid):
            tool=Tools.objects.get(id=toolid)
            if(request.is_ajax() and request.method=='POST'):
               req=Requests()
               req.BoorowerId=Profile.objects.get(username=request.user.username)
               req.Owner=tool.userID.username
               req.ToolId=tool
               req.StartDate=request.POST['startdate']
               req.EndDate=request.POST['enddate']
               req.borrowerMessage=request.POST['message1']
               req.ownerMessage=request.POST['message2']
               req.status=''
               if tool.pickuparrangement=='Shed':
                   req.status='Accepted'
                   req.ownerMessage='Your request has been utomatically approved by the system'
               req.save()
               if Requests.objects.filter(ToolId=tool).count()== Requests.objects.filter(ToolId=tool,status='Rejected').count():
                   if tool.availability==True:
                       tool.status='Available'
                   else:
                       tool.status='Not available'
               elif Requests.objects.filter(ToolId=tool,status='Accepted').count()>0:
                       tool.status='Reserved'
               elif Requests.objects.filter(ToolId=tool,status='Waiting for owner confirmation').count()>0:
                       tool.status='Reserved'
               else:
                   tool.status='Requested'
               tool.save()
            isowner=(tool.userID.username==request.user.username)
            userid = request.user.id
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/tooldetails.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'tool':tool,
                    'id':toolid,
                    'isowner':isowner,
                    'userid':userid,
                    'requestscount':countfunction(request.user.id),
                })
            )

@login_required
def mynotifications(request):
    try:
        requestlist1=Requests.objects.filter(BoorowerId_id=request.user.id)
    except ObjectDoesNotExist:
        requestlist1=None

    try:
        requestlist2=Requests.objects.filter(Owner=request.user.username)
    except ObjectDoesNotExist:
        requestlist2=None

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mynotification.html',
        context_instance = RequestContext(request,
        {
            'title':'My Request and reservation page',
            'message':'welcome',
            'year':datetime.now().year,
            'requestlist1':requestlist1,
            'requestlist2':requestlist2,
            'today':datetime.now(),
            'requestscount':countfunction(request.user.id),
        })
    )
@login_required
def mynotifications1(request):
    try:
        requestlist1=Requests.objects.filter(BoorowerId_id=request.user.id)
    except ObjectDoesNotExist:
        requestlist1=None

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mynotification1.html',
        context_instance = RequestContext(request,
        {
            'title':'My Request and reservation page',
            'message':'welcome',
            'year':datetime.now().year,
            'requestlist1':requestlist1,
            'today':datetime.now(),
            'requestscount':countfunction(request.user.id),
        })
    )
@login_required
def mynotifications3(request):
    shedList = Shed.objects.filter(CordinatorUserId=request.user.id)
    tool=Tools.objects.filter(shedID=shedList)
    try:
        requestlist2=Requests.objects.filter(ToolId_id=tool)
    except ObjectDoesNotExist:
        requestlist2=None
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mynotification3.html',
        context_instance = RequestContext(request,
        {
            'title':'My Shed Requests page',
            'message':'welcome',
            'year':datetime.now().year,
            'requestlist2':requestlist2,
            'today':datetime.now(),
            'requestscount':countfunction(request.user.id),
        })
    )
@login_required
def mynotifications2(request):

    try:
        requestlist2=Requests.objects.filter(Owner=request.user.username)
    except ObjectDoesNotExist:
        requestlist2=None

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mynotification2.html',
        context_instance = RequestContext(request,
        {
            'title':'My tools Requests page',
            'message':'welcome',
            'year':datetime.now().year,
            'requestlist2':requestlist2,
            'today':datetime.now(),
            'requestscount':countfunction(request.user.id),
        })
    )

@csrf_protect
@login_required
@csrf_exempt
def requestAction(request,requestid):
            if(request.is_ajax() and request.method=='POST'):
               req=Requests.objects.get(id=request.POST['id'])
               tool=Tools.objects.get(id=req.ToolId_id)
               if(request.POST['action']=='accept'):
                    req.borrowerMessage=request.POST['mymessage1'];
                    req.ownerMessage=request.POST['mymessage2'];
                    if req.status=='':
                        user=Profile.objects.get(id=req.BoorowerId_id)
                        user.BorrowCount=user.BorrowCount+1
                        user.save()
                        user=Profile.objects.get(username=req.Owner)
                        user.LendCount=user.LendCount+1
                        user.save()
                        tool.useCount=tool.useCount+1
                        tool.lastBorrowDate=datetime.now()
                        tool.save()
                    req.status='Accepted'
                    req.save()
               elif(request.POST['action']=='reject'):
                    req.ownerMessage=request.POST['mymessage2'];
                    req.status='Rejected'
                    req.save()
               elif(request.POST['action']=='borrowerreturn'):
                    req.borrowerMessage=request.POST['mymessage1'];
                    req.status='Waiting for owner confirmation'
                    req.save()
               elif(request.POST['action']=='borrowercancel'):
                    if req.status!='':
                        user=Profile.objects.get(id=req.BoorowerId_id)
                        user.BorrowCount=user.BorrowCount-1
                        user.save()
                        user=Profile.objects.get(username=req.Owner)
                        user.LendCount=user.LendCount-1
                        user.save()
                        tool=Tools.objects.get(id=req.ToolId_id)
                        tool.useCount=tool.useCount-1
                        tool.save()
                        if req.status!='':
                            res=Reservations()
                            res.BoorowerId=req.BoorowerId
                            res.Owner=req.Owner
                            res.ToolId=req.ToolId
                            res.StartDate=req.StartDate
                            res.EndDate=res.EndDate
                            if req.status=='Rejected':
                                res.status='Rejected'
                            else:
                                res.status='Canceled'
                            res.save()
                        req.delete()    
               else:
                   res=Reservations()
                   res.BoorowerId=req.BoorowerId
                   res.Owner=req.Owner
                   res.ToolId=req.ToolId
                   res.StartDate=req.StartDate
                   res.EndDate=req.EndDate
                   res.status='Approved'
                   res.save()

                   req.delete()
               if Requests.objects.filter(ToolId=tool).count()== Requests.objects.filter(ToolId=tool,status='Rejected').count():
                   if tool.availability==True:
                       tool.status='Available'
                   else:
                       tool.status='Not available'
               elif Requests.objects.filter(ToolId=tool,status='Accepted').count()>0:
                       tool.status='Reserved'
               elif Requests.objects.filter(ToolId=tool,status='Waiting for owner confirmation').count()>0:
                       tool.status='Reserved'
               else:
                   tool.status='Requested'
               tool.save()
               assert isinstance(request, HttpRequest)
               return render(
                    request,
                    'app/mynotification1.html',
                    context_instance = RequestContext(request,
                    {
                        'title':'My Request and reservation page',
                        'message':'welcome',
                        'year':datetime.now().year,
                        'requestscount':countfunction(request.user.id),
                    })
               )

#"""
#Method Name: countfunction
#Description: This method is responsible for returning request counts
#"""

@login_required
def myhistory(request):
    try:
        requestlist1=Reservations.objects.filter(BoorowerId_id=request.user.id)
    except ObjectDoesNotExist:
        requestlist1=None
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/MyHistory.html',
        context_instance = RequestContext(request,
        {
            'title':'My Request and reservation page',
            'message':'welcome',
            'year':datetime.now().year,
            'requestlist1':requestlist1,
            'today':datetime.now(),
            'requestscount':countfunction(request.user.id),
        })
    )
def countfunction(id):
        requestcount1=Requests.objects.filter(BoorowerId_id=id).count()
        print (requestcount1)
        user=Profile.objects.get(pk=id)
        requestcount2=Requests.objects.filter(Owner=user.username).count()
        shedList = Shed.objects.filter(CordinatorUserId=id)
        tool=Tools.objects.filter(shedID=shedList)
        requestcount3=Requests.objects.filter(ToolId_id=tool).count()
        return (requestcount1+requestcount2+requestcount3)