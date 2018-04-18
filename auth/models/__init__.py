import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

database_uri = os.environ.get("DATABASE_URI")

engine = create_engine(database_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

ModelBase = declarative_base()
ModelBase.query = db_session.query_property()


