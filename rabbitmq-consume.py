import pika
import time
import json
import requests


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='test', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def req(body):
    url = "http://fastmovie.online:9091/es"
    payload = json.dumps(body)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    json_body = json.loads(str(body, 'utf-8'))
    req(json_body)
    time.sleep(1)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=callback)

channel.start_consuming()