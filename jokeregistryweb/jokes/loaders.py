from datetime import datetime
import pytz

from django.conf import settings

import inspect
import re
import requests

from jokeregistryweb.accounts.models import User


class LoaderRegistry:

    def __init__(self):
        self.patterns = {}

        functions = inspect.getmembers(self, predicate=inspect.ismethod)

        for function in functions:
            sig = inspect.signature(function[1])

            if 'url' in sig.parameters:
                if sig.parameters['url'].annotation == inspect.Signature.empty:
                    continue

                pattern = re.compile(str(sig.parameters['url'].annotation))
                self.patterns[pattern] = function[1]

    def load(self, url):
        for pattern in self.patterns:
            if pattern.match(url):
                return self.patterns[pattern](url)

    def tweet(self, url: 'https://twitter.com/[A-Za-z0-9_]+/status/\d+'):
        '''Imports a joke from a tweet, creating a user if necessary'''

        status_id = url.split('/')[-1]

        headers = {
            'User-Agent': 'Joke Registry Beta',
            'Authorization': 'Bearer {}'.format(settings.TWITTER_BEARER_TOKEN)
        }
        response = requests.get(
            'https://api.twitter.com/1.1/statuses/show.json',
            params={'id': status_id},
            headers=headers)

        data = response.json()

        tweet_url = 'https://twitter.com/{}/status/{}'.format(
            data['user']['screen_name'],
            data['id_str']
        )
        created_at = datetime.strptime(
            data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        created_at = created_at.replace(tzinfo=pytz.UTC)

        # Check to see if this user exists, and create it if it doesn't
        try:
            author = User.objects.get(twitter_id=data['user']['id'])
        except:
            author = User.objects.create(
                username='@' + data['user']['screen_name'],
                twitter_id=data['user']['id']
            )

        # TODO: Check to see if a username has changed?

        # TODO: Automatic check for prior art?
        return {
            'text': data['text'],
            'link': tweet_url,
            'created': created_at,
            'author': author
        }
