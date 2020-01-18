from django.db import models

from datetime import timedelta


class Game(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    min_length = models.DurationField(default=timedelta, blank=True)
    max_length = models.DurationField(default=timedelta, blank=True)
    complexity = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    min_players = models.SmallIntegerField(blank=True)
    max_players = models.SmallIntegerField(blank=True)
    url = models.URLField(max_length=4000, blank=True)
    image_url = models.URLField(max_length=4000, blank=True)
    bgg_id = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Get data from BGG API if available

        super().save(*args, **kwargs)
