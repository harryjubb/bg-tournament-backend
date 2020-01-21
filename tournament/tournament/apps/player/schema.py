from django.db.models import Q

from graphene_django import DjangoObjectType
import graphene

from tournament.apps.player.models import Player


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ("id", "name")

    event_play_count = graphene.Int(
        event_code=graphene.String(required=True),
        description="Retrieve the number of plays for a given event code for this player.",
    )

    event_win_count = graphene.Int(
        event_code=graphene.String(required=True),
        description="Retrieve the number of wins for a given event code for this player.",
    )

    event_loss_count = graphene.Int(
        event_code=graphene.String(required=True),
        description="Retrieve the number of losses for a given event code for this player.",
    )

    event_plays = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(required=True),
        description="Retrieve plays for a given event code for this player.",
    )

    event_wins = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(required=True),
        description="Retrieve plays for a given event code that this player won.",
    )

    event_losses = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(required=True),
        description="Retrieve plays for a given event code that this player lost.",
    )

    event_total_score = graphene.Float(
        event_code=graphene.String(required=True),
        description="Retrieve the total score accrued for a given event code for this player.",
    )

    def resolve_event_play_count(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(Q(Q(winners__id=self.id) | Q(losers__id=self.id)))
            .distinct()
            .count()
        )

    def resolve_event_win_count(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(winners__id=self.id)
            .distinct()
            .count()
        )

    def resolve_event_loss_count(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(losers__id=self.id)
            .distinct()
            .count()
        )

    def resolve_event_plays(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(Q(Q(winners__id=self.id) | Q(losers__id=self.id)))
            .distinct()
        )

    def resolve_event_wins(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(winners__id=self.id)
            .distinct()
        )

    def resolve_event_losses(self, info, event_code=None):
        return (
            self.event_set.get(code=event_code)
            .play_set.filter(losers__id=self.id)
            .distinct()
        )

    def resolve_event_total_score(self, info, event_code=None):
        return sum(
            play.score
            for play in self.event_set.get(code=event_code)
            .play_set.filter(winners__id=self.id)
            .distinct()
        )
