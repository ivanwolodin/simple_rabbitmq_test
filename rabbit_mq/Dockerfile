FROM rabbitmq

ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

ADD init.sh /init.sh
EXPOSE 15672/tcp
EXPOSE 5672/tcp

# Here we create a non-default user 
CMD ["/init.sh"]
