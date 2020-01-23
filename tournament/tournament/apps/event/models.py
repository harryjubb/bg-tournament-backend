from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=10, unique=True)

    players = models.ManyToManyField("player.Player")

    def __str__(self):
        return f"Event {self.code}"
