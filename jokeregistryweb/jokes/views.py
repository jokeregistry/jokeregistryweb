import json

from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.template.response import TemplateResponse

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


def index(request):
    return TemplateResponse(request, 'index.html')
