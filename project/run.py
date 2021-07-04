from flask import Flask ,render_template ,request, redirect ,url_for ,session, flash , Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from controllers import *
from werkzeug.utils import secure_filename
import os
import cv2
import models
from models import *


app = Flask(__name__)
app = Flask(__name__,instance_relative_config=True)


#config_call 

#db = SQLAlchemy(app)
db = SQLAlchemy()
db.init_app(app)
app.config.from_object('config')
app.config.from_pyfile('config.py')


#Create DB
Migrate=Migrate(app,db)

#call static files (css,js)
css_admin = Bundle('css/all.min.css', 'css/bootstrap.min.css', 'css/fontawesome.min.css', output='gen/packed.css')
js = Bundle('js/Jquery.js', 'js/bootstrap.min.js', 'js/fontawesome.min.js','js/all.min.js', output='gen/packed.js')
assets = Environment(app)
assets.register('css_admin', css_admin)
assets.register('js_all', js)

#Extentions allowed
ALLOWED_EXTENSIONS = {'dicm', 'dcm'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#main route (home)
@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')


#login function
@app.route('/Login',methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = models.user.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect("/Login")
        else: 
            session['user'] = user
            return redirect("/index")
    return render_template('Login.html')

#Register function
@app.route('/Register',methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        user = models.user(username=request.form["userName"], first_name=request.form["firstName"],
                            last_name=request.form["lastName"], email=request.form["Email"], password=generate_password_hash(request.form["password"], method='sha256'), User_type=2)
        db.session.add(user)
        db.session.commit()
        session['user']= user
        return render_template('index.html')
        
    return render_template('Register.html')

#view function
@app.route('/viewProfile',methods=['GET', 'POST'])
def viewProfile():
    user_update = models.user.query.filter_by(id= session['user'].get("id"))
    if request.method == 'POST':
        user_update.username = request.form["username"]
        user_update.first_name = request.form["firstName"]
        user_update.last_name = request.form["lastName"]
        user_update.email = request.form["email"]
        user_update.password = generate_password_hash(request.form["password"], method='sha256')
        db.session.commit()
        return redirect("/index")
    return render_template('viewProfile.html', profile=user_update)

#view for admin function
@app.route('/viewUsers',methods=['GET', 'POST'])
def viewUsers():
    users = models.user.query.all()
    return render_template('viewUsers.html', users=users)

#add feedback function (user)
@app.route('/addFeedback',methods=['GET', 'POST'])
def addFeedback():
    if request.method == 'POST':
        feedback = models.feedback(user_id=session['user'].get("id"), comment=request.form['comment'], Date = datetime.now())
        db.session.add(feedback)
        db.session.commit()
        return render_template('index.html')
    return render_template('addFeedback.html')

#view feedback function (admin)
@app.route('/viewFeedback',methods=['GET', 'POST'])
def viewFeedback():
    feedbacks = models.feedback.query.all()
    return render_template('viewFeedback.html', feedbacks=feedbacks)

#logout function 
@app.route('/Logout',methods=['GET', 'POST'])
def Logout():
    session.pop('user',None)
    return render_template('index.html')


# delete user 
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_delete = models.user.query.filter_by(id=id)
    db.session.delete(user_delete)
    db.session.commit()
    return redirect("/viewUsers")
# user = models.user.query.filter_by(id=id).first()
#service function
@app.route('/service',methods=['GET', 'POST'])
def service():
    
    return render_template('service.html')

#upload function 
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
            CT = models.CT_scan(user_idimage_path=filename)
            db.session.add(CT)
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = app.config['UPLOAD_FOLDER'] + filename
            re = Read_all.ReadAll(filepath)
            return render_template('service.html',afile=re)
        
    return render_template('service.html')

#for run
if __name__ == '__main__':
    
    #app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
    app.run(debug=True)
with app.app_context():
    db.create_all()
