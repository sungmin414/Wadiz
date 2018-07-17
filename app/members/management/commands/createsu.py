from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
import json
import os
User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        secret = json.load(open(os.path.join(settings.SECRETS_DIR, 'base.json')))

        if not User.objects.filter(username=secret['SUPERUSER_USERNAME']):
            User.objects.create_superuser(
                username=secret['SUPERUSER_USERNAME'],
                password=secret['SUPERUSER_PASSWORD'],
                email=secret['SUPERUSER_EMAIL'],
            )


