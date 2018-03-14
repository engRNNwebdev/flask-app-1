from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
import uplynk
#Initialize app and Bootstrap

app = Flask(__name__)
Bootstrap(app)

#Create web page routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/success/<actionthing>/<name>')
def success(name,actionthing):
    if actionthing == 'stop':
        return 'Successfully stopped on port %s' % name
    elif actionthing == 'start':
        return 'Successfully started on port %s' % name
@app.route('/failure/<actionthing>/<name>')
def failure(name):
    if actionthing == 'stop':
        return 'The Slicer failed to stop %s, please escalate to Engineering' % name
    elif actionthing == 'start':
        return 'The Slicer failed to start on port %s, please escalate to Engineering' % name
@app.route('/login', methods = ['POST', 'GET'])
def login():
  if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
  else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))
@app.route('/content_start', methods = ['POST', 'GET'])
def start_slicer():
  if request.method == 'POST':
      eid = request.form['eid']
      slicer = request.form['slicers']
      uplynk.content_start(slicer,eid)
      return redirect(url_for('success', actionthing = 'start', name = eid))
  else:
      sliced = request.args.get('slicers')
      return redirect(url_for('failure',name = sliced))
@app.route('/blackout', methods = ['POST', 'GET'])
def blackout_slicer():
  if request.method == 'POST':
      slicer = request.form['slicers']
      uplynk.blackout(slicer)
      return redirect(url_for('success',actionthing = 'stop', name = slicer))
  else:
      sliced = request.args.get('slicers')
      return redirect(url_for('failure',name = sliced))
@app.route('/uplynk')
def uplynk_control():
    slicers = uplynk.slicers
    return render_template('uplynk_control.html',slicers=slicers)
@app.route('/materialid')
def material_id():
  return 'Material ID page goes here'
#Run App and startup
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
