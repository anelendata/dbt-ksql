/* Creating a stream directly from a Kafka topic
*/
(
      id string key,
      time bigint,
      value string
)
{{ with(
      kafka_topic='some_kafka_topic_name',
      partitions=3,
      key_format='kafka',
      value_format='avro',
      timestamp='time'
)
}}
