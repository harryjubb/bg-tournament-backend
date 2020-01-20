from django.db.models import Q

from graphene_django import DjangoObjectType
import graphene

from tournament.apps.player.models import Player


class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        fields = ("id", "name")

    event_plays = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(),
        description="Retrieve plays for a given event code for this player.",
    )

    event_wins = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(),
        description="Retrieve plays for a given event code that this player won.",
    )

    event_losses = graphene.List(
        "tournament.apps.play.schema.PlayType",
        event_code=graphene.String(),
        description="Retrieve plays for a given event code that this player lost.",
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
