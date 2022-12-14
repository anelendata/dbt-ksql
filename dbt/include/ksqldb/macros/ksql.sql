{% macro with(
    timestamp=None,
    partitions=None,
    replicas=None,
    key_format=None,
    value_format=None,
    kafka_topic=None
)
%}
with (
    {% if timestamp %}timestamp='{{ timestamp }}',{% endif %}
    {% if partitions %}partitions={{ partitions }},{% endif %}
    {% if replicas %}replicas={{ replicas }},{% endif %}
    {% if key_format %}key_format='{{ key_format }}',{% endif %}
    {% if value_format %}value_format='{{ value_format }}',{% endif %}
    kafka_topic='{% if kafka_topic %}{{ kafka_topic }}{% else %}{{ this.include(database=True) }}{% endif %}'
)
{% endmacro %}

{% macro drop_stream(relation, delete_topic=false) -%}
{% set query %}
{% if delete_topic %}
drop stream {{ relation }} delete topic
{% else %}
drop stream {{ relation }}
{% endif %}
{% endset %}
{% do run_query(query) %}
{%- endmacro %}

{% macro drop_table(relation, delete_topic=false) -%}
{% set query %}
{% if delete_topic %}
drop table {{ relation }} delete topic
{% else %}
drop table {{ relation }}
{% endif %}
{% endset %}
{% do run_query(query) %}
{%- endmacro %}

