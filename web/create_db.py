# create_db.py

from app import db
from models import *
db.create_all()
ed_slicer = Slicer(slicer_id='rnnuplynk1', address='192.168.101.15', port=65009, channel_id='Fios1News Long Island PGM')
db.session.add(ed_slicer)
posted = Slicer.query.order_by(Slicer.id.desc()).all()
