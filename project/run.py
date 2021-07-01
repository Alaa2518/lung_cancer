from flask import Flask ,render_template ,request
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
app = Flask('__name__')

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


css_admin = Bundle('css/all.min.css', 'css/bootstrap.min.css', 'css/fontawesome.min.css', output='gen/packed.css')
js = Bundle('js/Jquery.js', 'js/bootstrap.min.js', 'js/fontawesome.min.js','js/all.min.js', output='gen/packed.js')
assets = Environment(app)
assets.register('css_admin', css_admin)
assets.register('js_all', js)

@app.route('/')
def hello():
    return 'hello flask'

@app.route('/index',methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/user/<int:id>')
def hellouser(id):
    return 'hello flask'+ str(id)



if __name__ == '__main__':
    app.run(port=app.config['PORT'],debug=app.config['DEBUG'])
    



