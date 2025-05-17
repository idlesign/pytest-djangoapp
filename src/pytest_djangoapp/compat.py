from django import VERSION


def get_urlpatterns(patterns_list: list) -> list:
    """Returns object suitable to use as urlpatterns in `urls.py`.

    ```py
        urlpatterns = get_urlpatterns([
            url(r'^index/$', index, name='index'),
        ])

    :param patterns_list:

    """
    if VERSION >= (1, 9):
        return patterns_list

    from django.conf.urls import patterns

    return patterns('', *patterns_list)
