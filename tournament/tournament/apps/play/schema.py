import requests

from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene

from tournament.apps.play.models import Play
from tournament.apps.event.models import Event
from tournament.apps.game.models import Game
from tournament.apps.player.models import Player

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from tournament.apps.event.exceptions import EventInactiveError

channel_layer = get_channel_layer()


class PlayType(DjangoObjectType):
    class Meta:
        model = Play

    score = graphene.Float()
    players = graphene.List("tournament.apps.player.schema.PlayerType")

    def resolve_score(self, info):
        return self.score


class AddPlay(graphene.Mutation):
    class Arguments:
        event_id = graphene.UUID(required=True)
        game_id = graphene.UUID(required=True)
        winner_ids = graphene.List(graphene.UUID, required=True)
        loser_ids = graphene.List(graphene.UUID, required=True)

    ok = graphene.Boolean()
    play = graphene.Field(lambda: PlayType)

    def mutate(
        self, info, event_id=None, game_id=None, winner_ids=None, loser_ids=None
    ):

        if any([arg is None for arg in [event_id, game_id, winner_ids, loser_ids]]):
            raise GraphQLError(f"Missing required IDs")

        event = Event.objects.get(id=event_id)

        if not event.active:
            raise EventInactiveError("Cannot add a play to an inactive event")

        game = Game.objects.get(id=game_id)
        winners = Player.objects.filter(id__in=winner_ids).distinct()
        losers = Player.objects.filter(id__in=loser_ids).distinct()

        play = Play.objects.create(event=event, game=game)

        play.winners.set(winners)
        play.losers.set(losers)

        play.save()

        async_to_sync(channel_layer.group_send)(
            f"event_{play.event.code}", {"type": "play.added"}
        )

        # Fire custom webhooks
        for webhook in play.event.webhook_set.all():

            content = webhook.content.replace("%%play_summary%%", str(play))

            try:
                requests.request(
                    webhook.request_type,
                    webhook.url,
                    headers={"Content-Type": webhook.content_type},
                    data=content.encode("utf-8"),
                )
            except Exception as error:
                pass

        return AddPlay(ok=True, play=play)


class Mutation:
    add_play = AddPlay.Field(description="Add a play of a game to an event.")
