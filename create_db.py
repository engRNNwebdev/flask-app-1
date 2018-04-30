# create_db.py
import os
from app import db
from models import *
# Add all db models
db.create_all()
# Add Slicers
uplynk1 = Slicer(slicer_id=os.getenv('SLICER_ID_ONE'), address=os.getenv('SLICER_ADDRESS_ONE'), port=os.getenv('SLICER_PORT_ONE'), channel_id=os.getenv('SLICER_CHANNEL_ID_ONE'))
uplynk2 = Slicer(slicer_id=os.getenv('SLICER_ID_TWO'), address=os.getenv('SLICER_ADDRESS_TWO'), port=os.getenv('SLICER_PORT_TWO'), channel_id=os.getenv('SLICER_CHANNEL_ID_TWO'))
# Add User
user = User(username=os.getenv('WEB_USERNAME'), password_hash=os.getenv('WEB_SECRET_SUPER_PASS'), email=os.getenv('WEB_EMAIL'))
db.session.add_all([uplynk1, uplynk2, user])
# db.session.add(uplynk2)
db.session.commit()
posted = Slicer.query.order_by(Slicer.id.desc()).all()
