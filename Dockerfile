FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD /nginx/sites-enabled/ /etc/nginx/sites-enabled

# FROM python:2.7
# ADD . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# FROM ubuntu:trusty
FROM python:2.7-alpine
MAINTAINER Jonathan Ferraro "engstaff@rnntv.com"
# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN apk add --update python py-pip
ADD /web /app
WORKDIR /app
RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["python", "-u", "/app/app.py"]
