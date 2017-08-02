from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .forms import CustomUserForm, UserSignUpForm, UserSignInForm
from .models import CustomUser
import hashlib
import random
import datetime


class SignIn(View):


    def get(self, request):
        print(request.user)
        user_sign_in_form = UserSignInForm()
    
        return render(request, "sign_in.html", {"user_sign_in_form":user_sign_in_form})

    def post(self, request):
        if request.POST.get("submit"):

            user_sign_in_form = UserSignInForm(data=request.POST)
            
            if user_sign_in_form.is_valid():

                user_data = user_sign_in_form.cleaned_data
                user = authenticate(request, **user_data)
                
                if user:
                    login(request, user)

        return redirect('/')

class SignUp(View):


    def get(self, request):

        print(request.user)
        user_sign_up_form = UserSignUpForm()
        custom_user_form = CustomUserForm()
        
        return render(request, "sign_up.html", {"custom_user_form":custom_user_form, "user_sign_up_form":user_sign_up_form,})

    def post(self, request):
        if request.POST.get("submit"):
            user_sign_up_form = UserSignUpForm(data=request.POST)
            custom_user_form = CustomUserForm(data=request.POST)
            print(user_sign_up_form.is_valid() and custom_user_form.is_valid())
            if user_sign_up_form.is_valid() and custom_user_form.is_valid():
                user_data = user_sign_up_form.cleaned_data
                custom_user_data = custom_user_form.cleaned_data

                salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                usernamesalt = user_data['username']

                # if isinstance(usernamesalt, str):
                # usernamesalt = usernamesalt.decode("utf-8")

                custom_user_data['activation_key']= hashlib.sha1((salt+usernamesalt).encode('utf-8')).hexdigest()
                custom_user_data['key_expires'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
                

                del user_data['confirm']
                user = user_sign_up_form.save(user_data)
                print(user)
                custom_user_data["user"] = user.id
                # custom_user_data["user_id"] = user.id
                print(custom_user_data)
                custom_user_form.sendEmail(custom_user_data)
                custom_user = custom_user_form.save(custom_user_data)
                print("this is custom user: %s"%custom_user)
                # request.session['registered']=True #For display purposes
        return redirect("/")


# class SignIn(View):


#     def get(self, request):

#         print(request.user)
#         authentication_form = MyAuthenticationForm()
    
#         return render(request, "sign_in.html", {"authentication_form":authentication_form})

#     def post(self, request):
#         # if request.POST.get("submit") == "submit":

#         authentication_form = MyAuthenticationForm(data=request.POST)
#         print(authentication_form.is_valid())
#         if authentication_form.is_valid():
            
#             user_data = authentication_form.cleaned_data
#             print(user_data)
#             user = authenticate(request, **user_data)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/')
#             return HttpResponse(user)
#         else:
#             return HttpResponse(authentication_form)

#         return redirect('/')

class SignOut(View):


    def get(self, request):

        print(request.user)
        logout(request)
    
        return redirect('/sign_in/')


def activation(request, key):
    print(CustomUser.objects.all().count())
    for u in CustomUser.objects.all():
        print(u.activation_key)
    custom_user = get_object_or_404(CustomUser, activation_key=key)
    if custom_user.user.is_active == False:
        if timezone.now() > custom_user.key_expires:
            
            id_user = custom_user.user.id
        else: #Activation successful
            custom_user.user.is_active = True
            custom_user.user.save()

    return redirect('/sign_in/')