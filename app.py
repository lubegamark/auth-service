import datetime
import json
import os
import uuid

import jwt
from flasgger import Swagger
from flask import Flask, request
from flask.json import jsonify
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password
from flask_sqlalchemy import SQLAlchemy
from voluptuous import (
    MultipleInvalid,
    Required,
    Schema, Optional)

from auth.models import users, db_session
from auth.models.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")

db = SQLAlchemy(app)
db.session = db_session

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}

swagger = Swagger(app, config=swagger_config)


user_datastore = SQLAlchemyUserDatastore(
    db,
    users.User,
    users.Role)
security = Security(app, user_datastore)


@app.route('/status')
def status():
    payload = {"status": "running"}
    return json.dumps(payload)


@app.route('/register', methods=['POST'])
def register():
    """Create New User
    Register User in the system
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
              id: User
              required:
                - username
                - password
                - name
                - phoneNumber
              properties:
                name:
                  type: string
                  description: Name of user
                  default: John Doe
                username:
                  type: string
                  description: Username of user
                  default: john
                password:
                  type: string
                  description: User's Password
                  default: "********"
                phoneNumber:
                  type: string
                  description: User's Password
                  default: "+256789456123"
                email:
                  type: string
                  description: Users Email address
                  default: john@doe.me
    definitions:
      User:
        type: object
        properties:
          name:
            type: string
          username:
            type: string
          email:
            type: string
          phoneNumber:
            type: string
    responses:
      200:
        description: An instance of created user
        schema:
          id: Users
          type: object
          $ref: '#/definitions/User'
        examples:
          {"id": 1, "username": "john", "phoneNumber": "+256789456123"}
    """

    request_data = request.get_json()
    registration_schema = Schema({
        Required("name"): str,
        Required("username"): str,
        Required("password"): str,
        Required("phoneNumber"): str,
        Optional("email"): str,
    })

    try:
        validated = registration_schema(request_data)
        validated["phone_number"] = validated.pop("phoneNumber")
        validated["password"] = hash_password(validated["password"])
        validated["uuid"] = uuid.uuid4()

        new_user = security.datastore.create_user(**validated)
        print(type(new_user))
        db.session.commit()
    except MultipleInvalid as error:
        print(error)
        raise APIError("Validation Error", 400)
    except Exception as error:
        print(error)
        raise APIError("Unknown Error occurred", 500)
    return json.dumps(new_user.to_json())


@app.route('/token', methods=['POST'])
def login():
    """Login
    Get JWT Token
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
              id: User
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  description: Username of user
                  default: john
                password:
                  type: string
                  description: User's Password
                  default: "********"
    responses:
      200:
        description: An instance of created user
        schema:
          id: Users
          type: object
        examples:
          {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MjQ4MTM2NTksImlhdCI6MTUyNDgxMzM1OSwic3ViIjoiZGU2NTM0YWQtNWM0OC00NGEyLWJhYzktM2Q3OTkwMmVjODE2In0.4SQsr4I_R9mxdl-EgcggnPU8Ls_SR2zjdug-_mfhtKc"}

    """
    request_data = request.get_json()
    login_schema = Schema({
        Required("username"): str,
        Required("password"): str,
    })

    try:
        validated = login_schema(request_data)
        user = User.query.filter(User.username == validated["username"]).one()
        if user and verify_password(validated["password"], user.password):
            return encode_auth_token(user)
        else:
            raise APIError("Failed to Authenticate", 403)

    except MultipleInvalid as error:
        print(error)
        raise APIError("Validation Error", 400)
    except Exception as error:
        print(error)
        raise APIError("Unknown Error occurred", 500)


@app.route('/validate', methods=['POST'])
def validate_token():
    """Validate
    Check if JWT Token is valid
    ---
    parameters:
      - name: Authorization
        in: header
        schema:
          type: string
          required: true
    responses:
      200:
        description: user id
        schema:
          id: Users
          type: object
        examples:
          {"user": "de6534ad-5c48-44a2-bac9-3d79902ec816"}

    """
    bearer = request.headers["Authorization"]
    token = bearer.split(" ")[1]
    j = decode_auth_token(token)
    print(j)
    return jsonify({"user": j})


@app.route('/users', methods=['GET'])
def get_users():
    """Get Users
    Get All Users
    ---
    responses:
      200:
        description: List of all users in the system
        schema:
          id: Users
          type: object
        examples:
            [
              {
                "email": null,
                "name": "John Doe",
                "username": "john",
                "uuid": "de6534ad-5c48-44a2-bac9-3d79902ec816"
              },
              {
                "email": "lurark@gmail.com",
                "name": "Lu Rark",
                "username": "lu",
                "uuid": "d99b8842-4b2a-4af6-920a-8f190db006c8"
              },
              {
                "email": "aiba@gmail.com",
                "name": "Sela Aiba",
                "username": "aiba",
                "uuid": "7a5a317f-0aff-4710-b312-850a65f2e3f6"
              },
            ]


    """
    users = User.query.all()
    users_json = [u.to_json() for u in users]
    print(users_json)
    return jsonify(users_json)


def encode_auth_token(user):
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
            'sub': user.uuid
        }
        token = jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return json.dumps({"token": token.decode('utf-8')})
    except Exception as e:
        print(e)
        raise APIError("Unknown Error occurred", 500)


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
        raise APIError('Signature expired. Please log in again.', 401)
    except jwt.InvalidTokenError:
        raise APIError('Invalid token. Please log in again.', 401)


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(400)
def bad_request(e):
    response = jsonify({"message": "Bad Request"})
    response.status_code = 400
    return response


@app.errorhandler(401)
def unauthorized(e):
    response = jsonify({"message": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(e):
    response = jsonify({"message": "Forbidden"})
    response.status_code = 403
    return response


@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({"message": "Not Found"})
    response.status_code = 404
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({"message": "Unknown Error"})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
