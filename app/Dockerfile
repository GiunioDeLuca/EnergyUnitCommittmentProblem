FROM python:3.6.5

MAINTAINER GIUNIO Name "giuniodl@live.it"

ENV AM_I_IN_DOCKER_CONTAINER Yes

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN pip install -r requirements.txt

#EXPOSE 8888

ENTRYPOINT ["python", "/app/app.py"]
