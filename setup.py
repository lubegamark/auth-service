import os

from setuptools import setup


NAME = 'gmoney-auth-service'
DESCRIPTION = 'Gmoney Auth Service'
URL = 'https://gitlab.com/g-money/authService'
EMAIL = 'lubegamark@gmail.com'
AUTHOR = 'Lubega Mark'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

here = os.path.abspath(os.path.dirname(__file__))

about = {}
if not VERSION:
    with open(os.path.join(here, "auth", '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['auth'],
    include_package_data=True,
    install_requires=[
        'alembic==0.9.9',
        'bcrypt==3.1.4',
        'flake8==3.5.0',
        'flasgger==0.8.1',
        'Flask==0.12.2',
        'Flask-Cors==3.0.4',
        'Flask-Security==3.0.0',
        'Flask-SQLAlchemy==2.3.2',
        'PyJWT==1.6.1',
        'psycopg2-binary==2.7.4',
        'SQLAlchemy==1.2.6',
        'voluptuous==0.11.1'])
