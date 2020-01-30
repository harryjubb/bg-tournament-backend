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


# TODO: Add mutation for adding a play (Harry Jubb, Thu 30 Jan 2020 00:31:47 GMT)
# class AddPlay(graphene.Mutation):
#     class Arguments:
#         event_id =
