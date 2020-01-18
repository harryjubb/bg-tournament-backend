from django.db import models

from datetime import timedelta


class Game(models.Model):
    name = models.CharField(max_length=1024)
    min_length = models.DurationField(default=timedelta)
    max_length = models.DurationField(default=timedelta)
    complexity = models.DecimalField(max_digits=3, decimal_places=2)
    min_players = models.SmallIntegerField()
    max_players = models.SmallIntegerField()
    image_url = models.URLField(max_length=4000)
    bgg_id = models.IntegerField()

    def __str__(self):
        return self.name
