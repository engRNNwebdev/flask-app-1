from flask import Flask, redirect, url_for, request, render_template
import uplynk
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
   return 'Successfully started %s' % name

@app.route('/failure/<name>')
def success(name):
    return 'The Slicer failed to start %s, please escalate to Engineering' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/content_start', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      eid = request.form['eid']
      uplynk.content_start(eid)
      return redirect(url_for('success',name = eid))
   else:
      user = request.args.get('eid')
      return redirect(url_for('failure',name = eid))

@app.route('/uplynk')
def uplynk_control():
    return render_template('uplynk_control.html')

@app.route('/materials')
def material_id():
    return 'Material ID page goes here'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
