from flask import Flask, request
import json
from voluptuous import (
    MultipleInvalid,
    Required,
    Schema)


app = Flask(__name__)

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

    print(request_data)
    try:
        validated = registration_schema(request_data)
    except MultipleInvalid as error:
        print(error)
    return "OK"


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
