from operator import itemgetter
from typing import Optional, List
from urllib.parse import urljoin
from more_itertools import divide
import random
import time

from asgiref.sync import sync_to_async

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings

from tournament.apps.event.models import Event

from discord.ext import commands


def join_team_members(team_members):
    return "\n".join([f"- {team_member}" for team_member in team_members])


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

        bot = commands.Bot(
            command_prefix="!", description="Board game tournament helper bot"
        )

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

        @bot.command(
            name="turnorder",
            help="Determine order of playing for a set of player initials. Provide a list of initials separated by spaces",
        )
        async def turn_order(ctx, *args):

            player_initials = [initial for initial in args]

            if not player_initials:
                await ctx.send(
                    "You must provide player initials to determine a turn order"
                )
                return

            new_player_order = random.sample(player_initials, len(player_initials))
            new_player_order_formatted = "\n".join(
                [
                    f"{i + 1}. {player_initial}"
                    for i, player_initial in enumerate(new_player_order)
                ]
            )

            await ctx.send(f"**Turn Order**\n\n{new_player_order_formatted}")

        @bot.command(
            name="teams",
            help="Split a set of given player initials into a given number of teams",
        )
        async def teams(ctx, number_of_teams: int = None, *args):

            if not number_of_teams:
                await ctx.send(
                    "You must provide the number of teams to place players in"
                )
                return

            player_initials = [initial for initial in args]

            if not player_initials:
                await ctx.send("You must provide player initials to determine a teams")
                return

            new_player_order = random.sample(player_initials, len(player_initials))
            teams = divide(number_of_teams, new_player_order)

            teams_formatted = "\n\n".join(
                [
                    f"Team {i + 1}\n{join_team_members(team)}"
                    for i, team in enumerate(teams)
                ]
            )

            await ctx.send(f"**Teams**\n\n{teams_formatted}")

        bot.run(settings.DISCORD_TOKEN)
