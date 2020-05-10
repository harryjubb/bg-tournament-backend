import uuid
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=False)

    players = models.ManyToManyField("player.Player")

    def __str__(self):
        return f"Event {self.code}"

    def save(self, *args, **kwargs):

        # Force all event codes to be uppercase
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class Webhook(models.Model):
    """
    Webhooks called on event play additions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)

    name = models.CharField(max_length=1024)
    url = models.URLField(max_length=8192)
    request_type = models.CharField(
        choices=[("POST", "POST")], default="POST", max_length=10
    )
    content_type = models.CharField(max_length=1024, default="application/json")
    content = models.TextField(
        help_text="POST body content. Play data can be interpolated with: %%play_summary%%",
        null=True,
        blank=True,
    )
