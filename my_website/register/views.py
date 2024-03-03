from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views import View

from .forms import RegisterForm, LoginForm
from utils.messages import Message
# Create your views here.

class RegisterView(View):
    template_name = "register/register.html"
    view_name = "home"
    message = Message()

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(self.view_name)
        return render(request, self.template_name, {"form": form})
        
    
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    view_name = "home"
    message = Message()

    def get(self, request):
        logout(request)
        self.message.success(request,"Logout successfully")
        return redirect(self.view_name)

class LoginView(View):
    template_name = "registration/login.html"
    view_name = "home"
    message = Message()

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(self.request.GET.get('next'))
                return redirect(self.view_name)
            else:
                self.message.error(request, "Invalid username or password")
        return render(request, "registration/login.html", {"form": form})

    def get(self, request):
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})
