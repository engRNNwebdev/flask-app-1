from flask import Flask, redirect, url_for, request, render_template, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import BaseConfig
from urlparse import urlparse
import uplynk, os, logging, links, re, shutil
from logging.handlers import RotatingFileHandler
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = set(['txt'])

#Initialize app
app = Flask(__name__)
#Initialize Bootstrap
Bootstrap(app)
#Initialize Login, Postgres and Upload folder
app.config.from_object(BaseConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
web = links.links()
web_prod = links.links_prod()
web_it = links.links_it()
web_ftp = links.links_ftp()
web_broadcast = links.links_broadcast()
#Create web page routes
@app.route('/', methods = ['POST', 'GET'])
@login_required
def index():
    app.logger.info('Index Page Loaded')
    return render_template('index.html', web=web, web_prod=web_prod, web_it=web_it, web_ftp=web_ftp, web_broadcast=web_broadcast)

@app.route('/status/<actionthing>/<name>/<success>')
@login_required
def status(name,actionthing,success):
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
    return render_template('uplynk_control.html',slicers=db_slicers, worky = 'Select a Slicer and give the Asset a title and External ID (can be the same)')

@app.route('/preview')
@login_required
def preview():
    return render_template('preview.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/loganalysis', methods = ['POST', 'GET'])
@login_required
def loganalysis():
    errors = ['Blah blah blah\n']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            errors = ['No Results Available']
            return render_template('parser.html', errors=errors)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            errors = ['No Results Available']
            return render_template('parser.html', errors=errors)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.chdir(r'/tmp/') #establish dir to pull file from
            logentries = []
            with open(filename, 'r') as f:
                for line in f:
                    try:
                        logentries.append(line)
                    except:
                        logentries.append('Cannot add line :(\n')
                f.close()
            return render_template('parser.html', logentries=logentries)
            # return redirect(url_for('uploaded_file', filename=filename))
        errors =['Welp, nothing happened']
        return render_template('parser.html', errors=errors)
    elif request.method == 'GET':
        errors = ['Upload a .txt file with this tool to query and filter logs']
        return render_template('parser.html', errors=errors)

@app.route('/materialid', methods = ['POST', 'GET'])
@login_required
def material_id():
    if request.method == 'POST':
        return render_template('materialid.html')
    elif request.method == 'GET':
        return render_template('materialid.html')

@app.route('/init', methods = ['POST', 'GET'])
@login_required
def init():
    option = request.args.get('option')
    app.logger.info(option)
    if request.method == 'POST':
        if option == '1':
            folder = os.getenv('UPLOAD_FOLDER')
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
            errors = ['Logs have been deleted from disk']
            return render_template('parser.html', errors=errors)
        if option == '2':
            uplynk1 = Slicer(slicer_id=os.getenv('SLICER_ID_ONE'), address=os.getenv('SLICER_ADDRESS_ONE'), port=os.getenv('SLICER_PORT_ONE'), channel_id=os.getenv('SLICER_CHANNEL_ID_ONE'))
            uplynk2 = Slicer(slicer_id=os.getenv('SLICER_ID_TWO'), address=os.getenv('SLICER_ADDRESS_TWO'), port=os.getenv('SLICER_PORT_TWO'), channel_id=os.getenv('SLICER_CHANNEL_ID_TWO'))
            db.session.add_all([uplynk1, uplynk2])
            # db.session.add(uplynk2)
            db.session.commit()
            app.logger.info('Init slicers')
            errors = ['db Initiation has been performed... Check data for confirmation.']
            return render_template('parser.html', errors=errors)
        else:
            app.logger.info('Failed post message')
            return render_template('404.html')
    elif request.method == 'GET':
        app.info.logger('Attempted get on init page')
        return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Run App and startup
if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), host='0.0.0.0:5000')
