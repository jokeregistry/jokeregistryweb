from django.shortcuts import get_object_or_404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Claim


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
