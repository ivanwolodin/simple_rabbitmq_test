import os
import sys

import pika
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    PATH = sys.argv[1] if len(sys.argv) > 1 else '.'
    URL = sys.argv[2] if len(sys.argv) > 2 else 'rabbitmq_1'
except:
    PATH = '.'
    URL = 'rabbitmq_1'


class MyHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.cur_path = path

    def on_any_event(self, event):
        dirs = os.listdir(self.cur_path)
        # print(connection.is_open)

        on_open(connection)
        # on_channel_open(cha)
        # self.channel.basic_publish(exchange='', routing_key='hello', body=', '.join(dirs))
        print(" [x] Sent {} ".format(', '.join(dirs)))


# Step #3
def on_open(connection):
    # print('on open')
    connection.channel(on_open_callback=on_channel_open)


# Step #4
def on_channel_open(channel):
    # print('on channel')
    dirs = os.listdir(PATH)
    channel.basic_publish(exchange='', routing_key='hello', body=', '.join(dirs))

    # connection.close()


# Step #1: Connect to RabbitMQ
parameters = pika.URLParameters('amqp://user:user@{}:5672/%2F'.format(URL))

connection = pika.SelectConnection(parameters=parameters,
                                   on_open_callback=on_open)

try:
    event_handler = MyHandler(path=PATH)
    observer = Observer()

    observer.schedule(event_handler, PATH, recursive=True)

    observer.start()
    # Step #2 - Block on the IOLoop
    connection.ioloop.start()

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:
    print(connection.is_open)
    # Gracefully close the connection
    connection.close()

    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
    connection.ioloop.start()
