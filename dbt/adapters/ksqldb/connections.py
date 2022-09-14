from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Any, Dict, Tuple, List

import dbt.exceptions # noqa
from dbt.adapters.base import Credentials
from dbt.adapters.base import BaseConnectionManager as connection_cls
from dbt.clients import agate_helper
from dbt.contracts.connection import AdapterResponse
from dbt.events import AdapterLogger

from ksql import KSQLAPI

logger = AdapterLogger("ksqlDB")


@dataclass
class ksqlDBCredentials(Credentials):
    """
    Defines database specific credentials that get added to
    profiles.yml to connect to new adapter
    """

    # Add credentials members here, like:
    server: str
    api_key: str
    api_secret: str
    port: Optional[int] = 8088

    _ALIASES = {
        "key":"api_key",
        "secret":"api_secret"
    }

    @property
    def type(self):
        """Return name of adapter."""
        return "ksqldb"

    @property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return self.server

    def _connection_keys(self):
        """
        List of keys to display in the `dbt debug` output.
        """
        return ("server","port","api_key","api_secret", "database", "schema")


class ksqlDBConnectionManager(connection_cls):
    TYPE = "ksqldb"


    @contextmanager
    def exception_handler(self, sql: str):
        """
        Returns a context manager, that will handle exceptions raised
        from queries, catch, log, and raise dbt exceptions it knows how to handle.
        """
        # ## Example ##
        # try:
        #     yield
        # except myadapter_library.DatabaseError as exc:
        #     self.release(connection_name)

        #     logger.debug("myadapter error: {}".format(str(e)))
        #     raise dbt.exceptions.DatabaseException(str(exc))
        # except Exception as exc:
        #     logger.debug("Error running SQL: {}".format(sql))
        #     logger.debug("Rolling back transaction.")
        #     self.release(connection_name)
        #     raise dbt.exceptions.RuntimeException(str(exc))
        try:
            yield
        except Exception as e:
            raise

    @classmethod
    def get_ksql_client(cls, profile_credentials):
        ksql_server = f"{profile_credentials.server}:{profile_credentials.port}"
        api_key = profile_credentials.api_key
        api_secret = profile_credentials.api_secret
        client = KSQLAPI(ksql_server, api_key=api_key, secret=api_secret)
        return client

    @classmethod
    def open(cls, connection):
        """
        Receives a connection object and a Credentials object
        and moves it to the "open" state.
        """
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection

        credentials = connection.credentials

        try:
            handle = cls.get_ksql_client(connection.credentials)
            connection.state = "open"
            connection.handle = handle
        except Exception as e:
            logger.debug(
                "Got an error when attempting to create a bigquery " "client: '{}'".format(e)
            )
            connection.handle = None
            connection.state = "fail"
            raise Exception(str(e))

        return connection

    @classmethod
    def get_response(cls,cursor):
        """
        Gets a cursor object and returns adapter-specific information
        about the last executed command generally a AdapterResponse ojbect
        that has items such as code, rows_affected,etc. can also just be a string ex. "OK"
        if your cursor does not offer rich metadata.
        """
        # ## Example ##
        # return cursor.status_message
        pass

    def cancel(self, connection):
        """
        Gets a connection object and attempts to cancel any ongoing queries.
        """
        # ## Example ##
        # tid = connection.handle.transaction_id()
        # sql = "select cancel_transaction({})".format(tid)
        # logger.debug("Cancelling query "{}" ({})".format(connection_name, pid))
        # _, cursor = self.add_query(sql, "master")
        # res = cursor.fetchone()
        # logger.debug("Canceled query "{}": {}".format(connection_name, res))
        pass

    def begin(self):
        pass

    def cancel_open(self):
        pass

    def commit(self):
        pass

    def execute(self, sql, auto_begin=False, fetch=None) -> Tuple[str, str]:
        conn = self.get_thread_connection()
        client = conn.handle
        stream_properties = {"ksql.streams.auto.offset.reset": "latest"}
        res = client.ksql(sql, stream_properties)

        response = AdapterResponse(  # type: ignore[call-arg]
            _message=res,
            rows_affected=0,
            code="ksql",
        )
        table = agate_helper.empty_table()
        return res, table
