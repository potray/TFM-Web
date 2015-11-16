from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tfm.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^main/', views.index),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),

                       )
