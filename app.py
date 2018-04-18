from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import uplynk, os, logging
from logging.handlers import RotatingFileHandler
#Initialize app
app = Flask(__name__)
#Initialize Bootstrap
Bootstrap(app)
#Initialize Mongo Client
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
from models import *

#Create web page routes

@app.route('/', methods = ['POST', 'GET'])
def index():
    app.logger.info('TEST PRINT')
    posted = 'TEST PRINT'
    return render_template('index.html', test = posted)

@app.route('/status/<actionthing>/<name>/<success>', methods = ['POST', 'GET'])
def status(name,actionthing,success):
    slicers = uplynk.slicers
    if request.method == 'POST':
        if success:
            if actionthing == 'stop':
                return render_template('uplynk_control.html', slicers = slicers, worky = 'Successfully stopped on port %s' % name)
            elif actionthing == 'start':
                return render_template('uplynk_control.html', slicers = slicers, worky = 'Successfully started on port %s' % name)
        else:
            if actionthing == 'stop':
                return render_template('uplynk_control.html', slicers = slicers, worky = 'The Slicer failed to stop on port %s, please escalate to Engineering')
            elif actionthing == 'start':
                return render_template('uplynk_control.html', slicers = slicers, worky = 'The Slicer failed to start on port %s, please escalate to Engineering' % name)
    else:
        return render_template('uplynk_control.html', slicers = slicers, worky = 'The Slicer failed to start on port %s, please escalate to Engineering' % name)

@app.route('/login', methods = ['POST', 'GET'])
def login():
  if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
  else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/content_start', methods = ['POST', 'GET'])
def start_slicer(methods = ['POST', 'GET']):
  if request.method == 'POST':
      external_id = request.form['external_id']
      slicer = request.form['slicers']
      title = request.form['title']
      uplynk.content_start(slicer,external_id,title)
      #return render_template('uplynk_control.html', status_capture = 'result')
      return redirect(url_for('status', actionthing = 'start', name = slicer, success = True))
  else:
      sliced = request.args.get('slicers')
      return redirect(url_for('status', actionthing = 'start', name = sliced, success = False))

@app.route('/blackout', methods = ['POST', 'GET'])
def blackout_slicer():
  if request.method == 'POST':
      slicer = request.form['slicers']
      result = uplynk.blackout(slicer)
      #return render_template('uplynk_control.html',status_capture = 'result')
      return redirect(url_for('status', actionthing = 'stop', name = slicer, success = True))
  else:
      sliced = request.args.get('slicers')
      return redirect(url_for('status', actionthing = 'stop', name = sliced, success = False))

@app.route('/uplynk')
def uplynk_control():
    db_slicers = Slicer.query.order_by(Slicer.id.desc()).all()
    app.logger.info(db_slicers)
    slicers = uplynk.slicers
    return render_template('uplynk_control.html',slicers=db_slicers, worky = 'Select a Slicer and give the Asset a title and External ID (can be the same)')

@app.route('/preview')
def preview():
    return render_template('preview.html');

@app.route('/materialid')
def material_id():
  return 'Material ID page goes here'

#Run App and startup
if __name__ == '__main__':
    app.run(debug=True)
