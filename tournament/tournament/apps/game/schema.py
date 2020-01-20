from graphene_django import DjangoObjectType
import graphene

from tournament.apps.game.models import Game


class GameType(DjangoObjectType):
    class Meta:
        model = Game
