FROM python:3.7-stretch

VOLUME /usr/src/app
VOLUME /usr/lib/python3/dist-packages

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ADD entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

ENTRYPOINT /entrypoint

