{%- materialization incremental, adapter='ksqldb' -%}

    {{ exceptions.raise_compiler_error(
        """
        dbt-ksql does not support incremental
        Perhaps you want to use stream or table?
        """
    )}}
{%- endmaterialization -%}
