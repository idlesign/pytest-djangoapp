from django.conf.urls import url
from django.http import HttpResponse


from pytest_djangoapp.compat import get_urlpatterns


def index(request):

    if request.is_ajax():
        return HttpResponse('ajaxed')

    from django.contrib.staticfiles.templatetags.staticfiles import static
    return HttpResponse('fine %s' % static('blank.png'))


urlpatterns = get_urlpatterns([
    url(r'^index/$', index, name='index'),
])
