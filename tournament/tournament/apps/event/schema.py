from graphene_django import DjangoObjectType
import graphene

from tournament.apps.event.models import Event
from tournament.apps.play.schema import PlayType
from tournament.apps.game.schema import GameType
from tournament.apps.player.schema import PlayerType


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):
    event = graphene.Field(
        EventType,
        code=graphene.String(),
        description="Retrieve an event by an event code",
    )

    def resolve_event(self, info, code):
        return Event.objects.get(code=code)
