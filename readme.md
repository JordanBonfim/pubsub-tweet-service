# Publish/Subscribe Tweets Service using RabbitMQ

This project implements a simple Publish/Subscribe system using RabbitMQ to process tweets.



## Components
Publisher and Classifier have a producer/consumer relationship, while Classifier and Client use a publish/subscribe model.

It is possible to execute multiple classifiers simultaneously, allowing messages to be distributed among them.

### Publisher
Reads tweets from a pre-made JSON file and publishes them to a RabbitMQ queue.

### Classifier
Consumes tweets from the queue, classifies them into topics based on their content, and publish them to a
RabbitMQ topic exchange.

### Client
Consumes classified tweets from a topic queue and displays them to the user.

## Technologies
- Java for the publisher
- Python for the classifier and final client
- RabbitMQ
- Gson



## Execution Order
First, make sure Docker is installed.

Start RabbitMQ using the official community Docker image:


```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
``` 
1. Start RabbitMQ
2. Run the classifier
3. Run the client
4. Run the publisher