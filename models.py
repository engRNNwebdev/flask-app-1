# models.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Slicer(db.Model):

    __tablename__ = 'slicers'

    id = db.Column(db.Integer, primary_key=True)
    slicer_id = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "<User(slicer_id='%s', address='%s', port='%s', channel_id='%s')>" % (
                                self.slicer_id, self.address, self.port, self.channel_id)

class MosObject(db.Model):

    __tablename__ = 'mosids'

    id = db.Column(db.Integer, primary_key=True)
    storySlug = db.Column(db.String, nullable=False)
    objID = db.Column(db.String, nullable=False)
    mosAbstract = db.Column(db.String, nullable=False)
    roID = db.Column(db.String, nullable=False)
    storyID = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "<User(storySlug='%s', objID='%s', mosAbstract='%s', roID='%s', storyID='%s')>" % (
                                self.storySlug, self.objID, self.mosAbstract, self.roID, self.storyID)

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Log(db.Model):

    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(10000), index=True)

    def __repr__(self):
        return "<Log(entry=%s)>" % (self.entry)
    def __init__(self, entry):
        self.entry = entry

class Link(db.Model):

    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(200), index=True, unique=True)
    category = db.Column(db.String(64), index=True, nullable=False)

    def __repr__(self):
        return "<Link(name='%s', url='%d', category='%f')>" % (
                                self.name, self.url, self.category)
    def __init__(self, name, url, category):
        self.name = name
        self.url = url
        self.category = category

class Item(db.Model):

    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True, unique=True)
    user = db.Column(db.String(64), index=True, unique=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean(), index=True)
    def  __repr__(self):
        return "<Item(item='%s', user='%s', complete'%s')>" % (self.item, self.user, self.complete)
    def __init__(self, text, user, complete):
        self.text = text
        self.user = user
        self.complete = complete
        self.date_posted = datetime.datetime.now()
