import sys

import pika
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MyWindow(QMainWindow):
    """ gui """
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.textEdit_2.setEnabled(False)
        self.textEdit_2.setText('Press button to start listening')
        self.pushButton.pressed.connect(self.start_listening)
        # self.serial.readyRead.connect(self.do_after_data_recieved)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        self.textEdit.setText(body)

    def start_listening(self) -> None:
        try:
            credentials = pika.PlainCredentials('user', 'user')
            parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials)
            connection = pika.BlockingConnection(parameters)

            # connection = pika.BlockingConnection(
            #     pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='hello')
            channel.basic_consume(
                queue='hello',
                on_message_callback=self.callback,
                auto_ack=True
            )

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

            # channel.basic_qos(prefetch_count=2)
        except Exception as e:
            self.textEdit_2.setText('Invalid credentials')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
