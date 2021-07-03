import os
# basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
PORT= 5000
SECRET_KEY = os.urandom(32)
UPLOAD_FOLDER = 'static/img/upload'
QLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:1521:5000/lung_cancer'
UPLOAD_FOLDER = UPLOAD_FOLDER
# QLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'mysql+pymysql: //'+ os.path.join(basedir,'lung_cancer')
SQLALCHEMY_TRACK_MODIFICATIONS =False
