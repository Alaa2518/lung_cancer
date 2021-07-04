from run import db   
class user(db.Model):
    #coulmns
    id = db.Column(db.Integer, primary_key= True,autoincrement=True)
    username = db.Column('username',db.String(50),nullable=False)
    first_name = db.Column('First_name',db.String(50),nullable=False)
    last_name = db.Column('Last_name',db.String(50),nullable=False)
    email = db.Column('email',db.String(100),nullable=False)
    password = db.Column('Password',db.String(100),nullable=False)
    User_type = db.Column('user_type',db.Integer,nullable=False)

class feedback(db.Model): 
    #coulmns
    id = db.Column(db.Integer, primary_key= True,autoincrement=True)
    user_id= db.Column(db.Integer,primary_key=False,nullable=False)
    comment = db.Column('Comment',db.String(150),nullable=True)
    Date  = db.Column('Date',db.DateTime,nullable=False)

class CT_scan(db.Model): 
    #coulmns
    id = db.Column(db.Integer, primary_key= True,autoincrement=True)
    image_path = db.Column('image_path', db.String(150), nullable=False)
