from django.urls import path
from . import views

urlpatterns = [
    path('logout_user', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login')
]
