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
    # def __init__(self, text):
    #     self.text = text
    #     self.date_posted = datetime.datetime.now()

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

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(200), index=True, unique=True)

    def __repr__(self):
        return "<User(name='%s', url='%s')>" % (
                                self.name, self.url)
# [
#   {
#     "slicer_id": "rnnuplynk1",
#     "address": "192.168.101.15",
#     "port": 65009,
#     "channel_id": "Fios1News Long Island PGM"
#   },
#   {
#     "slicer_id": "rnnuplynk2",
#     "address": "192.168.101.15",
#     "port": 65011,
#     "channel_id": "Fios1News Long Island CLN"
#   }
# ]
