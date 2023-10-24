import os 
from sqlalchemy import create_engine, event, engine 
from sqlalchemy.orm import scoped_session, sessionmaker    
from models.base import Base as TimeStampedModel
from models.user import User    
                             


BASE_DIR  = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f"sqlite:///{BASE_DIR}/db", echo=True)

# session = scoped_session (
#     sessionmaker(
#         autoflush=False,
#         autocommit=False,
#         bind=engine
#     )
# )

# @event.listens_for(engine, 'connect')
# def seet_sqlite_pragma(dpapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys= ON")
#     cursor.close()


TimeStampedModel.metadata.create_all(engine)