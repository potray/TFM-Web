from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tfm.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', views.index),
                       url(r'^registration/', views.registration),
                       url(r'^login/', views.user_login),
                       url(r'^accounts/login/$', views.user_login),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^profile/', views.profile),
                       )
