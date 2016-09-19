from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .models import Greeting

def login(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'login.html', {'greetings': greetings})

# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
    print ("Hello World")
    #return HttpResponse('<pre>' + 'Hello World' + '</pre>')
    return render(request,"home.html")


# Create your views here.
def index(request):
    print ("Hello World")
    return HttpResponse('<pre>' + 'Hello World' + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
