from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth import views
from hello.forms import LoginForm
import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', hello.views.home, name='home'),      #we are changing this to home for now
    url(r'^db', hello.views.db, name='db'),
    #url(r'^login', hello.views.login, name='login'),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
]
