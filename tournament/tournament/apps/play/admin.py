from django.contrib import admin
from tournament.apps.play.models import Play


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("winners", "losers")
    list_display = ("__str__", "event", "date_created", "date_updated", "score")
    list_filter = (
        "event",
        "date_created",
        "date_updated",
        "winners",
        "losers",
    )
    readonly_fields = ("score", "date_created", "date_updated")
