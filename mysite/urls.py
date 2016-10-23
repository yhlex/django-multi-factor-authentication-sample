
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.views import *
from login.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^home/$', home),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^accounts/login/$', login),
    url(r'^logout/$', logout_page),
    url(r'^sent/$',send_code),
    url(r'^send_6_otp/$', send_6_otp, name='send_6_otp'),
    url(r'^getting_started_symantec/$', getting_started_symantec, name='getting_started_symantec'),
    url(r'^user_creation/$', create_user, name='create_user'),
    url(r'^send_sms/$',send_sms, name='send_sms'),
    url(r'^check_sms/$',check_sms, name='check_sms'),
    url(r'^result/$',confirm_code)




]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
