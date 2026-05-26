import pika
import time
import json


    
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

consume_channel = connection.channel()
consume_channel.queue_declare(queue='work_queue', durable=True, arguments={'x-queue-type': 'quorum'})
print('Waiting for tweets.')


publish_channel = connection.channel()
publish_channel.exchange_declare(exchange='tweets_topics',exchange_type='topic')


def classify_tweet(dict_tweet):

    topics = []

    author = dict_tweet["author"].lower()
    content = dict_tweet["content"].lower()

    # SPORTS
    sports_words = [
        "worldcup",
        "soccer",
        "football",
        "fifa",
        "goal",
        "cup",
        "lakers",
        "golf",
        "match",
        "league",
        "basketball"
    ]

    if author == "cristiano":
        topics.append("sports")
        topics.append("soccer")

    for word in sports_words:
        if word in content:
            topics.append("sports")
            break

    # MUSIC
    music_words = [
        "music",
        "song",
        "album",
        "playlist",
        "itunes",
        "mixtape",
        "concert",
        "studio"
    ]

    singers = [
        "selenagomez",
        "jtimberlake",
        "katyperry",
        "ladygaga",
        "justinbieber",
        "rihanna"
    ]

    if author in singers:
        topics.append("music")

    for word in music_words:
        if word in content:
            topics.append("music")
            break

    # MOVIES
    movie_words = [
        "movie",
        "film",
        "trailer",
        "disney",
        "theaters",
        "series",
        "superhero"
    ]

    for word in movie_words:
        if word in content:
            topics.append("movies")
            break

    # TECHNOLOGY
    tech_words = [
        "twitter",
        "api",
        "system",
        "downtime",
        "tweets",
        "android",
        "github",
        "developers",
        "autopilot"
    ]

    if author in ["twitter", "google", "github", "tesla"]:
        topics.append("technology")

    for word in tech_words:
        if word in content:
            topics.append("technology")
            break

    # GAMES
    games_words = [
        "zelda",
        "minecraft",
        "counter-strike",
        "tournament",
        "patch",
        "players"
    ]

    if author in ["nintendo", "riotgames", "steam", "playstation"]:
        topics.append("games")

    for word in games_words:
        if word in content:
            topics.append("games")
            break

    # SPACE
    space_words = [
        "mars",
        "starship",
        "spacex",
        "falcon",
        "nasa",
        "hubble"
    ]

    if author in ["spacex", "nasa"]:
        topics.append("space")

    for word in space_words:
        if word in content:
            topics.append("space")
            break

    return list(set(topics))

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
        
        topics = classify_tweet(dict_tweet)
        
        
        for topic in topics:
            publish_channel.basic_publish(
                exchange='tweets_topics',
                routing_key=topic,
                body=(dict_tweet["author"]+" publicou: "+dict_tweet["content"])
            )
    time.sleep(3)             
    ch.basic_ack(delivery_tag=method.delivery_tag)


consume_channel.basic_qos(prefetch_count=1)
consume_channel.basic_consume(queue='work_queue', on_message_callback=callback)
consume_channel.start_consuming()