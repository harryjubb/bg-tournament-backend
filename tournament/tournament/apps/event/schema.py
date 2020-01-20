from graphene_django import DjangoObjectType
import graphene

from tournament.apps.event.models import Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):
    event = graphene.Field(EventType, description="Retrieve an event by event code")

    def resolve_users(self, info):
        return UserModel.objects.all()


schema = graphene.Schema(query=Query)
