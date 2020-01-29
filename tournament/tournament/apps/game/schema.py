from graphene_django import DjangoObjectType
import graphene

from tournament.apps.game.models import Game


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class Query(graphene.ObjectType):
    games = graphene.List(GameType, description="Retrieve all available games",)

    def resolve_games(self, info):
        return Game.objects.all()
