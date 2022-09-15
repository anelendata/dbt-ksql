{%- materialization stream, adapter='ksqldb' -%}

  {%- set target_relation = this.incorporate(type='stream') -%}

  {% set grant_config = config.get('grants') %}

  {{ run_hooks(pre_hooks, inside_transaction=False) }}

  -- `BEGIN` happens here:
  {{ run_hooks(pre_hooks, inside_transaction=True) }}

  -- build model
  {% call statement('main') -%}
    {{ get_create_stream_as_sql(target_relation, sql) }}
  {%- endcall %}

  -- grant access code here?
  -- See https://github.com/dbt-labs/dbt-bigquery/blob/84c20fcef86d9777b6ce6a4745b6415ec288ed93/dbt/include/bigquery/macros/materializations/stream.sql

  {% do persist_docs(target_relation, model) %}

  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {{ adapter.commit() }}

  {{ run_hooks(post_hooks, inside_transaction=False) }}

  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}


{% macro get_create_stream_as_sql(relation, sql) -%}
  {{ adapter.dispatch('get_create_stream_as_sql', 'dbt')(relation, sql) }}
{%- endmacro %}

{% macro ksqldb__get_create_stream_as_sql(relation, sql) -%}
  {{ return(create_stream_as(relation, sql)) }}
{% endmacro %}

/* {# keep logic under old name for backwards compatibility #} */
{% macro create_stream_as(relation, sql) -%}
  {{ adapter.dispatch('create_stream_as', 'dbt')(relation, sql) }}
{%- endmacro %}

{% macro ksqldb__create_stream_as(relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}
  create or replace stream {{ relation.include(database=False) }}
    {{ sql }}
  ;
{%- endmacro %}


