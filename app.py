import datetime
import json
import os

import jwt
from flask import Flask, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password
from flask_sqlalchemy import SQLAlchemy
from voluptuous import (
    MultipleInvalid,
    Required,
    Schema)

from auth.models import users, db_session
from auth.models.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

db = SQLAlchemy(app)
db.session = db_session


user_datastore = SQLAlchemyUserDatastore(
    db,
    users.User,
    users.Role)
security = Security(app, user_datastore)


@app.route('/')
def index():
    return 'Ok'


@app.route('/status')
def status():
    payload = {"status": "running"}
    return json.dumps(payload)


@app.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    registration_schema = Schema({
        Required("name"): str,
        Required("username"): str,
        Required("password"): str,
        Required("phoneNumber"): str,
    })

    try:
        validated = registration_schema(request_data)
        validated["phone_number"] = validated.pop("phoneNumber")
        validated["password"] = hash_password(validated["password"])

        new_user = security.datastore.create_user(**validated)
        print(type(new_user))
        db.session.commit()
    except MultipleInvalid as error:
        print(error)
        return "Validation Error", 400
    except Exception as error:
        print(error)
        return "Unknown Error occurred", 500
    return json.dumps(new_user.to_json())


@app.route('/token', methods=['POST'])
def login():
    request_data = request.get_json()
    login_schema = Schema({
        Required("username"): str,
        Required("password"): str,
    })

    try:
        validated = login_schema(request_data)
        user = User.query.filter(User.username == validated["username"]).one()
        if user and verify_password(validated["password"], user.password):
            return encode_auth_token(user.id)
        else:
            return "Failed to Authenticate", 403

    except MultipleInvalid as error:
        print(error)
        return "Validation Error", 400
    except Exception as error:
        print(error)
        return "Unknown Error occurred", 500


@app.route('/validate', methods=['POST'])
def validate_token():
    bearer = request.headers["Authorization"]
    token = bearer.split(" ")[1]
    return decode_auth_token(token)


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                days=0,
                seconds=300),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return json.dumps({"token": token.decode('utf-8')})
    except Exception as e:
        print(e)
        return "Unknown Error occurred", 500


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        print(payload)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.', 401
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.', 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
