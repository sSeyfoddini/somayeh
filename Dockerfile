# Python-Basisimage
FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY / /app


CMD  ["uwsgi", "--http", "0.0.0.0:80", "--module", "wsgi:app", "--processes", "8", "--threads", "8"]
