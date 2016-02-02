from django.test import TestCase, override_settings, RequestFactory

from jokeregistryweb.jokes.models import Joke
from jokeregistryweb.jokes.views import load
from jokeregistryweb.accounts.models import User

from datetime import datetime
import pytz
import responses
from unittest.mock import MagicMock


class JokeTestCase(TestCase):

    @override_settings(TWITTER_BEARER_TOKEN='no-op')
    def test_twitter_url_submit(self):
        factory = RequestFactory()
        request = factory.get('/jokes/load')
        response = load(request)
        self.assertEquals(response.status_code, 405)

        request = factory.post(
            '/jokes/load',
            {'url': 'https://twitter.com/cregslist/status/651932161755475968'})
        user = User.objects.create_user(
            username='sean',
            email='sean@jokeregistry.online',
            password='hunter2')
        request.user = user
        Joke.objects.import_from_url = MagicMock(return_value=True)
        response = load(request)
        self.assertTrue(response.status_code < 500)

    @responses.activate
    @override_settings(TWITTER_BEARER_TOKEN='no-op')
    def test_twitter_import(self):

        self.assertEquals(User.objects.count(), 0)

        sample_response = {
            'created_at': 'Thu Oct 08 01:28:34 +0000 2015',
            'text': 'Linkedin Park',
            'id': 651932161755475968,
            'id_str': '651932161755475968',
            'user': {
                'screen_name': 'cregslist',
                'id': 304721573,
            }
        }

        responses.add(
            responses.GET,
            'https://api.twitter.com/1.1/statuses/show.json',
            json=sample_response,
            status=200)

        joke = Joke.objects.import_from_url('https://twitter.com/cregslist/status/651932161755475968')
        self.assertEquals(joke.text, 'Linkedin Park')
        self.assertEquals(joke.created, datetime(
            year=2015,
            month=10,
            day=8,
            hour=1,
            minute=28,
            second=34,
            tzinfo=pytz.utc
        ))
        self.assertEquals(joke.author.username, '@cregslist')

        self.assertEquals(len(responses.calls), 1)
        self.assertEquals(User.objects.count(), 1)

    @responses.activate
    @override_settings(TWITTER_BEARER_TOKEN='no-op')
    def test_duplicate_import_guard(self):
        self.assertEquals(User.objects.count(), 0)

        sample_response = {
            'created_at': 'Thu Oct 08 01:28:34 +0000 2015',
            'text': 'Linkedin Park',
            'id': 651932161755475968,
            'id_str': '651932161755475968',
            'user': {
                'screen_name': 'cregslist',
                'id': 304721573,
            }
        }

        responses.add(
            responses.GET,
            'https://api.twitter.com/1.1/statuses/show.json',
            json=sample_response,
            status=200)
        joke1 = Joke.objects.import_from_url('https://twitter.com/cregslist/status/651932161755475968')
        joke2 = Joke.objects.import_from_url('https://twitter.com/cregslist/status/651932161755475968')
        self.assertEquals(joke1.id, joke2.id)
