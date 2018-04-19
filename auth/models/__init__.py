import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker

database_uri = os.environ.get("DATABASE_URI")

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
