import pytest

from pytest_djangoapp.tests.testapp.models import Article
from django import VERSION


def test_models_basic():
    article = Article(title='my title')
    article.save()


@pytest.mark.skipif(VERSION < (1, 9), reason='Django 1.9+ required')
def test_db_queries(db_queries):

    assert len(db_queries) == 0

    article = Article(title='my title')
    article.save()

    print(db_queries.get_log())

    assert len(db_queries) == 1 if VERSION >= (2, 2) else 2

    assert len(db_queries.sql()) == 1  # auxiliary sql filtered
    assert db_queries.time() < 1

    db_queries.clear()
