from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Claim
from jokeregistryweb.jokes.models import Joke

class ClaimListView(ListView):
    model = Claim
claim_list_view = ClaimListView.as_view()


class ClaimDetailView(DetailView):
    model = Claim
claim_detail_view = ClaimDetailView.as_view()


def approve(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)


def reject(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)


@require_http_methods(["GET", "POST"])
def new(request):
    if request.META['REQUEST_METHOD'] == 'GET':
        return TemplateResponse(request, 'new_claim.html', {})

    if request.META['CONTENT_TYPE'] == 'application/json':
        # load JSON
        data = json.loads(request.body)
    else:
        data = request.POST

    infringed_joke = Joke.objects.import_from_url(data['infringed_url'])
    infringing_joke = Joke.objects.import_from_url(data['infringing_url'])

    if not (infringed_joke and infringing_joke):
        return TemplateResponse(request, 'new_claim.html', {'errors': ['Problem getting jokes.']})

    claim = Claim(infringed_joke=infringed_joke, infringing_joke=infringing_joke)
    claim.save()

    if claim:
        return redirect('/')
