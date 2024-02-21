from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out")
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
    
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
        
    return render(request, "registration/login.html", {"form": form})
