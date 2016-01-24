import json

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Joke


class JokeListView(ListView):

    model = Joke
joke_list_view = JokeListView.as_view()


class JokeDetailView(DetailView):

    model = Joke
joke_detail_view = JokeDetailView.as_view()


def new(request):
    return TemplateResponse(request, 'new_joke.html')


@require_http_methods(['POST'])
def load(request):

    if request.META['CONTENT_TYPE'] == 'application/json':
        # load JSON
        data = json.loads(request.body)
    else:
        data = request.POST

    joke = Joke.objects.import_from_url(data['url'])

    if joke:
        return redirect('/')
