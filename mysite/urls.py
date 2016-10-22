
from django.conf.urls import url, include, patterns
from django.contrib import admin
from login.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^home/$', home),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^sent/$','login.views.send_code'),
    url(r'^send_6_otp/$','login.views.send_6_otp', name='send_6_otp'),
    url(r'^send_sms/$','login.views.send_sms', name='send_sms'),
    url(r'^check_sms/$','login.views.check_sms', name='check_sms'),
    url(r'^result/$','login.views.confirm_code')




]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
