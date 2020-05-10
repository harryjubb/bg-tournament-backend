from operator import itemgetter
from typing import Optional
from urllib.parse import urljoin
import time

from asgiref.sync import sync_to_async

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from tournament.apps.event.models import Event

from discord.ext import commands


@sync_to_async
def get_event_leaderboard(event_code=None):

    event = None
    try:
        event = Event.objects.get(code=event_code)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        raise ValueError("Unable to find a leaderboard for this event.")

    if not event:
        raise ValueError("Unable to find a leaderboard for this event.")

    return {
        "event_name": event.name,
        "event_code": event.code,
        "leaderboard": sorted(
            [
                {
                    "name": player.name,
                    "score": sum(
                        play.score
                        for play in event.play_set.filter(
                            winners__id=player.id
                        ).distinct()
                    ),
                }
                for player in event.players.all()
            ],
            key=itemgetter("score"),
            reverse=True,
        ),
    }


@sync_to_async
def get_event_add_play_link(event_code=None):
    event = None
    try:
        event = Event.objects.get(code=event_code)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        raise ValueError("Unable to retrieve a link for this event.")

    if not event:
        raise ValueError("Unable to retrieve a link for this event.")

    return urljoin(
        settings.FRONTEND_DOMAIN, "/".join(["event", event.code, "play", "add"])
    )


class Command(BaseCommand):
    help = "Runs a Discord bot for the Tournament app"

    def handle(self, *args, **options):

        if not settings.DISCORD_TOKEN:

            # Fail silently
            print("No Discord token, sleeping indefinitely")

            while 1:
                time.sleep(10)

        bot = commands.Bot(command_prefix="!")

        @bot.event
        async def on_ready():
            print(f"{bot.user.name} has connected to Discord!")

        @bot.command(name="leaderboard", help="Show a tournament leaderboard")
        async def leaderboard(ctx, event_code: Optional[str] = None):

            # Get the leaderboard
            leaderboard = None
            try:
                leaderboard = await get_event_leaderboard(
                    event_code=event_code.upper()
                    if event_code
                    else ctx.channel.name.upper()
                )
            except ValueError as error:
                await ctx.send(str(error))
                return

            if not leaderboard:
                await ctx.send("Unable to find a leaderboard for this event.")
                return

            leaderboard_formatted = "\n".join(
                [
                    f"{i + 1}. {player['name']} ({round(player['score'])})"
                    for i, player in enumerate(leaderboard["leaderboard"])
                ]
            )

            leaderboard_url = urljoin(
                settings.FRONTEND_DOMAIN, "/".join(["event", leaderboard["event_code"]])
            )

            await ctx.send(
                f"""**{leaderboard["event_name"]} Leaderboard**

{leaderboard_formatted}

More details at {leaderboard_url}
"""
            )

        @bot.command(name="addplay", help="Get a tournament event add play link")
        async def add_play(ctx, event_code: Optional[str] = None):
            link = None

            try:
                link = await get_event_add_play_link(
                    event_code.upper() if event_code else ctx.channel.name.upper()
                )
            except ValueError as error:
                await ctx.send(str(error))
                return

            if not link:
                await ctx.send("Unable to retrieve a link for this event.")
                return

            await ctx.send(link)

        bot.run(settings.DISCORD_TOKEN)
