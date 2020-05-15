# FROM ubuntu:18.04
#FROM rabbitmq:latest
FROM python:3.7

MAINTAINER Ivan Volodin <ivanwolodin@gmail.com>

ENV to_working_dir /home/rbmq_app


WORKDIR                 ${to_working_dir}
COPY .                  /$to_working_dir

RUN apt-get update   && apt-get install nano
RUN apt-get update   && apt-get install net-tools
#RUN apt-get update   && apt-get -y install libpython3.7-dev

RUN python -m pip install pika --upgrade
RUN python -m pip install watchdog

CMD tail -f /dev/null # to prevent exiting
#ENTRYPOINT ["ping", "www.google.com"]
