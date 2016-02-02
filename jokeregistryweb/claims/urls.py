from django.conf.urls import url

from .views import claim_list_view, claim_detail_view, new

urlpatterns = [
    url(r'^$', claim_list_view),
    url(r'^(?P<pk>\d+)$', claim_detail_view),
    url(r'^new$', new),
]
