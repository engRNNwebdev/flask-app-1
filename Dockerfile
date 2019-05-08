FROM python:2.7-alpine
MAINTAINER Jonathan Ferraro "engstaff@rnntv.com"
WORKDIR /app
COPY requirements.txt .
RUN apk add --update python py-pip
RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
RUN apk add --no-cache tzdata
ENV TZ America/New_York
COPY . /app
EXPOSE 5000
CMD ["python", "-u", "/app/app.py"]
