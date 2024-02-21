from django.urls import path
from . import views

urlpatterns = [
    path('logout_user', views.logout_user, name='logout'),
    path('login', views.login_user, name='login')
]
