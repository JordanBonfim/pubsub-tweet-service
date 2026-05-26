import pika


available_topics = [
    "sports",
    "soccer",
    "music",
    "movies",
    "technology",
    "games",
    "space"
]

binding_keys = []
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

consume_channel = connection.channel()

try:
    print("Bem vindo")
    print("Digite 1 para se increver nos tópicos de interesse. Enter para pular para o próximo.")

    input("Aperte qualquer tecla para iniciar.")

    for topic in available_topics:
        entrada = input("Inscrever-se em:"+topic+"?")
        if(entrada=="1"):
            binding_keys.append(topic)
        
    print("Inscrito nos tópicos: ", binding_keys)

    consume_channel.exchange_declare(
        exchange='tweets_topics',
        exchange_type='topic'
    )

    result = consume_channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue


    for binding_key in binding_keys:
        consume_channel.queue_bind(
            exchange='tweets_topics', queue=queue_name, routing_key=binding_key)
        
    def callback(ch, method, properties, body):
        print(" ")
        print(" - "+body.decode('utf-8'))
        print(" ")

    consume_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print('Waiting for tweets.')
    consume_channel.start_consuming()
    
except KeyboardInterrupt:
    print("\nStopping subscriber")
    consume_channel.stop_consuming()
    print("Connection closed.")
