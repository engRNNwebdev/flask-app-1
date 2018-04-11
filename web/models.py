# models.py


import datetime
from app import db


<<<<<<< HEAD
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
=======
class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)

    def __init__(self, text):
        self.text = text
        self.date_posted = datetime.datetime.now()
>>>>>>> afb50f78d0c51b87691e57d282c7435b82a1fcf8
