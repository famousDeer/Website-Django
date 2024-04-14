from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View

from .models import Board_Games
from utils.messages import Message

# Create your views here.

class BoardGame(View):
    template_name = "board_games.html"
    view_name = 'board-games'
    message = Message()

    def get(self, request):
        return render(request, self.template_name)