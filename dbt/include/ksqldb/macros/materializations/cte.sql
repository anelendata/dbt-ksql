{%- materialization cte, adapter='ksqldb' -%}
    {{ exceptions.raise_compiler_error(
        """
        dbt-ksql does not support CTEs
        Perhaps you want to use stream or table?
        """
    )}}
{%- endmaterialization -%}
