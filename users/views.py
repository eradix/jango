from django.shortcuts import render, redirect
from .forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# for displaying login form and logging in user
def login_user(request):
    #redirects back the user to home page if user is currently logged in
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username =  login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request,'Successfully log in, {}'.format(username))
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')

    else:
        login_form = LoginForm() 

    context = {
        'title' : 'Sign in',
        'form' : login_form
    }

    return render(request, "auth/login.html", context)


@require_POST
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'Log out successfully.')
    return redirect('login_user')

#method for registering new user and displaying register form
def create_user(request):
    
    #redirects back the user to home page if user is currently logged in
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username =  form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            #login user
            login(request, user)
            messages.success(request,'Successfully log in, {}'.format(username))
            return redirect('index')
    else:
        form = CreateUserForm()

    context = {
        'form' : form,
        'title' : 'Sign up'
    }

    return render(request, "auth/create.html", context)