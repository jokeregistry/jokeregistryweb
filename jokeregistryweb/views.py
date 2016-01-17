from django.template.response import TemplateResponse

from .jokes.models import Joke

def index(request):
    context = {}
    jokes = Joke.objects.all()
    context['jokes'] = jokes
    return TemplateResponse(request, 'index.html', context)