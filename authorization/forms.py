from django import forms
from django.forms import inlineformset_factory
from .models import CustomUser
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.contrib.admin import widgets
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
import datetime



class CustomUserForm(forms.ModelForm): 
    
    class Meta:
        model = CustomUser
        exclude = ['user', 'activation_key', 'key_expires']

        widgets={
            "birthday": forms.DateInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
            "country": forms.TextInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
            "city": forms.TextInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
        }

    def save(self, data):
        user = User.objects.get(id=data["user"])
        data["user"] = user

        custom_user = CustomUser.objects.create(**data)
 
        custom_user.save()
        
        return custom_user

    def sendEmail(self, data):
        # link="http://http://127.0.0.1:8000/activate/"+data['activation_key']
        link="https://agile-falls-95273.herokuapp.com/activate/"+datas['activation_key']
        user = User.objects.get(id=data["user"])
        
        message="to activate account go to link %s"%link
        
        send_mail("Activation user", message, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)

class UserSignUpForm(forms.ModelForm):

    confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "", 
                'class': 'w3-input w3-border'
                }
            )
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm')

        widgets={
            "username": forms.TextInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
            "email": forms.EmailInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
            "password": forms.PasswordInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
        }
        help_texts = {
            'email': None,
        }



    def is_valid(self):
 
        valid = super(UserSignUpForm, self).is_valid()
 
        if not valid:
            return valid

        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            return False

        return valid

    def save(self, data):
        user = User.objects.create_user(**data)
        user.is_active = False
        user.save()
        print(user)
        return user

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = ''

class UserSignInForm(forms.ModelForm): 
    

    class Meta:
        model = User
        fields = ('email', 'password')

        widgets={
            "password": forms.PasswordInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'}),
            "email": forms.EmailInput(attrs={'placeholder': "", 'class': 'w3-input w3-border'})
        }
        help_texts = {
            'email': None,
        }
    