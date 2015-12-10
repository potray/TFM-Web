from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

import views
from tfm import settings

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^registration/', views.registration),
                       url(r'^login/', views.index),
                       url(r'^logout/', views.user_logout),
                       url(r'^crossdomain', views.crossdomain),
                       url(r'^accounts/login/$', views.index),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^notifications/', views.notifications),
                       url(r'^patients/$', views.list_patients),
                       url(r'^patients/patient', views.patient),
                       url(r'^patients/create', views.create_patient),
                       url(r'^patients/settings', views.patient_settings),
                       url(r'^patients/validateCode', views.validate_patient_code),
                       url(r'^patients/testResult', views.test_result),
                       url(r'^sendTestResult', views.send_test_result),
                       )


# Media URLs
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
