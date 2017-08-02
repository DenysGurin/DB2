from django import forms
from django.forms import TextInput, inlineformset_factory
from .models import Comment
# from main.models import 
from django.contrib.admin import widgets
# from django.forms.widgets import PasswordInput



class SearchForm(forms.Form):

    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'w3-input w3-border',
                                                           'id': "search",
                                                           'placeholder': "search",
                                                           'style': "border:none; outline: none",
                                                           'autofocus': "none"}))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': TextInput(attrs={
                    # 'class': 'w3-input w3-border w3-border-white', 
                    'placeholder': "comment",
            })
        }
    