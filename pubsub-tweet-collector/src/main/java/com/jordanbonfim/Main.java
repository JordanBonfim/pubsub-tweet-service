package com.jordanbonfim;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.*;


public class Main {

    private final static String QUEUE_NAME = "work_queue";
    public static void main(String[] args) throws Exception{

        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");


        Gson gson = new GsonBuilder()
                .serializeNulls()
                .create();

        FileReader reader = new FileReader("tweets2.json");

        Type listType = new TypeToken<List<Tweet>>(){}.getType();

        List<Tweet> tweets = gson.fromJson(reader, listType);



        Map<String, Object> queue_args = new HashMap<String, Object>();
        queue_args.put("x-queue-type", "classic");
        queue_args.put("x-message-ttl", 90000);

        try (Connection connection = factory.newConnection();

             Channel channel = connection.createChannel()) {
            channel.queueDeclare(QUEUE_NAME, true, false, false, queue_args);

            List<Tweet> batch = new ArrayList<>();

            for (int i = 1; i < tweets.size()+1; i += 1) {
                batch.add(tweets.get(i-1));
                if(i % 10 == 0){
                    String json = gson.toJson(batch);

                    channel.basicPublish(
                            "",
                            QUEUE_NAME,
                            null,
                            json.getBytes(StandardCharsets.UTF_8)
                    );

                    System.out.println("Sent batch: " + batch.toString());
                    batch.clear();
                    Thread.sleep(5000);
                }
            }

            // Ainda tem elementos para enviar
            if(batch.size()>0){
                String json = gson.toJson(batch);
                channel.basicPublish(
                        "",
                        QUEUE_NAME,
                        null,
                        json.getBytes(StandardCharsets.UTF_8)
                );

                System.out.println("Sent batch");
                batch.clear();
                Thread.sleep(5000);
            }
        }
        reader.close();
    }
}