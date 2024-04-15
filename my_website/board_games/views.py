from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View

from .models import Board_Games, User
from utils.messages import Message

# Create your views here.

class AddGame(View):
    template_name = "add_game.html"
    view_name = 'add-game'
    message = Message()

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        bg_name = request.POST.get("bg_name")
        bg_category = request.POST.get("bg_category")
        board_game = Board_Games.objects.create(user=user,
                                                name=bg_name,
                                                category=bg_category)
        board_game.save()

        return redirect(reverse(self.view_name))

class ListView(View):
    template_name = "list.html"
    view_name = 'list-game'
    
    def get(self, request):
        return render(request, self.template_name)