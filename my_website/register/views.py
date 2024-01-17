from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect("/home")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out")
    return redirect('/home')
