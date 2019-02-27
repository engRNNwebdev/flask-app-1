Docker Flask App

Steps to add a user to db

1: $ docker exec -it flask-app_web_1 /bin/sh
2: $ from app import db
3: $ from models import User
4: $ u = User(username='INSERT USERNAME', email='INSERT EMAIL')
5: $ u.set_password('ENTER PASSWORD')
6: $ u.check_password('ENTER PASSWORD') ... should return true
7: $ db.session.add(u)
8: $ db.session.commit()

Run this command to create dbs from the models: python create_db.py
