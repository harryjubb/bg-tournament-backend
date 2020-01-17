from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
