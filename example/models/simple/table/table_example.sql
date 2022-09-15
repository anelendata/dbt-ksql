/*
dbt-ksql will try to create ksql Table when materialized parameter is set as "table"

Again, the kafka_topic will be set as {{ this.database }}.{{ this.schema }}.{{ this.name }}
unless specified in with(kafka_topic="...") paramter.
*/
{{ config(materialized='table') }}

{{ with(
    partitions=6,
    replicas=3,
    timestamp='time',
    value_format='avro'
)}}
as
select
    id,
    latest_by_offset(price) as last_price,
from {{ ref('another_stream_by_create_stream_as') }}
window tumbling (size 3600 seconds)
where price is not null
group by id
emit changes
