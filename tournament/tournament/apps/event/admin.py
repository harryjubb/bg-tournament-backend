from django.contrib import admin
from tournament.apps.event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
