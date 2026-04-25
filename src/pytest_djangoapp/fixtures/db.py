from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Generator

import pytest
from django.db import DEFAULT_DB_ALIAS, connections, reset_queries

if TYPE_CHECKING:
    from collections import deque


@pytest.fixture
def db_queries(settings) -> Generator[Queries, None, None]:
    """Allows access to executed DB queries.

    ```py
    def test_db(db_queries):

        # Previous queries cleared at the beginning.
        assert len(db_queries) == 0

        ...  # Do some DB-related stuff.

        with db_queries.scope() as qrs:
            ...  # Do other DB-related stuff.
            assert len(qrs) == 2

        # or
        with db_queries.scope(expect=2):
            ...  # Do other DB-related stuff.

        # Assert total queries on default DB.
        assert len(db_queries) == 10

        # The default DB SQLs with auxiliary commands filtered out by default.
        sqls = db_queries.sql()

        # Assert total execution time is less than a second.
        assert db_queries.time() < 1

        # Drop SQL gathered so far on the default DB.
        db_queries.clear()
    ```

    .. warning:: Requires Django 1.9+ to work.

    """
    q = Queries()

    debug_values_prev = {}

    for connection in connections.all():
        debug_values_prev[connection.alias] = connection.force_debug_cursor
        connection.force_debug_cursor = True

    try:
        reset_queries()

        with q.scope() as queries:
            yield queries

    finally:

        for connection in connections.all():
            prev_debug_value = debug_values_prev.get(connection.alias, None)

            if prev_debug_value is not None:
                connection.force_debug_cursor = prev_debug_value

        reset_queries()


class Queries:
    """Allows access to executed DB queries."""

    sql_drop: ClassVar = {
        'BEGIN',
        'COMMIT',
        'END',
    }

    def __len__(self) -> int:
        return len(self.get_log())

    @contextmanager
    def scope(self, db_alias: str = '', *, expect: int | None = None) -> Generator[Queries, None, None]:
        """Context manager for scoped sql checks.
        Exposes the object with the same methods as given by `db_queries` (`Queries`).

        :param db_alias:
        :param expect: Number of SQL queries expected.
        """
        log = self.get_log(db_alias=db_alias)
        log_backup = deepcopy(log)
        self.clear(db_alias=db_alias)

        subqueries = self.__class__()
        try:
            yield subqueries

            if expect is not None:
                log = subqueries.get_log(db_alias=db_alias)
                assert expect == len(log), log

        finally:
            log_backup_sub = deepcopy(subqueries.get_log(db_alias=db_alias))
            subqueries.clear(db_alias=db_alias)
            log.extend(log_backup + log_backup_sub)

    def get_log(self, db_alias: str = '') -> deque:
        """
        :param db_alias:

        """
        return connections[db_alias or DEFAULT_DB_ALIAS].queries_log

    def clear_all(self):
        """Clears all queries logged for all DBs."""
        reset_queries()

    def clear(self, db_alias: str = ''):
        """Clear queries for the given or the default DB.

        :param db_alias: Database alias. Default is used if not given.

        """
        self.get_log(db_alias=db_alias).clear()

    def sql(self, db_alias: str = '', *, drop_auxiliary: bool = True) -> list[str]:
        """Returns a list of queries executed using the given or the default DB.

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

    def time(self, db_alias: str = '') -> Decimal:
        """Returns total time executing queries (in seconds) using the given or the default DB.

        :param db_alias: Database alias. Default is used if not given.

        """
        return sum(Decimal(log_entry['time']) for log_entry in self.get_log(db_alias=db_alias))
