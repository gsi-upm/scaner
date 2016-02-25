FROM python:3-onbuild

ENV REDIS_HOST redis
ENV ORIENTDB_HOST orientdb

ADD run-web.sh /usr/local/bin/
ADD run-celery.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run-web.sh
RUN chmod +x /usr/local/bin/run-celery.sh

CMD ["run-web.sh"]