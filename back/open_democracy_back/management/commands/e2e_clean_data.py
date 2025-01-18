from django.core.management import BaseCommand

from open_democracy_back.e2e_urls import clean_data


class Command(BaseCommand):
    help = "Command to delete all participations to get a clean database"

    def handle(self, *args, **options):
        clean_data()
        return
