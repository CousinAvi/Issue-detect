from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from sqlalchemy import exc
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..config import db_url
from sqlalchemy.orm import Session
from typing import Generator

print(db_url)

engine = create_engine(db_url, pool_size=30)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info["pid"] = os.getpid()


@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info["pid"] != pid:
        connection_record.dbapi_connection = connection_proxy.dbapi_connection = None
        raise exc.DisconnectionError(
            "Connection record belongs to pid %s, "
            "attempting to check out in pid %s" % (connection_record.info["pid"], pid)
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
