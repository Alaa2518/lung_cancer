from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

# from controllers import *


app = Flask('__name__')
app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

css_admin = Bundle('css/all.min.css', 'css/bootstrap.min.css', 'css/fontawesome.min.css', output='gen/packed.css')
js = Bundle('js/Jquery.js', 'js/bootstrap.min.js', 'js/fontawesome.min.js','js/all.min.js', output='gen/packed.js')
assets = Environment(app)
assets.register('css_admin', css_admin)
assets.register('js_all', js)

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(db, app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'dicm', 'dcm'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/Login',methods=['GET', 'POST'])
def Login():
    user = 2
    session['user'] = user
    if 'user' in session:
        session['user'] = session.get("user")
    else:
        session['user']= "object from user"
    return render_template('Login.html')


@app.route('/Register',methods=['GET', 'POST'])
def Register():
    return render_template('Register.html')


@app.route('/viewProfile',methods=['GET', 'POST'])
def viewProfile():
    return render_template('viewProfile.html')


@app.route('/viewUsers',methods=['GET', 'POST'])
def viewUsers():
    return render_template('viewUsers.html')



@app.route('/addFeedback',methods=['GET', 'POST'])
def addFeedback():
    return render_template('addFeedback.html')


@app.route('/viewFeedback',methods=['GET', 'POST'])
def viewFeedback():
    return render_template('viewFeedback.html')


@app.route('/Logout',methods=['GET', 'POST'])
def Logout():
    session.pop('user',None)
    return "logout"



@app.route('/serves',methods=['GET', 'POST'])
def serves():
    
    return render_template('serves.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # re = Read_all.ReadAll(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('serves.html')
        
    return render_template('serves.html')

if __name__ == '__main__':
    
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
    



