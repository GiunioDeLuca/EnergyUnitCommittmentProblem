#FROM python:3.6.5
#FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
FROM quoinedev/python3.6-pandas-alpine

MAINTAINER GIUNIO Name "giuniodl@live.it"

ENV AM_I_IN_DOCKER_CONTAINER Yes

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN pip install -r requirements.txt

#EXPOSE 8888

ENTRYPOINT ["python", "/app/app.py"]
