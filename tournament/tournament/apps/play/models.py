from django.db import models


class Play(models.Model):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    winners = models.ManyToManyField("player.Player", related_name="won_plays")
    losers = models.ManyToManyField("player.Player", related_name="lost_plays")

    def __str__(self):
        return f"Play of {self.game.name} at {self.event.code} won by {', '.join(winner.name for winner in self.winners.all())}"
