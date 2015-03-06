"""
Definition of urls for DjangoWebProject3.
"""
from app.views import *
from datetime import datetime
from django.conf.urls import patterns, url,include
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    #============= site views  ============================================
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.siteViews.home', name='home'),
    url(r'^contact$', 'app.views.siteViews.contact', name='contact'),
    url(r'^about', 'app.views.siteViews.about', name='about'),

    #============= Shed Views  =============================================
    url(r'^createShed', 'app.views.shedViews.createShed', name='createShed'),
    url(r'^shedTable', 'app.views.shedViews.shedTable', name='shedTable'),
    url(r'^Shed', 'app.views.shedViews.ShedView', name='Shed'),
    #======================borrow view =================================
    #url(r'^borrowingrequest','app.views.requestview', name='borrowingrequest'),
    url(r'^sheddetails/(?P<shedid>\d+)$', 'app.views.shedViews.readSheddetails', name='sheddetails'),
    #============= User Views  =============================================
    url(r'^createuser', 'app.views.userViews.createUser', name='createuser'),
    url(r'^signup', 'app.views.userViews.Usersignup', name='signup'),
    url(r'^profile', 'app.views.userViews.profileview', name='profile'),
    url(r'^preference', 'app.views.userViews.preferenceview', name='preference'),
    url(r'^usertable', 'app.views.userViews.myprofile', name='usertable'),
    url(r'^userprofile/(?P<userid>\d+)$', 'app.views.userViews.userprofile', name='userprofile'),
    url(r'^password_change_form', 'app.views.userViews.resetPasswordView', name='password_change_form'),
    url(r'^password_update_form', 'app.views.userViews.updatePasswordView', name='password_update_form'),

    #============= Tool Views  =============================================
   url(r'^registerTool', 'app.views.toolViews.registerTool', name='registerTool'),
   url(r'^addtool', 'app.views.toolViews.Addtool', name='addtool'),
   url(r'^ToolStatistics', 'app.views.statisticsViews.MostActiveToolView', name='MostActiveTool'),
   url(r'^UserStatistics', 'app.views.statisticsViews.MostActiveUserView', name='MostActiveUser'),
   url(r'^tooldetails/(?P<toolid>\d+)$', 'app.views.toolViews.readTooldetails', name='tooldetails'),
   url(r'^mytooldetails/(?P<toolid>\d+)$', 'app.views.toolViews.readmyTooldetails', name='mytooldetails'),
   url(r'^updatemyTooldetails/(?P<toolid>\d+)$', 'app.views.toolViews.updatemyTooldetails', name='updatemyTooldetails'),
   url(r'^toollist', 'app.views.toolViews.toolList', name='toollist'),
   url(r'^mytools', 'app.views.toolViews.myTools', name='mytools'),

   #============= Boorow tool  =============================================
   url(r'^requesttool/(?P<toolid>\d+)$', 'app.views.borrowViews.requesttool', name='requesttool'),
   url(r'^mynotification1$', 'app.views.borrowViews.mynotifications1', name='mynotification1'),
   url(r'^mynotification2$', 'app.views.borrowViews.mynotifications2', name='mynotification2'),
   url(r'^mynotification3$', 'app.views.borrowViews.mynotifications3', name='mynotification3'),
   url(r'^MyHistory$', 'app.views.borrowViews.myhistory', name='MyHistory'),

   url(r'^requestupdate/(?P<requestid>\d+)$', 'app.views.borrowViews.requestAction', name='requestAction'),


   url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
