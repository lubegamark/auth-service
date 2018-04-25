import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker

db_provider = os.environ.get("DATABASE_PROVIDER")
db_user = os.environ.get("DATABASE_USER")
db_password = os.environ.get("DATABASE_PASSWORD")
db_host = os.environ.get("DATABASE_HOST")
db_port = os.environ.get("DATABASE_PORT")
db_name = os.environ.get("DATABASE_NAME")

database_uri = "{provider}://{user}:{password}@{host}:{port}/{db}".format(
    provider=db_provider,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    db=db_name
)

engine = create_engine(database_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

DeclarativeBase = declarative_base()
DeclarativeBase.query = db_session.query_property()


class Serializer(object):

    def serialize(self, fields):
        if fields:
            return {c: getattr(self, c) for c in fields}
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class BaseModel(DeclarativeBase, Serializer):
    __abstract__ = True

    def to_json(self):
        return self.serialize(self.FIELDS)
