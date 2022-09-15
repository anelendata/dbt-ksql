{% macro get_create_table_as_sql(relation, sql) -%}
  {{ adapter.dispatch('get_create_table_as_sql', 'dbt')(relation, sql) }}
{%- endmacro %}

{% macro default__get_create_table_as_sql(relation, sql) -%}
  {{ return(create_table_as(relation, sql)) }}
{% endmacro %}


/* {# keep logic under old name for backwards compatibility #} */
{% macro create_table_as(relation, sql) -%}
  {{ adapter.dispatch('create_table_as', 'dbt')(relation, sql) }}
{%- endmacro %}

{% macro default__create_table_as(relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}
  create or replace table {{ relation.include(database=False) }}
    {{ sql }}
  ;
{%- endmacro %}
