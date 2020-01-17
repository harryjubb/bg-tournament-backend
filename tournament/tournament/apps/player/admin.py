from django.contrib import admin
from tournament.apps.player.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
