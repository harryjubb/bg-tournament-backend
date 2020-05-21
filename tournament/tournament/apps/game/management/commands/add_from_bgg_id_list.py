import time

from django.core.management.base import BaseCommand
from django.conf import settings

from tournament.apps.game.models import Game


class Command(BaseCommand):
    help = "Add a new-line separated list of BGG IDs (from a file, absolute path) to the database"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1, type=str)

    def handle(self, *args, **options):

        if options["filename"]:

            with open(options["filename"][0], "r") as fo:
                for line in fo:
                    bgg_id = int(line.strip())

                    game = None
                    created = None
                    try:
                        game, created = Game.objects.get_or_create(bgg_id=bgg_id)
                    except Exception as error:
                        print(f"Error getting or creating game with bgg_id {bgg_id}")
                        continue

                    if created:
                        print(f"Created {bgg_id} {game}")
                        time.sleep(3)
                    else:
                        print(f"Found existing for {bgg_id} {game}")
                        time.sleep(0.05)
