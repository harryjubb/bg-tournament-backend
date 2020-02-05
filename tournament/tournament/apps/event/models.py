import uuid
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=10, unique=True)

    players = models.ManyToManyField("player.Player")

    def __str__(self):
        return f"Event {self.code}"

    def save(self, *args, **kwargs):

        # Force all event codes to be uppercase
        self.code = self.code.upper()
        super().save(*args, **kwargs)
