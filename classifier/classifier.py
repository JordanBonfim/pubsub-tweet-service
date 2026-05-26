import pika
import time
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

consume_channel = connection.channel()
consume_channel.queue_declare(queue='work_queue', durable=True, arguments={'x-queue-type': 'quorum'})
print('Waiting for tweets.')



def callback(ch, method, properties, body):

    tweets_json = json.loads(body.decode('utf-8').replace("'", '"'))
    print("Received "+str(len(tweets_json)) +" tweets.")
    
    for tweet in tweets_json:

        # Tratamento dos dados
        dict_tweet = {
            "author": tweet["author"],
            "content": tweet["content"],
            "date_time": tweet["dateTime"],
            "language": tweet["language"],
            "number_of_likes": tweet["numberOfLikes"],
            "number_of_shares": tweet["numberOfShares"]
        }
        print(dict_tweet)
    
        
        
        
    time.sleep(3)             
    ch.basic_ack(delivery_tag=method.delivery_tag)


consume_channel.basic_qos(prefetch_count=1)
consume_channel.basic_consume(queue='work_queue', on_message_callback=callback)
consume_channel.start_consuming()