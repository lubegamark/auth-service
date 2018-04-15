"""Users"""
import sqlalchemy as sa

from auth.models import ModelBase


class User(ModelBase):
    """Users of the system
    """

    __tablename__ = 'users'

    id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    username = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=True)
    phone_number = sa.Column(sa.String, nullable=False)
    
