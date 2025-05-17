from typing import List

import pytest
from decimal import Decimal
from django.db import connections, DEFAULT_DB_ALIAS, reset_queries

if False:  # pragma: nocover
    from collections import deque  # noqa


@pytest.fixture
def db_queries(settings) -> 'Queries':
    """Allows access to executed DB queries.

    ```py
    def test_db(db_queries):

        # Previous queries cleared at the beginning.
        assert len(db_queries) == 0

        ...  # Do some DB-related stuff.

        # Assert total queries on all DBs.
        assert len(db_queries) == 10

        # Default DBs SQLs with auxiliary commands filtered out by default.
        sqls = db_queries.sql()

        # Assert total execution time is less than a second.
        assert db_queries.time() < 1

        # Drop SQL gathered so far on default DB.
        db_queries.clear()
    ```

    .. warning:: Requires Django 1.9+ to work.

    """
    queries = Queries()

    debug_values_prev = {}

    for connection in connections.all():
        debug_values_prev[connection.alias] = connection.force_debug_cursor
        connection.force_debug_cursor = True

    try:
        queries.clear_all()

        yield queries

    finally:

        for connection in connections.all():
            prev_debug_value = debug_values_prev.get(connection.alias, None)

            if prev_debug_value is not None:
                connection.force_debug_cursor = prev_debug_value

        queries.clear_all()


class Queries:
    """Allows access to executed DB queries."""

    sql_drop = {
        'BEGIN',
        'COMMIT',
        'END',
    }

    def __len__(self) -> int:
        return len(self.get_log())

    def get_log(self, db_alias: str = None) -> 'deque':
        """
        :param db_alias:

        """
        return connections[db_alias or DEFAULT_DB_ALIAS].queries_log

    def clear_all(self):
        """Clears all queries logged for all DBs."""
        reset_queries()

    def clear(self, db_alias: str = None):
        """Clear queries for the given or default DB.

        :param db_alias: Database alias. Default is used if not given.

        """
        self.get_log(db_alias=db_alias).clear()

    def sql(self, db_alias: str = None, *, drop_auxiliary: bool = True) -> List[str]:
        """Returns a list of queries executed using the given or default DB.

        :param db_alias: Database alias. Default is used if not given.

        :param drop_auxiliary: Filter out auxiliary SQL like:
            * BEGIN
            * COMMIT
            * END

        """
        sqls = []

        auxiliary = self.sql_drop

        for log_entry in self.get_log(db_alias=db_alias):
            sql = ' '.join(sql_line.strip() for sql_line in log_entry['sql'].splitlines())
            if not drop_auxiliary or sql not in auxiliary:
                sqls.append(sql)

        return sqls

    def time(self, db_alias: str = None) -> Decimal:
        """Returns total time executing queries (in seconds) using the given or default DB.

        :param db_alias: Database alias. Default is used if not given.

        """
        times = [Decimal(log_entry['time']) for log_entry in self.get_log(db_alias=db_alias)]
        return sum(times)
