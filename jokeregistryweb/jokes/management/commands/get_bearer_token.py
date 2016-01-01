from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import base64
import requests


class Command(BaseCommand):
    help = '''Prints a bearer token for the application

    (https://dev.twitter.com/oauth/application-only)'''

    def handle(self, *args, **options):
        try:
            key = settings.TWITTER_CONSUMER_KEY
            secret = settings.TWITTER_CONSUMER_SECRET
        except AttributeError:
            raise CommandError('You must have a TWITTER_CONSUMER_KEY and TWITTER_CONSUMER_SECRET')

        credentials = '{key}:{secret}'.format(key=key, secret=secret)
        credentials = base64.b64encode(credentials.encode())

        headers = {
            'User-Agent': 'Joke Registry Beta',
            'Authorization': 'Basic {}'.format(credentials.decode('utf-8')),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        print(headers)

        response = requests.post(
            'https://api.twitter.com/oauth2/token',
            data='grant_type=client_credentials',
            headers=headers)

        print(response.content)
        response.raise_for_status()
        print(response.json()['access_token'])

        # AAAAAAAAAAAAAAAAAAAAANEujgAAAAAA%2BHGdTHKkkwDmoQYe89RVYNGaLM4%3D4breVz7YjNWBcOaTyD6Px15LMB1Xphirp4EvtAJPpcSg124byi
