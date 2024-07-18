from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
# Create your views here.
from .forms import UserRegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Please enter correct username and password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/users/login')