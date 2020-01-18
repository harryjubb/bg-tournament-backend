from django.contrib import admin
from tournament.apps.game.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
