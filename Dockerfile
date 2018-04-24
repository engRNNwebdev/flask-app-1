#FROM ubuntu:latest
FROM python:2.7-alpine
MAINTAINER Jonathan Ferraro "engstaff@rnntv.com"
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
#RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN apk add --update python py-pip
RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY . /app

#RUN pip upg
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["python", "-u", "/app/app.py"]
