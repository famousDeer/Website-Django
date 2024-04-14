from django.urls import path
from . import views

urlpatterns = [
    path('board-games', views.BoardGame.as_view(), name='board-games'),
]