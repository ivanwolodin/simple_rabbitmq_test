#FROM python:3.7
FROM rabbitmq

# Define environment variables.
ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

ADD init.sh /init.sh
EXPOSE 15672/tcp
EXPOSE 5672/tcp

# Define default command
CMD ["/init.sh"]
