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
        email = request.form['email']
        password = request.form['password']
        user = models.user.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for("Login"))
        else: 
            session['User_type'] = user.User_type
            session['user_id'] = user.id
            return redirect(url_for("index"))
    return render_template('Login.html')

#Register function
@app.route('/Register',methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        if request.form["userName"] != '' and request.form["firstName"] != '' and request.form["lastName"] != '' and request.form["Email"] != '' and request.form["password"] !='':
            user = models.user(username=request.form["userName"], first_name=request.form["firstName"],
                                last_name=request.form["lastName"], email=request.form["Email"], password=generate_password_hash(request.form["password"], method='sha256'), User_type=2)
            db.session.add(user)
            db.session.commit()
            session['User_type'] = user.User_type
            session['user_id'] = user.id
            return redirect(url_for("/index"))
            
    return render_template('Register.html')

#view function
@app.route('/viewProfile',methods=['GET', 'POST'])
def viewProfile():
    ID = session['user_id']
    # profile = models.user.query.get_or_404(id)
    profile = models.user.query.filter_by(id = ID).first()
    # profile = models.user.query.get(ID)

    
    if request.method == 'POST':
        profile.id = profile.id
        profile.User_type = profile.User_type
        if request.form["username"] != '':
            profile.username = request.form["username"]
        else:
            profile.username = profile.username

        if request.form["username"] != '':
            profile.first_name = request.form["firstName"]
        else:
            profile.first_name = profile.first_name

        if request.form["username"] != '':
            profile.last_name = request.form["lastname"]
        else:
            profile.last_name = profile.last_name

        if request.form["username"] != '':
            profile.email = request.form["email"]
        else:
            profile.email = profile.email

        if request.form["username"] != '':
            profile.password = generate_password_hash(request.form["password"], method='sha256')
        else:
            profile.password =profile.password
        # db.session.add(profile)
        if db.session.commit:            
            db.session.commit()
        return redirect( url_for("index"))
    return render_template('viewProfile.html', profile=profile)

#view function




#view for admin function
@app.route('/viewUsers',methods=['GET', 'POST'])
def viewUsers():
    users = models.user.query.all()
    return render_template('viewUsers.html', users=users)

#add feedback function (user)
@app.route('/addFeedback',methods=['GET', 'POST'])
def addFeedback():
    feedbacks = models.feedback.query.all()
    if request.method == 'POST':
        feedback = models.feedback(user_id=session['user_id'], comment=request.form['comment'], Date=datetime.now())
        db.session.add(feedback)
        db.session.commit()
        return render_template('index.html')
    return render_template('addFeedback.html', feedbacks=feedbacks)

#view feedback function (admin)
@app.route('/viewFeedback',methods=['GET', 'POST'])
def viewFeedback():
    feedbacks = models.feedback.query.all()
    return render_template('viewFeedback.html', feedbacks=feedbacks)

#logout function 
@app.route('/Logout',methods=['GET', 'POST'])
def Logout():
    session.pop('user_id', None)
    session.pop("User_type", None)
    return render_template('index.html')


# delete user 
@app.route('/delete/<int:Id>', methods=['GET', 'POST'])
def delete(Id):
    # user_delete = models.user.query.get_or_404(Id)
    # models.user.query.filter_by(id =Id).delete()
    # db.session.delete(user_delete)
    db.session.query(models.user).filter(models.user.id == Id).delete()
    db.session.commit()
    return redirect(url_for('viewUsers'))

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
            CT = models.CT_scan(image_path=file.filename)
            db.session.add(CT)
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = app.config['UPLOAD_FOLDER'] +'/'+ filename
            preprocessing_and_predict = preprocessing()
            result = preprocessing_and_predict.ReadAll(filepath)

            #result must return 0 ,  1 , 2 , or 3 if return type array or string not work 
            
            return render_template('service.html', result=result)
        
        
    return render_template('service.html')

#for run
if __name__ == '__main__':
    
    #app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
    app.run(debug=True)
with app.app_context():
    db.create_all()
