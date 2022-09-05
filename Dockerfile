# base image
FROM ubuntu:20.04

RUN useradd -m app

# setup environment variable
ENV ProjectPath=/home/app/panel

# set work directory
RUN mkdir -p $ProjectPath

# where your code lives
WORKDIR $ProjectPath

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required libraries and programs
RUN apt-get update && apt-get install -y gcc python3-dev python3-pip nano

# copy whole project to your docker home directory.
COPY --chown=app:app . $ProjectPath

# run this command to install all dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt  

# port where the Django app runs  
EXPOSE 80

# start server  
CMD gunicorn server:app -w 1 -b 0:80
