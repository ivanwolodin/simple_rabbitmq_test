#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('user', 'user')
parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='boobs!')
print(" [x] Sent 'I am the best!'")
connection.close()