import graphene

import tournament.apps.event.schema


class Query(
    tournament.apps.event.schema.Query,
    tournament.apps.game.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
