{%- materialization ephemeral, adapter='ksqldb' -%}
    {{ exceptions.raise_compiler_error(
        """
        dbt-ksql does not support ephemerals (sub-query)
        Perhaps you want to use stream or table?
        """
    )}}
{%- endmaterialization -%}
