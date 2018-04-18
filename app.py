import json
import os

from flask import Flask, request
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from voluptuous import (
    MultipleInvalid,
    Required,
    Schema)

from auth.models import users, db_session

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

@app.route('/register', methods=['GET', 'POST'])
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
        db.session.commit()
    except MultipleInvalid as error:
        print(error)
        return "Validation Error", 400
    except Exception as error:
        print(error)
        return "Unknown Error occurred", 500
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
