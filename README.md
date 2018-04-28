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

#### Minikube Development
 - Switch to the docker inside minikiube `eval $(minikube docker-env)`
 - Build the docker image inside your minikube `docker build -t gmoney-auth-image:v0 .`
 - Add the following secrets
   - flask.password_salt (random string preferrably 128bytes or more)
   - flask.secret_key (random string preferrably 128bytes or more)
   - db-variables.database (database name)
   - db-variables.user_username (database user)
   - db-variables.user_password (database user password)
   - db.db_uri (full database uri in the form `postgres://user_username:user_password@database_host/database_name`)
 - The variables in db.db_uri must match those used in db_variables
 - Assuming you have a file for each variable e.g secret_key containing the secret key, run the following to add those secrets
 ```
 kubectl create secret generic flask --from-file=secret_key --from-file=password_salt
 kubectl create secret generic db-variables --from-file=database --from-file=user_password --from-file=user_username
 kubectl create secret generic db --from-file=db_uri --from-file=db_uri
 ```
 - Apply the service `kubectl apply -f auth-service.yml`
 - Get the pod for auth deployment from `kubectl get pods`
 - Login to the deployment `kubectl exec -it auth-deployment-actual-pod -- "/bin/bash"` Replace `auth-deployment-actual-pod` with actual deployment name
 - Run alembic migrations `alembic upgrade head`
 - Access the serivce from the IP and Port given to the auth service
