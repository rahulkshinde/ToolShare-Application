#"""
#Name: toolViews
#Description: This file is responsible for rendering tool functionalities
#"""
import sys
import datetime
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import date,datetime
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
from app.views import borrowViews
#"""
#Method Name: AddTool
#Description: This method is responsible for rendering the register tool form
#"""

@login_required
@login_required
def Addtool(request):
   
            assert isinstance(request, HttpRequest)
            userprofile = Profile.objects.get(pk = request.user.id)
            shed = Shed.objects.filter(ShareZoneId=userprofile.sharezone)
            return render(
                request,
                'app/registerTool.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'YourTool Registeration Page',
                    'year':datetime.now().year,
                    'form':RegisterToolForm,
                    'sheds':shed,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )

#"""t
#Method Name: registerTool
#Description: This method is responsible for registering tool
#"""

@login_required
def registerTool(request):
    if request.POST:
        Toolform=RegisterToolForm(request.POST, request.FILES)
        if Toolform.is_valid():
            tool=Tools()
            tool.name=Toolform.cleaned_data['Toolname']
            tool.Description=Toolform.cleaned_data['Description']
            tool.Category=Toolform.cleaned_data['Category']
            tool.uniqueness=Toolform.cleaned_data['UniqueAttribute']
            tool.pickuparrangement=Toolform.cleaned_data['pickuparrangement']
            print(Toolform.cleaned_data['availability']);
            if (Toolform.cleaned_data['availability']=='true'):
                    tool.availability=True
                    tool.status='Available'
            else:
                    tool.availability=False  
                    tool.status='Not Available'       
            #tool.status=Toolform.cleaned_data['status']
            tool.activation=True
            tool.stuff_image=Toolform.cleaned_data['stuff_image']
            tool.registrationDate=datetime.now()
            try:
                user=Profile.objects.get(pk=request.user.id)
                tool.userID=user
            except ObjectDoesNotExist:
                user=0
            tool.useCount=0
            tool.lastBorrowDate=datetime.now()
            if (request.POST['pickuparrangement'] == 'Shed'):
                    tool.pickuparrangement='Shed'
                    tool.shedID = Shed.objects.get(pk=request.POST["shed_id"])
                    tool.Address1 = None
                    tool.Address2 = None
            if (request.POST['pickuparrangement'] == 'Other'):
                    tool.pickuparrangement='Other'
                    tool.Address1 = request.POST['address1']
                    tool.Address2 = request.POST['address2']
                    tool.shedID = None
            tool.save()
            userid = request.user.id
            userprofile = Profile.objects.get(pk = userid)
            tool = Tools.objects.filter(userID_id = userprofile.user_id)
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/mytools.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'tool':tool,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
        else:
            assert isinstance(request, HttpRequest)
            userprofile = Profile.objects.get(pk = request.user.id)
            shed = Shed.objects.filter(ShareZoneId=userprofile.sharezone)
            return render(
                request,
                'app/registerTool.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'YourTool Registeration Page',
                    'year':datetime.now().year,
                    'form':Toolform,
                    'sheds':shed,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )

#"""
#Method Name: toolTable
#Description: This method is responsible for displaying the regiestered tool list
#"""
@csrf_protect
@login_required
@csrf_exempt
def readTooldetails(request,toolid):
            tool=Tools.objects.get(id=toolid)
            if(request.is_ajax() and request.method=='POST'):
                if (request.POST['activation']=='1'):
                    tool.activation=True
                else:
                    tool.activation=False
                if (request.POST['availability']=='1'):
                    tool.availability=True
                    #tool.status = 'Available'
                else:
                    tool.availability=False
                    #tool.status = 'Not Available'
                    #print(tool.status)
                pickuparrangement= request.POST['pickuparrangement']
                if (request.POST['pickuparrangement']==pickuparrangement and request.POST['availability']=='1'):
                    tool.pickuparrangement='Home'
                else:
                    tool.pickuparrangement='Shed'
                tool.status=request.POST['status'];
                # Rahul Shinde - Sharing from community shed                
                if (request.POST['sharinglocation'] == 'Shed'):
                    tool.pickuparrangement='Shed'
                    tool.shedID = Shed.objects.get(pk=request.POST["shed_id"])
                    tool.Address1 = None
                    tool.Address2 = None
                # Rahul Shinde - Change Sharing Location  
                if (request.POST['sharinglocation'] == 'Other'):
                    tool.pickuparrangement='Other'
                    tool.Address1 = request.POST['otheraddress1']
                    tool.Address2 = request.POST['otheraddress2']
                    tool.shedID = None
                 #
                tool.save()
            isowner=(tool.userID.username==request.user.username)
            userid = request.user.id
            
            
            isborrower=0
            try:
                requestlist=Requests.objects.filter(ToolId_id=tool.id)
                for item in requestlist:
                    if item.BoorowerId.username==request.user.username:
                        isborrower=1
            except ObjectDoesNotExist:
                requestlist=None
            # Rahul Shinde - Change Sharing Location
            userprofile = Profile.objects.get(pk = userid)
            shareZoneId = userprofile.sharezone
            shedList = Shed.objects.filter(ShareZoneId=shareZoneId)
            print(shedList)
            print(datetime.today())
            #print(datetime.now().strftime("%Y-%m-%d"))
            Today = print(datetime.now().strftime("%Y-%m-%d"))
            #print(date.strftime(today,"%Y-%m-%d"))
            Borrowed_Flag= '0'
            Future_Reservations = '0'
            Cannot_Change_Details ='0'
            requestList = Requests.objects.filter(ToolId_id=toolid)
            for item in requestList:
                if ((item.status == 'Accepted') or (item.status == '')):
                   StartDate= date.strftime(item.StartDate,"%Y-%m-%d")
                   EndDate= date.strftime(item.EndDate,"%Y-%m-%d")

                   if ((date.strftime(item.StartDate,"%Y-%m-%d") <= datetime.now().strftime("%Y-%m-%d")) and (date.strftime(item.EndDate,"%Y-%m-%d") >= datetime.now().strftime("%Y-%m-%d"))):
                        Borrowed_Flag= '1'
                   if (date.strftime(item.StartDate,"%Y-%m-%d") > datetime.now().strftime("%Y-%m-%d")):
                        Future_Reservations = '1'
            if (Borrowed_Flag == '1' or Future_Reservations  == '1'):
                Cannot_Change_Details = '1';
            print(Cannot_Change_Details)
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/tooldetails.html',
                context_instance = RequestContext(request,
                {
                    'sheds':shedList,
                    'title':'Register Tool',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'tool':tool,
                    'id':toolid,
                    'isowner':isowner,
                    'userid':userid,
                    'requestlist':requestlist,
                    'isborrower':isborrower,
                    'Cannot_Change_Details':Cannot_Change_Details,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )

@login_required
def readmyTooldetails(request,toolid):
            tool=Tools.objects.get(id=toolid)
            userid = request.user.id
            form = updateToolForm()
            if tool.availability:
                form.fields['availability1'].initial= '1'
            else:
                form.fields['availability1'].initial= '0'
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/mytooldetails.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'tool':tool,
                    'id':toolid,
                    'userid':userid,
                    'form':form,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
#"""
#Method Name: toolList
#Description: This method is responsible for displaying the tool available in the sharezone
#"""

@login_required
def toolList(request):
            user_id = request.user.id
            userprofile = Profile.objects.get(pk = user_id)
            shareid = userprofile.sharezone_id
            Tool_ID = []
            #UP = Profile.objects.filter(sharezone_id = shareid)
            #for ups in UP:
            #    tool.add = Tools.objects.filter( userID_id = ups.pk)
            #tool = Tools.objects.filter( userID_id = UP.userID_id)
            for profile in Profile.objects.filter(sharezone_id = shareid):
                for tools in profile.tools_set.select_related().all():
                        if tools.userID_id != user_id:
                            if (tools.activation):
                                Tool_ID.append(tools.id)
            tool = Tools.objects.filter(pk__in=Tool_ID)
            
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/toollist.html',
                context_instance = RequestContext(request,
                {
                    'title':'Available Tools',
                    'message':'Your ashare zone available tools',
                    'year':datetime.now().year,
                    'tool':tool,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )


#"""
#Method Name: My Tools
#Description: This method is responsible for displaying the owners tools
#"""

@login_required
def myTools(request):
            userid = request.user.id
            userprofile = Profile.objects.get(pk = userid)
            tool = Tools.objects.filter(userID_id = userprofile.user_id)
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/mytools.html',
                context_instance = RequestContext(request,
                {
                    'title':'My Tools',
                    'message':'Your ashare zone available tools',
                    'year':datetime.now().year,
                    'tool':tool,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )

def updatemyTooldetails(request,toolid):
    if request.POST:
        Toolform=updateToolForm(request.POST)
        tool1=Tools.objects.get(id=toolid)
        userid = request.user.id
        if Toolform.is_valid():
           tool1.availability=Toolform.cleaned_data['availability1']
           if tool1.availability == 1:
                tool1.availability = True
                tool1.status='Available'
                tool1.save()
           else:
                tool1.availability = False
                tool1.save()
        userprofile = Profile.objects.get(pk = userid)
        tool11 = Tools.objects.filter(userID_id = userprofile.user_id)
        assert isinstance(request, HttpRequest)
        return render(
                request,
                'app/mytools.html',
                context_instance = RequestContext(request,
                {
                    'title':'Available Tools',
                    'message':'Your ashare zone available tools',
                    'year':datetime.now().year,
                    'tool':tool11,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
    else:
        tool=Tools.objects.get(id=toolid)
        userid = request.user.id
        form = updateToolForm()
        form.fields['availability1'].initial= tool.availability
        assert isinstance(request, HttpRequest)
        return render(
                request,
                'app/mytoolupdate.html',
                context_instance = RequestContext(request,
                {
                    'title':'Register Tool',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'tool':tool,
                    'id':toolid,
                    'userid':userid,
                    'form':form,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
    