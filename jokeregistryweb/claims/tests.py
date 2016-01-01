from django.test import TestCase, override_settings

from jokeregistryweb.jokes.models import Joke
from .models import Claim
import responses


class ClaimsTestCase(TestCase):

    @responses.activate
    @override_settings(TWITTER_BEARER_TOKEN='no-op')
    def test_prior_art(self):

        initial_response = {
            'created_at': 'Thu Oct 08 01:28:34 +0000 2015',
            'text': 'Linkedin Park',
            'id': 651932161755475968,
            'id_str': '651932161755475968',
            'user': {
                'screen_name': 'cregslist',
                'id': 304721573,
                'id_str': '304721573'
            }
        }
        responses.add(
            responses.GET,
            'https://api.twitter.com/1.1/statuses/show.json?id=651932161755475968',
            json=initial_response,
            status=200,
            match_querystring=True)

        prior_art_response = {
            'created_at': 'Tue Oct 06 18:11:15 +0000 2015',
            'text': 'LinkedIn Park, the most annoying cover band ever',
            'id': 651459722063822848,
            'id_str': '651459722063822848',
            'user': {
                'screen_name': 'iamsomejerk',
                'id': 17317042,
                'id_str': '17317042'
            }
        }
        responses.add(
            responses.GET,
            'https://api.twitter.com/1.1/statuses/show.json?id=651459722063822848',
            json=prior_art_response,
            status=200,
            match_querystring=True)

        bad_joke = Joke.objects.import_from_tweet('651932161755475968')

        claim = Claim.objects.create(
            joke=bad_joke,
            link='https://twitter.com/iamsomejerk/status/651459722063822848',
        )
        claim.approve()

        # Refresh the infringing joke
        bad_joke.refresh_from_db()
        self.assertTrue(bad_joke.parent is not None)
        self.assertEquals(bad_joke.parent.author.username, '@iamsomejerk')
        self.assertEquals(bad_joke.parent.text, 'LinkedIn Park, the most annoying cover band ever')
