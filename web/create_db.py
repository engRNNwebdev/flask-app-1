# create_db.py

<<<<<<< HEAD
from app import db
from models import *
db.create_all()
ed_slicer = Slicer(slicer_id='rnnuplynk1', address='192.168.101.15', port=65009, channel_id='Fios1News Long Island PGM')
db.session.add(ed_slicer)
posted = Slicer.query.order_by(Slicer.id.desc()).all()
=======

from app import db

db.create_all()
>>>>>>> afb50f78d0c51b87691e57d282c7435b82a1fcf8
