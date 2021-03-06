from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile
import random
import string
import json

file_secrets = "secrets.conf"  # generated file with all secrets
file_database = 'activity-tracker.db'


app = Flask(__name__)

# secrets are set during loading
app.secret_key = ''
password_hash_salt = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % file_database

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    data = db.Column(db.Text, nullable=False, default=json.dumps({}))

    def __str__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return 'WIP'


@app.route('/data/<string:username>', methods=['GET', 'POST'])
def get_or_set_data(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, password='')
        db.session.add(user)
        db.session.commit()
    if request.method == 'POST':
        user.data = request.form['data']
        db.session.commit()
        resp = Response('ok')
    else:
        resp = Response(user.data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Initialization part of the script, together with first set-up
if not isfile(file_secrets):
    print('Now, generating your secrets...')
    password_hash_salt = ''.join(random.SystemRandom().choice(string.printable) for _ in range(64))
    app.secret_key = ''.join(random.SystemRandom().choice(string.printable) for _ in range(64))
    data_dict = {'password_hash_salt': password_hash_salt, 'app_secret': app.secret_key}
    with open(file_secrets, 'wt') as f:
        json.dump(data_dict, f, indent=1)
else:
    with open(file_secrets, 'rt') as f:
        data_dict = json.load(f)
        password_hash_salt = data_dict['password_hash_salt']
        app.secret_key = data_dict['app_secret']

db.create_all()

print("That's all, your're clear for launch")
