from dbt.adapters.ksqldb.connections import ksqlDBConnectionManager # noqa
from dbt.adapters.ksqldb.connections import ksqlDBCredentials
from dbt.adapters.ksqldb.impl import ksqlDBAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import ksqldb


Plugin = AdapterPlugin(
    adapter=ksqlDBAdapter,
    credentials=ksqlDBCredentials,
    include_path=ksqldb.PACKAGE_PATH
    )
