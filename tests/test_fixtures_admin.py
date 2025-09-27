import pytest

from tests.testapp.models import Article


@pytest.fixture
def client_env(admin_client):
    admin_client.configure(app='testapp', model='article')

    article_1 = Article(title='article_1')
    article_1.save()

    article_2 = Article(title='article_2')
    article_2.save()

    article_3 = Article(title='article_3')
    article_3.save()

    return admin_client, [article_1, article_2, article_3]


class TestaAdminClient:

    def test_configure_model(self, admin_client):
        # by name
        admin_client.configure(app='testapp', model='article')
        # by model type
        admin_client.configure(app='testapp', model=Article)
        # by model instance
        admin_client.configure(app='testapp', model=Article())

    def test_listing(self, client_env):
        client, __ = client_env
        response = client.call_listing()
        assert response.ok
        assert 'article_1' in response.text

    def test_listing_action(self, client_env):
        client, articles = client_env
        response = client.call_listing_action(action='rename', items=articles[:2])
        assert response.ok
        assert 'renamedfine' in response.text

        for article in articles:
            article.refresh_from_db()

        assert articles[0].title == 'renamedfine'
        assert articles[2].title == 'article_3'

        # set to all
        response = client.call_listing_action(action='rename')
        assert response.ok
        assert 'article_3' not in response.text

        articles[2].refresh_from_db()
        assert articles[2].title == 'renamedfine'

    def test_change(self, client_env):
        client, articles = client_env

        # by id
        response = client.call_change(articles[0].pk)
        assert response.ok
        assert 'value="article_1"' in response.text

        # by model
        response = client.call_change(articles[0])
        assert response.ok
        assert 'value="article_1"' in response.text
