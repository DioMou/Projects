package org.bankBalance;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.junit.jupiter.api.Test;
import org.testng.Assert;

import java.io.IOError;
import java.io.IOException;

public class bankBalanceProducerTest {
    @Test
    public void newRandomTransactionTest(){
        ProducerRecord<String,String> record= bankBalanceProducer.newRandomTrasaction("john");
        String key=record.key();
        String value = record.value();

        Assert.assertEquals(key,"john");
        ObjectMapper mapper = new ObjectMapper();
        try{
            JsonNode node =mapper.readTree(value);
            Assert.assertEquals(node.get("name").asText(),"john");
            Assert.assertTrue(node.get("amount").asInt()<100," : amount is less than 100");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
