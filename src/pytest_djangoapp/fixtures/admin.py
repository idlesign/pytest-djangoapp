from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable

import pytest
from django.db.models import Model
from django.urls import reverse

from .request import DjagoappClient

if TYPE_CHECKING:
    from .users import TypeUser


class AdminClient:

    @classmethod
    def _enhance_result(cls, result):
        result.ok = result.status_code == 200
        if not hasattr(result, 'text'):
            result.text = result.content.decode()

    def __init__(self, *, user_func: callable, app_name: str):
        self.client = None
        self._app_name = app_name
        self._user_func = user_func
        self._url_listing = None
        self._url_add = None
        self._url_change = None

    def configure(self, *, model: str | Model | type[Model], app: str = '', user: TypeUser = None):
        """Configure the client.

        :param model: Model name, class or instance.
        :param app: Application name.
        :param user: User object.
        """
        model_name = model if isinstance(model, str) else model._meta.model_name

        self.client = DjagoappClient(
            user=user or self._user_func(superuser=True),
        )
        app = app or self._app_name
        self._url_listing = reverse(f'admin:{app}_{model_name}_changelist')
        self._url_add = reverse(f'admin:{app}_{model_name}_add')
        self._url_change = f'admin:{app}_{model_name}_change'

    def call_listing(self, *, follow: bool = True, **kwargs):
        """Calls items listing page and returns the response.

        :param follow: Follow redirects.
        :param kwargs: Additional arguments passed client requesting method.
        """
        result = self.client.get(self._url_listing, follow=follow, **kwargs)
        self._enhance_result(result)
        return result

    def call_listing_action(
            self,
            action: str,
            *,
            items: Iterable[str | Model] | None = None,
            follow: bool = True,
            **kwargs
    ):
        """Calls items listing page and returns the response.

        :param action: Action name.
        :param items: Items to apply action to (ids or models). Or None to apply to all items.
        :param follow: Follow redirects.
        :param kwargs: Additional arguments passed client requesting method.
        """
        select_across = 0
        items_ = []

        if items is None:
            select_across = 1
            items_ = ['dummy']

        else:
            for item in items:
                if isinstance(item, Model):
                    item = f'{item.pk}'
                items_.append(item)

        result = self.client.post(
            self._url_listing,
            {
                "action": action,
                "_selected_action": items_,
                "select_across": select_across,
                "index": 0,
            },
            follow=follow,
            **kwargs
        )
        self._enhance_result(result)
        return result

    def call_change(self, obj: Any, *, follow: bool = True, **kwargs):
        """Calls item details/edit/change page and returns the response.

        :param obj: Model instance or id.
        :param follow: Follow redirects.
        :param kwargs: Additional arguments passed client requesting method.
        """
        obj_id = obj.pk if isinstance(obj, Model) else obj
        result = self.client.get(reverse(self._url_change, kwargs={'object_id': obj_id}), follow=follow, **kwargs)
        self._enhance_result(result)
        return result


@pytest.fixture
def admin_client(user_create, conf_app_name) -> AdminClient:
    """Facilitates Admin interface testing.

    ```py
    def test_admin(admin_client):
        admin_client.configure(app='myapp', model=my_model_obj)

        response = admin_client.call_listing()
        response = admin_client.call_change(my_model_obj.pk)
        response = client.call_listing_action(action='rename', items=[my_model_obj])

        assert response.ok
        assert 'some' in response.text
    ```

    :returns: Admin client object.

    """
    return AdminClient(user_func=user_create, app_name=conf_app_name)
