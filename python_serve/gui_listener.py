import datetime
import sys

import pika
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

try:
    url = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
except:
    url = '127.0.0.1'


class BindRabbitMQ(QObject):
    image_signal = pyqtSignal(str)
    textEdit = None

    def __init__(self, textEdit):
        super(BindRabbitMQ, self).__init__()
        BindRabbitMQ.textEdit = textEdit

    @pyqtSlot()
    def bind_to_rabbit(self, ):
        credentials = pika.PlainCredentials('user', 'user')
        parameters = pika.ConnectionParameters(url, 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.queue_declare(queue='hello')
        channel.basic_consume(
            queue='hello',
            on_message_callback=BindRabbitMQ.callback,
            # on_message_callback=self.callback,
            auto_ack=True
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        BindRabbitMQ.textEdit.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        BindRabbitMQ.textEdit.append(body.decode("utf-8"))
        BindRabbitMQ.textEdit.append('*************************************')


class MyWindow(QMainWindow):
    """ gui """

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle('Messages from RabbitMQ')
        # self.textEdit.setEnabled(False)
        self.textEdit.setOverwriteMode(True)
        self.textEdit_2.setEnabled(False)
        self.textEdit_2.setText('Press button to start listening')
        self.pushButton.pressed.connect(self.start_listening)
        # self.serial.readyRead.connect(self.do_after_data_recieved)

        self.binder = BindRabbitMQ(self.textEdit)
        self.thread = QThread(self)
        self.binder.image_signal.connect(self.image_callback)
        self.binder.moveToThread(self.thread)
        self.thread.started.connect(self.binder.bind_to_rabbit)

    def start_listening(self) -> None:
        self.thread.start()
        self.textEdit_2.setText('Listening to {}'.format(url))
        # channel.basic_qos(prefetch_count=2)

    @pyqtSlot(str)
    def image_callback(self, filepath):
        self.textEdit_2.setText('Successfull connect')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
