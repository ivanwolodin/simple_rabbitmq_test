import os
import sys
import time

import pika
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def initiate_broker_connection():

    credentials = pika.PlainCredentials('user', 'user')
    parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    #
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    return channel, connection


channel, connection = initiate_broker_connection()
channel.queue_declare(queue='hello')


class MyHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.cur_path = path

    def on_any_event(self, event):
        dirs = os.listdir(self.cur_path)
        channel.basic_publish(exchange='', routing_key='hello', body=', '.join(dirs))
        print(" [x] Sent {} ".format(', '.join(dirs)))

    # Для оптимизации можно реализовать эти методы
    # def on_created(self, event):
    #     pass
    #
    # def on_deleted(self, event):
    #     pass
    #
    # def on_moved(self, event):
    #     pass


def validate_path(path):

    print('start looking directory {}'.format(path))
    try:
        if os.path.isdir(path):
            print('Big brother is here. Watching...')
            return True
        else:
            print('There is no such dir {}. Exiting'.format(path))
            return False
    except Exception as e:
        print('No such dir. Exception: {}'.format(e))
        return False


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    if validate_path(path) is False:
        connection.close()
        exit(0)

    event_handler = MyHandler(path)
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        connection.close()
    observer.join()