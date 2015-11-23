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
                       url(r'^logout/', views.user_logout),

                       url(r'^accounts/login/$', views.user_login),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^profile/', views.profile),
                       url(r'^patients/$', views.list_patients),
                       url(r'^patients/patient', views.patient),
                       url(r'^patients/create', views.create_patient),
                       url(r'^patients/validateCode', views.validate_patient_code),
                       url(r'^patients/testResult', views.test_result),
                       url(r'^sendTestResult', views.send_test_result),
                       url(r'^crossdomain', views.crossdomain)
                       )
