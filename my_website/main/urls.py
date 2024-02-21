from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.HomeView.as_view(), name="home"),
    path("view/", views.ToDoListView.as_view(), name="view"),
]
