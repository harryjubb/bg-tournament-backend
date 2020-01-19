from django.contrib import admin
from tournament.apps.play.models import Play


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("winners", "losers")
    readonly_fields = ("score",)
