from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Requis.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Requis.')
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )