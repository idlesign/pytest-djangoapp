from django.conf.urls import url
from django.http import HttpResponse

from pytest_djangoapp.compat import get_urlpatterns


def raise_exception(request):
    raise Exception('This one should be handled by 500 technical view')


def index(request, some_id):

    if request.method == 'POST':
        return HttpResponse('json')

    if request.is_ajax():
        return HttpResponse('ajaxed')

    from django.templatetags.static import static
    return HttpResponse('%s | fine %s' % (some_id, static('blank.png')))


urlpatterns = get_urlpatterns([
    url(r'^index/(?P<some_id>\d+)/$', index, name='index'),
    url(r'^raiser/$', raise_exception, name='raiser'),
])
