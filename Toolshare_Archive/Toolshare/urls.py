from django.conf.urls import patterns, include, url
from django.contrib import admin
from Toolshare_Module.views import main_page,logout_page
import os.path

site_media = os.path.join(os.path.dirname(__file__),'site_media')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Toolshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main_page),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root': site_media}),
    url(r'^login/$','django.contrib.auth.views.login'),
    url(r'^logout/$',logout_page),
)
