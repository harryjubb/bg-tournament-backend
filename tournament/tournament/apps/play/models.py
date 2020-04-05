import uuid
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from tournament.apps.play.utils import score_play
from tournament.apps.event.exceptions import EventInactiveError

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

from asgiref.sync import async_to_sync


class Play(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    winners = models.ManyToManyField("player.Player", related_name="won_plays")
    losers = models.ManyToManyField("player.Player", related_name="lost_plays")

    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    @property
    def players(self):
        return (self.winners.all() | self.losers.all()).distinct()

    @property
    def score(self):
        """
        Score per-winner of this play.
        """
        return score_play(
            game_min_length=self.game.min_length,
            game_complexity=self.game.complexity,
            num_winners=self.winners.count(),
            num_losers=self.losers.count(),
        )

    def __str__(self):
        return f"{self.winners.count() + self.losers.count()} player {self.game.name} at {self.event.code} won by {', '.join(winner.name for winner in self.winners.all())}, scoring {self.score:.2f} per winner"

    def save(self, *args, **kwargs):

        if not self.event.active:
            raise EventInactiveError("Cannot save a play for an inactive event")

# @receiver(post_save, sender=Play)
# def play_post_save(sender, instance, **kwargs):
#     async_to_sync(channel_layer.group_send)(
#         f"event_{instance.event.code}", {"type": "play.added"}
#     )


@receiver(post_delete, sender=Play)
def play_post_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        f"event_{instance.event.code}", {"type": "play.deleted"}
    )
