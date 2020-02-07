from graphene_django import DjangoObjectType
import graphene

from tournament.apps.event.models import Event
from tournament.apps.play.schema import PlayType
from tournament.apps.game.schema import GameType
from tournament.apps.player.schema import PlayerType


class EventType(DjangoObjectType):
    class Meta:
        model = Event

    recent_plays = graphene.List(
        PlayType, n=graphene.Int(), description="Recent plays in order of recency."
    )

    def resolve_recent_plays(self, info, n=5):
        return self.play_set.order_by("-date_created")[:n]


class Query(graphene.ObjectType):
    event = graphene.Field(
        EventType,
        code=graphene.String(required=True),
        description="Retrieve an event by an event code",
    )

    def resolve_event(self, info, code=None):
        return Event.objects.get(code=code)
