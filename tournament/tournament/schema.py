import graphene

import tournament.apps.event.schema
import tournament.apps.game.schema
import tournament.apps.play.schema


class Query(
    tournament.apps.event.schema.Query,
    tournament.apps.game.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    tournament.apps.play.schema.Mutation, graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
