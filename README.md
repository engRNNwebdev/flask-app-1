Docker Flask App

Next steps are to add a CI with Travis or something. 

## Deployment on local and remote host without CI 

1: SSH to Ubuntu Server

2: (Optional: New Server)

  a: $ git clone <URL>

2: (Optional: Update Repo in Server)

  a: $ git pull origin master

3: $ cd flask-app/

4: $ docker-compose build

5: $ docker-compose up -d
  
