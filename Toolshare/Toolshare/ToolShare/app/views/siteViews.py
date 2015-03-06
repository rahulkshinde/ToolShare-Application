#"""
#Name: siteViews
#Description: This file is responsible for rendering home page functionalities
#"""
import sys
from django.shortcuts import render, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Shed,Tools
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.views import borrowViews
#===================== Ibrahim Section ===============================  
#"""
#Method Name: home
#Description: This method is responsible for rendering the home page
#"""                                     
@csrf_exempt 
def home(request):
    """Renders the home page."""
    if request.user.is_authenticated():
         requestcount=borrowViews.countfunction(request.user.id)
    else:
         requestcount='none'
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'requestscount':requestcount,
        })
    )

def contact(request):
    """Renders the contact page."""
    if request.user.is_authenticated():
         requestcount=borrowViews.countfunction(request.user.id)
    else:
         requestcount='none'
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
             'requestscount':requestcount,
        })
    )

def about(request):
   
    """Renders the about page."""
    if request.user.is_authenticated():
         requestcount=borrowViews.countfunction(request.user.id)
    else:
         requestcount='none'
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'requestscount':requestcount,
        })
    )

