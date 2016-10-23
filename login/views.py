from django.shortcuts import render

# Create your views here.
#views.py
from login.forms import *
from mysite.forms.SixDigitForm import SixDigitForm
from mysite.forms.SMSForm import SMSForm
from mysite.forms.NewSymantecUserForm import NewSymantecUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from symantec_package import HTTPHandler
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
from suds.client import Client

from django.shortcuts import render
global transactionId


import string
import random
import time

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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
            #return HttpResponseRedirect('/register/success/',  context_instance=RequestContext(request))
            return render(request,'registration/success.html')
    else:
        form = RegistrationForm()
        variables = {'form': form }

        return render(request, 'registration/register.html', variables)
    # return render_to_response(
    # 'registration/register.html',
    # variables,
    # )

@csrf_protect
def register_success(request):
    return render_to_response('registration/success.html', context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
# def home(request):
#     form = SixDigitForm()
#
#     csrfContext = RequestContext(request)
#     return render_to_response(
#     'home.html',
#     { 'user': request.user, 'form': form }, csrfContext
#     )
def home(request):
    forms = SMSForm()
    form = SixDigitForm()

    csrfContext = RequestContext(request)
    return render_to_response(
    'home.html',
    { 'user': request.user, 'forms': forms, 'form':form}, csrfContext
    )

@login_required
@csrf_protect
def getting_started_symantec(request):
    form = NewSymantecUserForm()

    csrfContext = RequestContext(request)
    variables = { 'form':form }
    return render(request, 'getting_started_symantec.html', variables)
    # return render_to_response(
    # 'getting_started_symantec.html',
    # { 'user': request.user, 'form':form }, context_instance=csrfContext
    # )

@csrf_protect
def create_user(request):
    managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'
    client = HTTPHandler.setConnection(managementservices_url)
    management_services_object = SymantecManagementServices(client)
    if (request.method == "POST"):
        form = NewSymantecUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            credential_id = form.cleaned_data["credential_id"]
            security_code = form.cleaned_data["security_code"]

            user_created = management_services_object.createUser(id_generator(), email)
            if ("0000" in str(user_created)):
                added_cred = management_services_object.addCredential(id_generator(), email, credential_id, "STANDARD_OTP",\
                                                                            security_code)
                if ("0000" in str(added_cred)):
                    return HttpResponse("GOOD!")
                else:
                    return HttpResponse("Failure...")
    pass

def send_code(request):
        global transactionId
        url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-auth-1.7.wsdl'


        client = HTTPHandler.setConnection(url)

        urls = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        clients = HTTPHandler.setConnection(urls)
        userService = SymantecUserServices(client)
        queryService = SymantecQueryServices(clients)

        push_results = client.service.authenticateUserWithPush(requestId='189392', userId=str(request.user))
        info_list = str(push_results).split('\n')
        for item in info_list:
            if 'transactionId' in item:
                transactionId = item.split('=')[1][1:][1:-1]

        while 1:
            push_res = clients.service.pollPushStatus(requestId='13498345', transactionId=transactionId)
            if ("approved" in str(push_res)):
                return render_to_response("succeed.html",)
        # if(authenticateUserWithPushThenPolling(userService,queryService, "Push_Test", "PushPollTest","Arren_phone")):
        #     return HttpResponse("Succeed")
        return HttpResponseRedirect("/home")

@csrf_protect
def send_6_otp(request):
    queryurl = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
    queryclient = HTTPHandler.setConnection(queryurl)
    queryService = SymantecQueryServices(queryclient)
    user_credentials = queryService.getUserInfo(id_generator(),request.user)[7]
    for item in user_credentials:
        credentialId = item[0]
    if (request.method == "POST"):
        form = SixDigitForm(request.POST)
        if form.is_valid():
            #post = form.save(commit=False)
            otp = form.cleaned_data["six_digit_code"]


            userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
            user_services_client = HTTPHandler.setConnection(userservices_url)

            user_service = SymantecUserServices(user_services_client)
            authenticate_result = user_service.authenticateWithStandard_OTP(id_generator(), credentialId, otp)
            if ("0000" in str(authenticate_result)):
                return render_to_response("succeed.html")
            else:
                return HttpResponse("Failure..." + str(request.user))
    else:
        return HttpResponse("what?!")

    pass


def confirm_code(request):
    urls = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
    clients = HTTPHandler.setConnection(urls)
    push_res = clients.service.pollPushStatus(requestId='13498345', transactionId=transactionId)
    if("approved" in str(push_res)):
        return HttpResponse("Succeed")
    else:
        return HttpResponse("Failed")


@csrf_protect
def send_sms(request):

    mgmturl = "http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-mgmt-1.7.wsdl"
    mgmtclient = HTTPHandler.setConnection(mgmturl)
    mgmtService = SymantecManagementServices(mgmtclient)

    authenticate = mgmtService.sendOtpSMS(id_generator(), str(request.user), "15177757651")
    return HttpResponseRedirect("/home")
    # if (request.method == "POST"):
    #     form = SMSForm(request.POST)
    #     if form.is_valid():
    #         # post = form.save(commit=False)
    #         sms = form.cleaned_data["sms_code"]
    #
    #
    #         time.sleep(10)
    #         authenticate_result = mgmtService.authenticateWithSMS(id_generator(), phoneNum, str(sms))
    #         if ("0000" in str(authenticate_result)):
    #             return HttpResponse("Success!" + str(request.user))
    #         else:
    #             return HttpResponse("Failure..." + str(request.user))
    # else:
    #     return HttpResponse("what?!")
    #
    # pass


@csrf_protect
def check_sms(request):
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
        user_services_client = HTTPHandler.setConnection(userservices_url)
        user_service = SymantecUserServices(user_services_client)
        queryurl = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        queryclient = HTTPHandler.setConnection(queryurl)
        queryService = SymantecQueryServices(queryclient)
        user_info = queryService.getUserInfo(id_generator(), request.user)
        user_credentials = user_info[7]
        for item in user_credentials:
            if "SMS" in item[1]:
                phoneNum = item[0]
        if (request.method == "POST"):

            form = SMSForm(request.POST)
            if form.is_valid():
                # post = form.save(commit=False)
                sms = form.cleaned_data["sms_code"]
                authenticate_result = user_service.authenticateWithSMS("CheckTest", "15177757651", sms)


                if ("0000" in str(authenticate_result)):
                    return render_to_response("succeed.html")
                else:
                    return HttpResponse("Failure..." + str(request.user) + phoneNum)
        else:
            return HttpResponse("what?!")

        pass
