from flask import Flask, request
import os
import json
import psycopg2
import jwt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from schema import create_schema


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://globals:globals@localhost/globals'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
CORS(app, resource={fr"*": {"origins": "*"}})
HOME_DIR = os.getcwd()
My_SECRET_STRING = "AccuracySecretKey"
db = SQLAlchemy(app)

user = "globals"
password = "globals"
host = "localhost"
port = 5432
database = "globals"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    schemaname = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, username, password, schemaname):
        self.username = username
        self.password = password
        self.schemaname = schemaname


@app.route('/', methods=["GET"])
def index():
    return "<h1><center>Register User</center></h1>"


@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = json.loads(request.data)["username"]
    if not os.path.exists(fr'{HOME_DIR}/{username}'):
        os.makedirs(fr'{HOME_DIR}/{username}')
        os.makedirs(fr'{HOME_DIR}/{username}/data_input')
        os.makedirs(fr'{HOME_DIR}/{username}/data output')
    return "OK"


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST" and json.loads(request.data)["password"] and json.loads(request.data)["username"]:
        username = json.loads(request.data)["username"]
        password = json.loads(request.data)["password"]
        exist = Users.query.filter_by(username=username).first()
        if exist and exist.password == password:
            payload = {'user_id': {"id": exist.id, "username": exist.username}}
            token = jwt.encode(payload=payload, key=My_SECRET_STRING)
            return {'success': True,
                    'message': 'User created and schema is generated',
                    'token': token,
                    'isUserLoggedId': 1,
                    'username': username,
                    'schema': exist.schemaname}
        else:
            return {'success': False,
                    'message': 'Please check your username and password.'}
    else:
        return {'success': False,
                'message': 'This method accept POST'}


@app.route('/register', methods=['POST'])
def registration():
    if request.method == "POST" and json.loads(request.data)["username"] and json.loads(request.data)["password"]\
            and json.loads(request.data)["schemaname"]:
        username = json.loads(request.data)["username"]
        password = json.loads(request.data)["password"]
        schemaname = json.loads(request.data)["schemaname"]

        conn = psycopg2.connect(
            database=database, user=user, password=password, host=host, port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", [username])
        if cursor is not None:
            record = Users(username, password, schemaname)
            db.session.add(record)
            db.session.commit()
            create_schema(schemaname)
            return {'success': True,
                    'message': 'User created and schema is generated'}
        else:
            return {'success': False,
                    'message': 'User already exist'}
    else:
        return {'success': False,
                'message': 'this method accept GET'}


if __name__ == '__main__':
    # app.run(host='192.168.1.34')
    db.create_all()
    app.run()
