from typing import Optional, Any, Dict, Tuple, List

import dbt
from dbt.adapters.base import BaseAdapter as adapter_cls
from dbt.adapters.base import (
    BaseAdapter,
    available,
    RelationType,
    SchemaSearchMap,
    AdapterConfig,
)
from dbt.adapters.ksqldb.relation import ksqlDBRelation
# from dbt.adapters.ksqldb import ksqlDBColumn
# from dbt.adapters.ksqldb import ksqlDBConnectionManager
from dbt.adapters.ksqldb import ksqlDBConnectionManager
from dbt.logger import GLOBAL_LOGGER as logger


class ksqlDBAdapter(adapter_cls):
    """
    Controls actual implmentation of adapter, and ability to override certain methods.
    """
    Relation = ksqlDBRelation

    ConnectionManager = ksqlDBConnectionManager

    @classmethod
    def date_function(cls):
        """
        Returns canonical date func
        """
        return "CAST(FROM_UNIXTIME(UNIX_TIMESTAMP()) AS DATE)"

    @classmethod
    def is_cancelable(cls) -> bool:
         return False

    @available
    def empty(self, database: str) -> str:
        return ""

    @available
    def list_schemas(self, database: str) -> List[str]:
        return ["."]

    def convert_boolean_type(self):
        return "boolean"

    def convert_date_type(self):
        return "date"

    def convert_datetime_type(self):
        raise dbt.exceptions.NotImplementedException(
            "`datetime` is not implemented for this adapter!"
        )

    def convert_number_type(self):
        "double"

    def convert_text_type(self):
        return "string"

    def convert_time_type(self):
        return "time"

    def create_schema(self, relation):
        return
        raise dbt.exceptions.NotImplementedException(
            f"`create_schema({relation})` is not implemented for this adapter!"
        )

    def drop_relation(self, relation):
        is_cached = self._schema_is_cached(relation.database, relation.schema)  # type: ignore[arg-type]
        if is_cached:
            self.cache_dropped(relation)
        conn = self.connections.get_thread_connection()

        # ref = self.get_table_ref_from_relation(relation)
        logger.info(f"Dropping {relation}")
        # Implement here
        try:
            conn.handle.ksql(query)
        except Exception as e:
            logger.warning(e)

    def drop_stream(self, relation, delete_topic=False):
        conn = self.connections.get_thread_connection()

        # ref = self.get_table_ref_from_relation(relation)
        logger.info(f"Dropping {relation}")
        ref = relation
        query = f"DROP STREAM {ref}"
        if delete_topic:
            query += "DELETE TOPIC"
        query += ";"

        try:
            conn.handle.ksql(query)
        except Exception as e:
            logger.warning(e)

    def drop_schema(self):
        raise dbt.exceptions.NotImplementedException(
            "`drop_schema` is not implemented for this adapter!"
        )


    def expand_column_types(self):
        raise dbt.exceptions.NotImplementedException(
            "`expand_column_types` is not implemented for this adapter!"
        )


    def get_columns_in_relation(self):
        raise dbt.exceptions.NotImplementedException(
            "`get_columns_in_relation` is not implemented for this adapter!"
        )

    def list_relations_without_caching(self, schema_relation):
        t = ksqlDBRelation.create(
            database="test", schema="hello", identifier="", quote_policy={}, type=ksqlDBRelation.Table
        )
        return [t,]

    def quote(self):
        return '"'

    def rename_relation(self, from_relation, to_relation):
        raise dbt.exceptions.NotImplementedException(
            "`rename_relation` is not implemented for this adapter!"
        )

    def truncate_relation(self):
        raise dbt.exceptions.NotImplementedException(
            "`truncate` is not implemented for this adapter!"
        )
