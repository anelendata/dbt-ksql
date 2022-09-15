{%- materialization view, adapter='ksqldb' -%}
    {{ exceptions.raise_compiler_error(
        """
        dbt-ksql does not support views
        Perhaps you want to use stream or table?
        """
    )}}
{%- endmaterialization -%}
