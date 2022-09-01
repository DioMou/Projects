package org.bankBalance;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.KeyValueStore;

import java.io.IOException;
import java.io.ObjectInputFilter;
import java.time.Instant;
import java.util.Properties;

public class bankBalanceApp {
    public static void main(String[] args) {
        Properties config = new Properties();
        config.put(StreamsConfig.APPLICATION_ID_CONFIG,"bank-balance");
        config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG,"localhost:9092");
        config.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");

        config.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG,"0");
        // Exactly once processing!!
        config.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once");

        ObjectNode initialBalance = JsonNodeFactory.instance.objectNode();
        initialBalance.put("count", 0);
        initialBalance.put("balance", 0);
        initialBalance.put("time", Instant.ofEpochMilli(0L).toString());

        //json serde
        final Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        final Deserializer<JsonNode> jsonDeSerializer = new JsonDeserializer();
        final Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer,jsonDeSerializer);


        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, JsonNode> balanceInput= builder.stream("bank-transactions", Consumed.with(Serdes.String(),jsonSerde));
        KTable<String,JsonNode> bankBalance =balanceInput.groupByKey(Grouped.with(Serdes.String(),jsonSerde))
                .aggregate(
                        ()->initialBalance,
                        (key,transaction,balance)->newBalance(transaction,balance),
                        Materialized.<String,JsonNode, KeyValueStore<Bytes,byte[]>>as("tempbalance-agg")
                                .withKeySerde(Serdes.String())
                                .withValueSerde(jsonSerde)
                );
        bankBalance.toStream().to("bank_balance_output",Produced.with(Serdes.String(),jsonSerde));
        KafkaStreams streams = new KafkaStreams(builder.build(),config);
        streams.cleanUp();
        streams.start();

        streams.metadataForLocalThreads().forEach(data->System.out.println(data));
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));

    }
    private static ObjectNode newBalance(JsonNode newTransaction,JsonNode balance){
        ObjectNode newBalance = JsonNodeFactory.instance.objectNode();
        newBalance.put("count",balance.get("count").asInt()+1);
        newBalance.put("balance",newTransaction.get("amount").asInt()+balance.get("balance").asInt());

        Long newTime=Instant.parse(newTransaction.get("time").asText()).toEpochMilli();
        Long balanceTime= Instant.parse(balance.get("time").asText()).toEpochMilli();
        Instant realMaxTime=Instant.ofEpochMilli(Math.max(newTime,balanceTime));
        newBalance.put("time",realMaxTime.toString());
        return newBalance;
    }
}
