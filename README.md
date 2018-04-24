# auth-service

> Service for Authenticating users

## Features
 - Register User
 - Login User (Get jwt token)
 - Validate token

### Requirements
 - python3.6
 - postgres9.6

## How to use

### Stand alone
 - Create a virtual environment
 - Run `pip install -e .`
 - Set up a postgres9.6 database
 - Set environment variables
 - export DATABASE_URI=postgres://username:password@postgres_ip:postgres_port/database_name
 - export SECURITY_PASSWORD_SALT=random-long-string
 - export SECRET_KEY=random-long-string
 - export FLASK_DEBUG=1 #if you need to debug
 - Run `alembic upgrade head`
 - Run application `python app.py`
 - The API documentation is available at the root of the application `/`

### Kubernetes