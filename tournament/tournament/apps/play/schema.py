from graphene_django import DjangoObjectType
import graphene

from tournament.apps.play.models import Play


class PlayType(DjangoObjectType):
    class Meta:
        model = Play

    score = graphene.Float()
    players = graphene.List("tournament.apps.player.schema.PlayerType")

    def resolve_score(self, info):
        return self.score
