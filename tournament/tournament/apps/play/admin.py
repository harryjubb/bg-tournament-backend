from django.contrib import admin
from tournament.apps.play.models import Play


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("winners", "losers")
    list_display = ("__str__", "date_created", "date_updated", "score")
    list_filter = (
        "date_created",
        "date_updated",
        "game",
        "event",
        "winners",
        "losers",
    )
    readonly_fields = ("score", "date_created", "date_updated")
