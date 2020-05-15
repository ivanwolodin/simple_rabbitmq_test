FROM python:3.7

ENV to_working_dir /home/rbmq_app

WORKDIR                 ${to_working_dir}
COPY .                  /$to_working_dir

RUN apt-get update   && apt-get install nano
RUN apt-get update   && apt-get install net-tools
RUN apt-get update   && apt-get -y install libpython3.7-dev

RUN python -m pip install pika --upgrade

CMD tail -f /dev/null # to prevent exiting
