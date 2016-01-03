import json
from django.http import HttpResponseNotAllowed

from .models import Joke


def load(request):
    if request.METHOD != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if request.meta['CONTENT_TYPE'] == 'application/json':
        # load JSON
        data = json.loads(request.body)
    else:
        data = request.POST

    joke = Joke.objects.import_from_url(data['url'])
    