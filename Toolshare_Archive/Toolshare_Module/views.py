from django.http import HttpResponse,Http404
from django.template import Template,Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response,RequestContext
from django.template.defaulttags import csrf_token
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def main_page(request):
    return render_to_response('main_page.html',RequestContext(request)
                              )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

# Create your views here.
