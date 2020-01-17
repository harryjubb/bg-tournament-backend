from django.db import models
from tournament.apps.player.models import Player


class Event(models.Model):
    code = models.CharField(max_length=10)

    players = models.ManyToManyField(Player)

    def __str__(self):
        return f"Event {self.code}"
