from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Database

class Board_Games(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board_games")
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=32)
    played_counter = models.IntegerField(default=0)
    