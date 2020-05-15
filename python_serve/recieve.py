#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('user', 'user')
parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_qos(prefetch_count=2)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()