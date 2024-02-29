from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("<int:id>", login_required(views.index, login_url='login'), name="index"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("", views.HomeView.as_view()),
    path("view/", login_required(views.ToDoListView.as_view(), login_url='login'), name="view"),
]
