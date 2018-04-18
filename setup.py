from setuptools import setup

setup(
    name='gmoney-auth-service',
    packages=['auth'],
    include_package_data=True,
    install_requires=[
        'alembic==0.9.9',
        'Flask==0.12.2',
        'Flask-Security==3.0.0',
        'psycopg2==2.7.4',
        'SQLAlchemy==1.2.6',
        'voluptuous==0.11.1'])
