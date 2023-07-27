from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

#login form class
class LoginForm(forms.Form):
  
    username = forms.CharField(
    label='Username', 
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
    label='Password', 
    max_length=100,
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#register form for user
class CreateUserForm(forms.Form):

    username = forms.CharField(
    label='Username', 
    max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
    label='Email', 
    max_length=100,
    widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
    label='Password', 
    max_length=100,
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
    label='Confirm Password', 
    max_length=100,
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            #raise forms.ValidationError("Passwords does not match.")
            self.add_error('password2', "Passwords do not match.")
        
        return cleaned_data

