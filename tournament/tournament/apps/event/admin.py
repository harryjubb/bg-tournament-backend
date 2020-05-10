from django.contrib import admin
from tournament.apps.event.models import Event, Webhook
from tournament.apps.play.models import Play


class PlayInline(admin.TabularInline):
    model = Play


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [PlayInline]
    filter_horizontal = ("players",)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    pass
