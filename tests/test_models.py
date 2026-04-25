import pytest
from django import VERSION

from tests.testapp.models import Article


def test_models_basic():
    article = Article(title='my title')
    article.save()


@pytest.mark.skipif(VERSION < (1, 9), reason='Django 1.9+ required')
def test_db_queries(db_queries):

    assert len(db_queries) == 0

    article = Article(title='my title')
    article.save()

    assert len(db_queries) == 1 if VERSION >= (2, 2) else 2

    assert len(db_queries.sql()) == 1  # auxiliary sql filtered
    assert db_queries.time() < 1

    db_queries.clear()


@pytest.mark.skipif(VERSION < (1, 9), reason='Django 1.9+ required')
def test_db_queries_scoped(db_queries):

    list(Article.objects.all())
    assert len(db_queries) == 1, db_queries.sql()

    with db_queries.scope() as subqueries1:
        list(Article.objects.filter(title='one'))

        with pytest.raises(AssertionError), db_queries.scope(expect=22):
            # fails expectation: 22!=1
            list(Article.objects.filter(title='fail'))

        with db_queries.scope() as subqueries2:
            list(Article.objects.filter(title='two'))
            # only this scope
            assert len(subqueries1) == 1, subqueries2.get_log()

        # this scope and inner
        assert len(subqueries1) == 3, subqueries1.get_log()

    # both inner and outer
    assert len(db_queries) == 4, db_queries.get_log()
