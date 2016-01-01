from django.conf import settings
from django.db import models

from jokeregistryweb.accounts.models import User

import datetime
import pytz
import requests


class JokeManager(models.Manager):

    def import_from_tweet(self, status_id):
        '''Imports a joke from a tweet, creating a user if necessary'''

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
        created_at = datetime.datetime.strptime(
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
        joke = Joke.objects.create(
            text=data['text'],
            link=tweet_url,
            created=created_at,
            author=author
        )

        return joke


class Joke(models.Model):

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField()
    link = models.URLField(null=True, blank=True)

    # On an "original" joke, this will be null
    # N.B. Chris tried naming this field "original" and tests broke
    #       but naming it "parent" made it work
    # TODO(anyone): ^WHY????
    parent = models.ForeignKey('jokes.Joke', null=True, blank=True, on_delete=models.CASCADE)

    objects = JokeManager()
