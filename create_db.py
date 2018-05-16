# create_db.py
import os
from app import db
from models import *
# Add all db models
db.create_all()
# Add Slicers
