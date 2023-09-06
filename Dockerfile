# pull official base image
FROM python:3.11-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# copy entrypoint
COPY ./entrypoint .
RUN sed -i 's/\r$//g' entrypoint
RUN chmod +x entrypoint

# create the additional directories
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/media

COPY ./start .
RUN sed -i 's/\r$//g' start
RUN ["chmod", "+x", "start"]

COPY ./start-celery-worker .
RUN sed -i 's/\r$//g' start-celery-worker
RUN ["chmod", "+x", "start-celery-worker"]

# run entrypoint
ENTRYPOINT ["sh", "/home/app/web/entrypoint"]