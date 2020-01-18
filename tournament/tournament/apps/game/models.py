from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=1024)
    length = models.DurationField()
    complexity = models.SmallIntegerField()
    min_players = models.SmallIntegerField()
    max_players = models.SmallIntegerField()
    image_url = models.URLField(max_length=4000)
    bgg_id = models.IntegerField()

    def __str__(self):
        return self.name
