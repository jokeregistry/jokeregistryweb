from django.template.response import TemplateResponse

from .claims.models import Claim
from .jokes.models import Joke

def index(request):
    context = {}
    claims = Claim.objects.all()
    context['claims'] = claims
    jokes = Joke.objects.all()
    context['jokes'] = jokes
    return TemplateResponse(request, 'index.html', context)