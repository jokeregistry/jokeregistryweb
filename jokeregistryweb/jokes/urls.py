from django.conf.urls import url

from .views import joke_list_view, joke_detail_view, new, load

urlpatterns = [
    url(r'^$', joke_list_view),
    url(r'^(?P<pk>\d+)$', joke_detail_view),
    url(r'^new$', new),
    url(r'^load$', load),
]
