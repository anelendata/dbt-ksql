/*
The kafka_topic will be set as {{ this.database }}.{{ this.schema }}.{{ this.name }}
unless specified in with(kafka_topic="...") paramter.
*/
{{ with(
    timestamp='time',
    partitions=3,
    replicas=3,
    key_format='avro',
    value_format='avro'
) }}
as
select
    {{ common_cols() }}
    cast(extractjsonfield(value, '$.price') as double) as price,
from {{ ref('a_stream_from_a_topic') }}
partition by id
emit changes
