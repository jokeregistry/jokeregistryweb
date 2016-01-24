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

    infringing_joke = models.ForeignKey(
        'jokes.Joke',
        related_name='infringing_claim',
        help_text='The infringing joke')
    infringed_joke = models.ForeignKey(
        'jokes.Joke',
        related_name='infringed_claim',
        help_text='The original joke')
    text = models.TextField(help_text='additional detail', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=FILED)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', '-updated')

    def approve(self):
        if self.infringed_joke.created < self.infringing_joke.created:
            self.infringing_joke.parent = self.infringed_joke
            self.infringing_joke.save()

        self.status = Claim.APPROVED
        self.save()

    def reject(self):
        self.status = Claim.REJECTED
        self.save()
