FROM ubuntu:latest
MAINTAINER Jonathan Ferraro "engstaff@rnntv.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
#You are using pip version 8.1.1, however version 9.0.1 is available.
#You should consider upgrading via the 'pip install --upgrade pip' command
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
