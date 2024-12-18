FROM python:3.11.3-slim-buster

ENV HOME /root
ARG LOG-LEVEL INFO

WORKDIR /app
RUN apt update && apt install default-jre -y

COPY requirements.txt /app/app/
RUN pip install -r /app/app/requirements.txt
RUN python -m nltk.downloader punkt

#COPY python files
COPY app /app/app
COPY migrations /app/migrations
COPY config.py /app/
COPY wsgi.py /app/

EXPOSE 80
ENTRYPOINT gunicorn --workers=2 --threads=4 --worker-class=gthread --log-file=- --log-level=$LOG-LEVEL -b 0.0.0.0:80 wsgi:app