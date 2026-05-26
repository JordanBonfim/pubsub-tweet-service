package com.jordanbonfim;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;


public class Main {

    private final static String QUEUE_NAME = "work_queue";
    public static void main(String[] args) throws Exception{

        Random rand = new Random();


        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");


        Gson gson = new GsonBuilder()
                .serializeNulls()
                .create();

        FileReader reader = new FileReader("tweets2.json");

        Type listType = new TypeToken<List<Tweet>>(){}.getType();

        List<Tweet> tweets = gson.fromJson(reader, listType);

        System.out.println(tweets.size());
        System.out.println(tweets.get(0).content);




        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            channel.queueDeclare(QUEUE_NAME, true, false, false, Map.of("x-queue-type", "quorum"));

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