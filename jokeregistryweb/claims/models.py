from django.db import models

from jokeregistryweb.jokes.models import Joke


class Claim(models.Model):
    '''A claim of prior art (or infringement)'''

    FILED = 0
    APPROVED = 1
    REJECTED = 2
    STATUS_CHOICES = (
        (FILED, 'Filed'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )

    joke = models.ForeignKey(
        'jokes.Joke',
        help_text='The joke this claim is in regards to')
    link = models.URLField(help_text='a link to the prior art')
    text = models.TextField(help_text='additional detail', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=FILED)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', '-updated')

    def approve(self):
        new_joke = Joke.objects.import_from_url(self.link)

        if new_joke.created < self.joke.created:
            self.joke.parent = new_joke
            self.joke.save()
        else:
            # This new joke is an infringer...
            new_joke.parent = self.joke
            new_joke.save()

        self.status = Claim.APPROVED
        self.save()

    def reject(self):
        self.status = Claim.REJECTED
        self.save()
