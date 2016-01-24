from django.conf import settings
from django.db import models


class JokeManager(models.Manager):
    from .loaders import LoaderRegistry
    registry = LoaderRegistry()

    def import_from_url(self, url):
        # Check if joke already loaded
        jokes = Joke.objects.filter(link=url)
        if jokes.count() > 0:
            return jokes[0]

        kwargs = self.registry.load(url)
        if kwargs:
            return self.create(**kwargs)

    def approved(self):
        return self.filter(approved=True)


class Joke(models.Model):

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField()
    link = models.URLField(null=True, blank=True)
    approved = models.BooleanField(default=True)

    # On an "original" joke, this will be null
    # N.B. Chris tried naming this field "original" and tests broke
    #       but naming it "parent" made it work
    # TODO(anyone): ^WHY????
    parent = models.ForeignKey('jokes.Joke', null=True, blank=True, on_delete=models.CASCADE)

    objects = JokeManager()
