#"""
#Name: userViews.py
#Description: This file is responsible for handling functionalities related to users.
#"""

import sys
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Shed
from app.models import Tools
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from app.forms import ShedForm,RegisterToolForm
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
#Method Name: createUser
#Description: This method is responsible for displaying the signup form
#"""

def createUser(request):
        return render(
        request,
        'app/signup.html',
        context_instance = RequestContext(request,
        {
            'title':'Sign Up',
            'message':'Your signup page.',
            'year':datetime.now().year,
            'form':signUp,

        })
        )

#"""
#Method Name: Usersignup
#Description: This method is responsible for registering new user
#"""

def Usersignup(request):
    if request.POST:
        userform=signUp(request.POST)
        if userform.is_valid():
            #if userform.cleaned_data['password1'] != userform.cleaned_data['password2']:
             #       raise forms.ValidationError("Passwords do not match.")
            userprofile = Profile.objects.create_user(userform.cleaned_data["username"],userform.cleaned_data["email"],userform.cleaned_data["password1"])
            userprofile.first_name=userform.cleaned_data['first_name']
            userprofile.last_name=userform.cleaned_data['last_name']
            userprofile.last_login=datetime.now()
            userprofile.date_joined=datetime.now()
            userprofile.Middle_Name=userform.cleaned_data['middle_name']
            userprofile.PhoneNumber=userform.cleaned_data['PhoneNumber']
            userprofile.Dateofbirth=userform.cleaned_data['dateofbirth']
            #userprofile.RegistrationDate=datetime.now()
            userprofile.Address1=userform.cleaned_data['address1']
            userprofile.Address2=userform.cleaned_data['address2']
            userprofile.PickUpArrangement=userform.cleaned_data['pickuparrangement']
            userprofile.Gender=userform.cleaned_data['gender']
            userprofile.BorrowCount=0
            userprofile.LendCount=0
            userprofile.user=userprofile
            zipcode3 = userform.cleaned_data['zipcode']
            try:
                zone = Sharezone.objects.get(pk=zipcode3)
                userprofile.sharezone=zone
            except ObjectDoesNotExist:
                zone=Sharezone()
                zone.ZipCode=userform.cleaned_data['zipcode']
                zone.Country=userform.cleaned_data['country']
                zone.State=userform.cleaned_data['state']
                zone.City=userform.cleaned_data['city']
                zone.SharezoneName=userform.cleaned_data['city']
                zone.save()
                userprofile.sharezone=zone
            userprofile.save()
            from django.contrib.auth import authenticate, login
            user = authenticate(username =userform.cleaned_data['username'], password =userform.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            usr= user
            assert isinstance(request, HttpRequest)
            return render(
            request,
            'app/Registration_Success.html',
            context_instance = RequestContext(request,
            {
                'title':'User has been created',
                'message':'welcome',
                'year':datetime.now().year,
                'usr':usr,
      
            })
            )
        else:
            usr= Profile.objects.all()
            return render(
            request,
            'app/signup.html',
            context_instance = RequestContext(request,
            {
                'title':'Sign Up',
                'message':'Error',
                'year':datetime.now().year,
                'form':userform,
            })
        )
#===========  pooja ==========================================
#=========== profile view ====================================
#"""
#Method Name: profileview
#Description: This method is responsible for the functionality related to users profile changes
#"""

@login_required
def profileview(request):
    if request.POST:
        user_id = request.user.id
        userprofile = Profile.objects.get(pk = user_id)
        userform=Profileform(request.POST)
        if userform.is_valid():
            #userprofile.first_name=userform.cleaned_data['FirstName']
            #userprofile.last_name=userform.cleaned_data['LastName']
            #userprofile.Middle_Name=userform.cleaned_data['MiddleName']
            userprofile.Address1=userform.cleaned_data['Address11']
            userprofile.Address2=userform.cleaned_data['Address12']
            userprofile.Gender=userform.cleaned_data['Gender1']
            userprofile.PhoneNumber=userform.cleaned_data['PhoneNumber']
            userprofile.email=userform.cleaned_data['Email']
            #userprofile.Dateofbirth=userform.cleaned_data['DateofBirth1']
            if (userprofile.sharezone.ZipCode!=userform.cleaned_data['ZipCode']):
                shedList = Shed.objects.filter(CordinatorUserId=request.user.id)
                tools=Tools.objects.filter(shedID=shedList)
                for tool in tools:
                    tool.pickuparrangement='Home'
                    tool.Address1 =None
                    tool.Address2 = None
                    tool.shedID = None
                    tool.save()
                for shed in shedList:
                    shed.delete()
            try:
                zone = Sharezone.objects.get(pk=userform.cleaned_data['ZipCode'])
                userprofile.sharezone=zone
            except ObjectDoesNotExist:
                zone=Sharezone()
                zone.ZipCode=userform.cleaned_data['ZipCode']
                zone.Country=userform.cleaned_data['Country11']
                zone.State=userform.cleaned_data['State11']
                zone.City=userform.cleaned_data['City11']
                zone.SharezoneName=userform.cleaned_data['City11']
                zone.save()
                userprofile.sharezone=zone
            userprofile.save()
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/usertable.html',
                context_instance = RequestContext(request,
                {
                    'title':'User Profile has been updated',
                    'message':'your profile has been successfully updated',
                    'year':datetime.now().year,
                    'usr':userprofile,
                    'requestscount':borrowViews.countfunction(request.user.id),
                })
            )
        else:
            return render(
                request,
                'app/Profile.html',
                context_instance = RequestContext(request,
                {
                    'title':'User Profile did not submit',
                    'message':'There were some errors',
                    'year':datetime.now().year,
                    'form':userform,
                })
            )    
    else:
        assert isinstance(request, HttpRequest)
        user_id = request.user.id
        profile = Profile.objects.get(pk = user_id)
        form =Profileform()
        form.fields['FirstName'].initial= profile.first_name
        form.fields['LastName'].initial= profile.last_name
        form.fields['MiddleName'].initial = profile.Middle_Name
        form.fields['Address11'].initial = profile.Address1
        form.fields['Address12'].initial = profile.Address2
        form.fields['Gender1'].initial = profile.Gender
        form.fields['Email'].initial= profile.email
        form.fields['PhoneNumber'].initial = profile.PhoneNumber
        #form.fields['DateofBirth1'].initiall=profile.Dateofbirth
        form.fields['ZipCode'].initial=profile.sharezone.ZipCode
        form.fields['Country11'].initial=profile.sharezone.Country
        form.fields['State11'].initial=profile.sharezone.State
        form.fields['City11'].initial=profile.sharezone.City
        return render(
            request,
            'app/Profile.html',
            context_instance = RequestContext(request,
            {
                'title':'Update User profile',
                'message':'Your profile page',
                'year':datetime.now().year,
                'form':form,
                'requestscount':borrowViews.countfunction(request.user.id),
            })
        )


            
#=========== pooja        ===============
#============ preference view ===========
#"""
#Method Name: preferenceview
#Description: This method is responsible for handling the users preference changes
#"""

@login_required
def preferenceview(request):
    if(request.POST):
        preference1 =PreferenceForm(request.POST)
        assert isinstance(request, HttpRequest)
        user_id = request.user.id
        profile = Profile.objects.get(pk = user_id)
        if preference1.is_valid():
            profile.PickUpArrangement=preference1.cleaned_data['PickUpArrangements']
            profile.RemainderFrequency=preference1.cleaned_data['RemainderFrequency1']
            profile.RemainderType=preference1.cleaned_data['RemainderType1']
            profile.save()
            usr=Profile.objects.get(pk=request.user.id)
        """Renders the about page."""
        return render(
            request,
            'app/usertable.html',
            context_instance = RequestContext(request,
            {
                'title':'Change User Preferences',
                'message':'Your Preference Page.',
                'year':datetime.now().year,
                'usr':usr,
                'requestscount':borrowViews.countfunction(request.user.id),
            })
        )
    else:
            preference1 =PreferenceForm()
            profile = Profile.objects.get(pk = request.user.id)
            preference1.fields['PickUpArrangements'].initial=profile.PickUpArrangement
            preference1.fields['RemainderFrequency1'].initial=profile.RemainderFrequency
            preference1.fields['RemainderType1'].initial = profile.RemainderType

            return render(
            request,
            'app/preference.html',
            context_instance = RequestContext(request,
            {
                'title':'Change User Preferences',
                'message':'Your Preference Page.',
                'year':datetime.now().year,
                'form':preference1,
                'requestscount':borrowViews.countfunction(request.user.id),
            })
        )

#"""
#Method Name: myprofile
#Description: This method is responsible for displaying the users profile
#"""

@login_required
def myprofile(request):
    usr=Profile.objects.get(pk=request.user.id)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/usertable.html',
        context_instance = RequestContext(request,
        {
            'title':'My Profile',
            'message':'welcome',
            'year':datetime.now().year,
            'usr':usr,
        })
    )


@login_required
def userprofile(request,userid):
    usr=Profile.objects.get(pk=userid)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/usertable.html',
        context_instance = RequestContext(request,
        {
            'title':'My Profile',
            'message':'welcome',
            'year':datetime.now().year,
            'usr':usr,
        })
    )
# Rahul Shinde
#"""
#Method Name: resetPasswordView
#Description: This method is responsible for resetting password
#"""
def resetPasswordView(request):
    """Renders the about page."""
    context=RequestContext(request,
        {
            'title':'Change Password',
            'message':'Please reset your password',
            'year':datetime.now().year,

            
        })
    
    if request.POST:
        form=resetPasswordForm(request.POST)
        context['form']=form
        if form.is_valid():
             password = User.objects.make_random_password()
             user = User.objects.get(username=form.cleaned_data['userName'])
             user.set_password(password)
             user.save()
             context['msg']='Your new password is:'+password
    else:
        form = resetPasswordForm()
        context['form']=form



    return render(
        request,
        'app/password_change_form.html',
        context_instance = context )

# Rahul Shinde
#"""
#Method Name: updatePasswordView
#Description: This method is responsible for updating password
#"""
@login_required
def updatePasswordView(request):
    pwd = updatePasswordForm()
    user = request.user
    context=RequestContext(request,
        {
            'title':'Please Update Your Password',
            'message':'Update',
            'year':datetime.now().year,
            'pwd':pwd,
            'requestscount':borrowViews.countfunction(request.user.id),
        })
    if request.method == 'POST':
        pwd = updatePasswordForm(request.POST)
        if user.check_password(request.POST['oldPassword']):
            if pwd.is_valid():
                user.set_password(request.POST['newPassword'])
                user.save()
                context['msg']='Your new password is saved.'
            else:
                context['msg'] = 'Passwords do not match.'       
        else:
            context['msg']='Your old password is incorrect'
       
    return render(
        request,
        'app/password_update_form.html',
        context_instance = context,
        
    )