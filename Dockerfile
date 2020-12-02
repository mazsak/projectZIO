FROM python:3.6-alpine

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY Pipfile* ./

RUN apk update

RUN apk add --update curl

RUN apk add --no-cache bash

RUN apk add --update openjdk8

RUN curl -s https://get.nextflow.io | bash

RUN pip install --no-cache-dir pipenv \
    && pipenv install --system --deploy --clear \
    && pip uninstall pipenv -y

COPY . .

WORKDIR /usr/src/app

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD echo Django application is running