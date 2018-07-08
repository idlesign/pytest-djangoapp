from django import VERSION

from django.conf.urls import url
from django.http import HttpResponse


def index(request):

    if request.is_ajax():
        return HttpResponse('ajaxed')

    from django.contrib.staticfiles.templatetags.staticfiles import static
    return HttpResponse('fine %s' % static('blank.png'))


def get_urls():

    urls = [
        url(r'^index/$', index, name='index'),
    ]

    if VERSION >= (1, 9):
        return urls

    from django.conf.urls import patterns
    return patterns('', *urls)


urlpatterns = get_urls()


if VERSION < (1, 10):
    from django.conf.urls import patterns
    urlpatterns.insert(0, '')
    urlpatterns = patterns(*urlpatterns)
