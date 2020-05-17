import os
import sys
import time

import pika
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    PATH = sys.argv[1] if len(sys.argv) > 1 else '.'
    URL = sys.argv[2] if len(sys.argv) > 2 else 'rabbitmq_1'
except:
    PATH = '.'
    URL = 'rabbitmq_1'


class RabbitSender():
    def __init__(self, user='user', password='user', url='rabbitmq_1', port=5672):
        self.chanel = None
        self.connection = None
        self.user = user
        self.password = password
        self.url = url
        self.port = port

    def initiate_broker_connection(self):
        credentials = pika.PlainCredentials(self.user,
                                            self.password)
        parameters = pika.ConnectionParameters(self.url,
                                               self.port,
                                               '/',
                                               credentials)

        self.connection = pika.BlockingConnection(parameters)
        #
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))

        self.chanel = self.connection.channel()
        self.chanel.queue_declare(queue='hello')
        return self.chanel, self.connection

    def close_connection(self):
        self.connection.close()


class MyHandler(FileSystemEventHandler):
    def __init__(self, path, channel):
        self.cur_path = path
        self.channel = channel

    def on_any_event(self, event):
        dirs = os.listdir(self.cur_path)
        self.channel.basic_publish(exchange='', routing_key='hello', body=', '.join(dirs))
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
    if validate_path(PATH) is False:
        # connection.close()
        exit(0)
    rabbit_sender_obj = RabbitSender()
    rabbit_sender_obj.initiate_broker_connection()
    event_handler = MyHandler(path=PATH,
                              channel=rabbit_sender_obj.chanel)

    observer = Observer()

    observer.schedule(event_handler, PATH, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        rabbit_sender_obj.close_connection()
    observer.join()
