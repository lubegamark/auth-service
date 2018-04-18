"""Users"""
import sqlalchemy as sa

from auth.models import ModelBase


class RoleUser(ModelBase):
    """Role and User intermediate Table
    """
    __tablename__ = 'roles_users'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    role_id = sa.Column(sa.Integer, sa.ForeignKey('roles.id'))


class Role(ModelBase):
    """Roles to handle permissions
    """
    __tablename__ = 'roles'

    id = sa.Column(sa.Integer(), nullable=False, primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))


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
    last_login_at = sa.Column(sa.DateTime())
    current_login_at = sa.Column(sa.DateTime())
    last_login_ip = sa.Column(sa.String(100))
    current_login_ip = sa.Column(sa.String(100))
    login_count = sa.Column(sa.Integer)
    active = sa.Column(sa.Boolean())
    confirmed_at = sa.Column(sa.DateTime())
    roles = sa.orm.relationship(
        'Role',
        secondary='roles_users',
        backref=sa.orm.backref('users', lazy='dynamic')
    )
