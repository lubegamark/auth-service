from setuptools import setup

setup(
    name='gmoney-auth-service',
    packages=['auth'],
    include_package_data=True,
    install_requires=[
        'alembic==0.9.9',
        'bcrypt==3.1.4',
        'flake8==3.5.0',
        'Flask==0.12.2',
        'Flask-Security==3.0.0',
        'Flask-SQLAlchemy==2.3.2',
        'PyJWT==1.6.1',
        'psycopg2==2.7.4',
        'SQLAlchemy==1.2.6',
        'voluptuous==0.11.1'])
