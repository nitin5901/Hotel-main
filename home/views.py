from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.forms import AuthenticationForm

from .models import person
from .forms import UserForm, RegisterForm


from twilio.rest import Client as TwilioClient
from decouple import config
import os
from twilio.http.http_client import TwilioHttpClient


#proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone = config("TWILIO_PHONE")
#client = TwilioClient(account_sid, auth_token, http_client=proxy_client)
client = TwilioClient(account_sid, auth_token)




def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def admin_page(request):
    return render(request, 'admin_page.html')


def booking(request):
    client.messages.create(
        body="Your verification code is lalala. -Pragati Tandon :)",
        from_=twilio_phone,
        to= '+919314538380'
    )
    return render(request, 'book_table.html')


def rating(request):
    return render(request, 'rating.html')


def login_request(request):
    message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = "Success: You are now logged in. "
                uss = request.user
                prsn = person.objects.get(user=uss)
                return render(request, 'index.html',{"message": message,"prsn": prsn,})
            else:
                message = "Error: Invalid Username or Password."
        else:
            message = "Error: Invalid Username or Password."
    form = AuthenticationForm()
    context = {"form": form, "message": message, }
    return render(  request = request, template_name = "home/login.html", context=context)



def register(request):
    form1 = RegisterForm()
    if request.method == 'POST':
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password', None)
        userMail = request.POST.get('email', None)
        user1 = User.objects.create_user(username=userName, password=userPass, email=userMail)
        form1 = RegisterForm(request.POST)
        if form1.is_valid() :
            prs = form1.save(False)
            prs.user = user1
            form1.save(True)
            return render(request, 'index.html' )
        message = 'ERROR !! Could not register. Please try again. '
        return render(request,  'index.html', {'message': message })
    return render(request, 'home/register.html')



def logout_request(request):
    logout(request)
    message = "Logged out successfully!"
    return render(request, 'index.html', {"message": message, })

