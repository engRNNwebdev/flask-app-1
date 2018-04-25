# create_db.py

from app import db
from models import *
db.create_all()
uplynk1 = Slicer(slicer_id=os.getenv('SLICER_ID_ONE'), address=os.getenv('SLICER_ADDRESS_ONE'), port=os.getenv('SLICER_PORT_ONE'), channel_id=os.getenv('SLICER_CHANNEL_ID_ONE'))
uplynk2 = Slicer(slicer_id=os.getenv('SLICER_ID_TWO'), address=os.getenv('SLICER_ADDRESS_TWO'), port=os.getenv('SLICER_PORT_TWO'), channel_id=os.getenv('SLICER_CHANNEL_ID_TWO'))
db.session.add_all([uplynk1, uplynk2])
# db.session.add(uplynk2)
db.session.commit()
posted = Slicer.query.order_by(Slicer.id.desc()).all()
