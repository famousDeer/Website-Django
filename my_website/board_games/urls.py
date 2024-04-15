from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('board-games/add-game', login_required(views.AddGame.as_view(), login_url='login'), name='add-game'),
    path('board-games/list-game', login_required(views.ListView.as_view(), login_url='login'), name='list-game'),
]