Проект, состоящий из двух приложений: - клиент и сервер. Суть решения - удаленный монитор содержимого каталога.

Сервер получает путь к каталогу через аргументы командной строки. 
Клиенту получает адрес сервера.
Сервер следит за изменениями в заданном каталоге, и, если содержимое изменилось, оно должно быстро обновиться на клиенте.

Решение с использованием amqp.

-------------------------------------------------------------------------------------------------------------------------

Решение использует:

    * python 3.7
    * RabbitMQ
    * библиотеку PyQt 5.14 (для gui)
    * pika 1.1.0 (для соединения с RabbitMQ)


При помощи Докера проект разворачивается на одном компьютере по схеме приведенной на рисунке.


![application_pattern](python_serve/application_pattern.png)


После запуска ***docker-compose up -d*** (в папке с файлом .yaml)
разворачивается два контейнера, находящиеся в одной сети. 

Первый сервис разворачивает **RabbitMQ**, создает пользователя user с паролем user через shell-скрипт.
Второй сервис *python_serve* скачивает нужные библиотеки, в нем нужно запустить скрипт *watchdog.py* 
в фоновом режиме ***python async_rabbitmq_sender.py  path_to_follow url & ***

Исходя из настроек в .yaml , *url=rabbitmq_1* (можно сделать это автоматически, изменив настройки в .yaml).

На компьютере хосте нужно развернуть приложение ***python gui_listener.py url*** 
По-умолчанию, при разворачивании приложения с докерами *url=127.0.0.1*
GUI приложение многопоточное. В отдельном потоке обрабатываются принятия сообщений от RabbitMQ.

Внешний вид графического приложения gui_listener


![gui](python_serve/gui.png)


После этого нужно в контейнере сервиса python_serve переместиться в директорию, указанную в *path_to_follow* и начать менять структуру директории.

Теперь при любом изменении *path_to_follow* скрипт *async_rabbitmq_sender.py* будет отправлять сообщения в очередь rabbit_mq, 
а компьютер-хост контейнеров при помощи *gui_listener.py* будет их немедленно получать
