from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from tournament.apps.play.utils import score_play

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

from asgiref.sync import async_to_sync


class Play(models.Model):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    winners = models.ManyToManyField("player.Player", related_name="won_plays")
    losers = models.ManyToManyField("player.Player", related_name="lost_plays")

    @property
    def players(self):
        return (self.winners.all() | self.losers.all()).distinct()

    @property
    def score(self):
        return score_play(
            game_min_length=self.game.min_length,
            game_complexity=self.game.complexity,
            num_winners=self.winners.count(),
            num_losers=self.losers.count(),
        )

    def __str__(self):
        return f"{self.winners.count() + self.losers.count()} player {self.game.name} at {self.event.code} won by {', '.join(winner.name for winner in self.winners.all())}, scoring {self.score:.2f} per winner"


@receiver(post_save, sender=Play)
def play_post_save(sender, instance, **kwargs):
    # Push to event websocket group here
    async_to_sync(channel_layer.group_send)(
        f"event_{instance.event.code}", {"type": "play.added"}
    )
