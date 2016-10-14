from django.shortcuts import render

# Create your views here.
#views.py
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from symantec_package import HTTPHandler

global transactionId
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )

def send_code(request):
        global transactionId
        url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-auth-1.7.wsdl'


        client = HTTPHandler.setConnection(url)


        push_results = client.service.authenticateUserWithPush(requestId='189392', userId='y1196293')
        info_list = str(push_results).split('\n')
        for item in info_list:
            if 'transactionId' in item:
                transactionId = item.split('=')[1][1:][1:-1]
        urls = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        clients = HTTPHandler.setConnection(urls)

        while 1:
            push_res = clients.service.pollPushStatus(requestId='13498345', transactionId=transactionId)
            if ("approved" in str(push_res)):
                return HttpResponse("Succeed")
        return HttpResponseRedirect("/home")

def confirm_code(request):
    urls = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
    clients = HTTPHandler.setConnection(urls)
    push_res = clients.service.pollPushStatus(requestId='13498345', transactionId=transactionId)
    if("approved" in str(push_res)):
        return HttpResponse("Succeed")
    else:
        return HttpResponse("Failed")

