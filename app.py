from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import BaseConfig
from urlparse import urlparse
import uplynk, os, logging
from logging.handlers import RotatingFileHandler
#Initialize app
app = Flask(__name__)
#Initialize Bootstrap
Bootstrap(app)
#Initialize Mongo Client
app.config.from_object(BaseConfig)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)

from models import *
from forms import *

# gunicorn logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

#Create web page routes

@app.route('/', methods = ['POST', 'GET'])
@login_required
def index():
    #posted = Slicer.query.order_by(Slicer.id.desc()).all()
    app.logger.info('TEST PRINT')
    posted = 'TEST PRINT'
    return render_template('index.html', test = posted)

@app.route('/status/<actionthing>/<name>/<success>')
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/content_start', methods = ['POST', 'GET'])
@login_required
def start_slicer():
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
@login_required
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
@login_required
def uplynk_control():
    db_slicers = Slicer.query.order_by(Slicer.id.desc()).all()
    app.logger.info(db_slicers)
    slicers = uplynk.slicers
    return render_template('uplynk_control.html',slicers=db_slicers, worky = 'Select a Slicer and give the Asset a title and External ID (can be the same)')

@app.route('/preview')
@login_required
def preview():
    return render_template('preview.html');

@app.route('/materialid', methods = ['POST', 'GET'])
@login_required
def material_id():
    if request.method == 'POST':
        return render_template('materialid.html')
    elif request.method == 'GET':
        return render_template('materialid.html')

@app.route('/init')
@login_required
def init():
    uplynk1 = Slicer(slicer_id=os.getenv('SLICER_ID_ONE'), address=os.getenv('SLICER_ADDRESS_ONE'), port=os.getenv('SLICER_PORT_ONE'), channel_id=os.getenv('SLICER_CHANNEL_ID_ONE'))
    uplynk2 = Slicer(slicer_id=os.getenv('SLICER_ID_TWO'), address=os.getenv('SLICER_ADDRESS_TWO'), port=os.getenv('SLICER_PORT_TWO'), channel_id=os.getenv('SLICER_CHANNEL_ID_TWO'))
    db.session.add_all([uplynk1, uplynk2])
    # db.session.add(uplynk2)
    db.session.commit()
    app.logger.info('Init slicers')
    posted = 'Initiated'
    return render_template('index.html', test = posted)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Run App and startup
if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0:5000')
