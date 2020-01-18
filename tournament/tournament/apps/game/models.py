from django.db import models

from datetime import timedelta

from tournament.apps.game.utils import get_bgg_data

DEFAULTS = {
    "name": "Name",
    "game_type": "boardgame",
    "min_age": 0,
    "min_length": timedelta(minutes=5),
    "max_length": timedelta(minutes=10),
    "complexity": 2.0,
    "min_players": 2,
    "max_players": 5,
    "url": "https://google.com",
    "image_url": "https://via.placeholder.com/128",
}


class Game(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    game_type = models.CharField(
        max_length=100,
        choices=(("boardgame", "Board Game"), ("videogame", "Video Game")),
        blank=True,
    )
    min_age = models.SmallIntegerField(blank=True)
    min_length = models.DurationField(blank=True)
    max_length = models.DurationField(blank=True)
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
        bgg_item = get_bgg_data(self.bgg_id)

        for field in (
            "name",
            "game_type",
            "min_age",
            "min_length",
            "max_length",
            "complexity",
            "min_players",
            "max_players",
            "url",
            "image_url",
        ):
            if (
                getattr(self, field) is None or getattr(self, field) == ""
            ) and bgg_item[field] is not None:
                setattr(self, field, bgg_item[field])
            elif (
                getattr(self, field) is None or getattr(self, field) == ""
            ) and bgg_item[field] is None:
                setattr(self, field, DEFAULTS[field])
            else:
                pass

        super().save(*args, **kwargs)
