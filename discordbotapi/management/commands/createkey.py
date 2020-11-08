from django.core.management.base import BaseCommand
from discordbotapi.models import APIKey


class Command(BaseCommand):
    help = 'Creates an API Key'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Successfully created Key: {APIKey.generate_key()}'))