{%- materialization table, adapter='ksqldb' -%}

  {%- set target_relation = this.incorporate(type='table') -%}

  {% set grant_config = config.get('grants') %}

  {{ run_hooks(pre_hooks, inside_transaction=False) }}

  -- `BEGIN` happens here:
  {{ run_hooks(pre_hooks, inside_transaction=True) }}

  -- build model
  {% call statement('main') -%}
    {{ get_create_table_as_sql(target_relation, sql) }}
  {%- endcall %}

  -- grant access code here?
  -- See https://github.com/dbt-labs/dbt-bigquery/blob/84c20fcef86d9777b6ce6a4745b6415ec288ed93/dbt/include/bigquery/macros/materializations/table.sql

  {% do persist_docs(target_relation, model) %}

  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {{ adapter.commit() }}

  {{ run_hooks(post_hooks, inside_transaction=False) }}

  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}
