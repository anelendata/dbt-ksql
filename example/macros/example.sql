{% macro common_cols() %}
    id,
    parse_timestamp(
        extractjsonfield({{ key }}, '$.updated'),
        'yyyy-MM-dd''T''HH:mm:ss.SSSX'
    )
{% endmacro %}
