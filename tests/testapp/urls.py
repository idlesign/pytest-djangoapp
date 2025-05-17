try:
    from django.urls import re_path
    
except ImportError:
    from django.conf.urls import url as re_path

    
from django.http import HttpResponse

from pytest_djangoapp.compat import get_urlpatterns


def raise_exception(request):
    raise Exception('This one should be handled by 500 technical view')


def index(request, some_id):

    if request.method == 'POST':
        return HttpResponse('json')

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # .headers in Django 2.2+
        return HttpResponse('ajaxed')

    from django.templatetags.static import static
    return HttpResponse(f"{some_id} | fine {static('blank.png')}")


urlpatterns = get_urlpatterns([
    re_path(r'^index/(?P<some_id>\d+)/$', index, name='index'),
    re_path(r'^raiser/$', raise_exception, name='raiser'),
])
