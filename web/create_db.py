# create_db.py
import os
from app import db
from models import *
db.create_all()
slicer = Slicer(slicer_id=os.getenv('SLICER_ID_ONE'), address=os.getenv('SLICER_ADDRESS_ONE'), port=os.getenv('SLICER_PORT_ONE'), channel_id=os.getenv('SLICER_CHANNEL_ID_ONE'))
print 'Slicer made'
# db.session = sessionmaker(bind = engine)()
db.session.add(slicer)
print 'Slicer added'
