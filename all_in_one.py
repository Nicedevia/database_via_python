import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import streamlit as st 
import streamlit as st 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f"sqlite:///{BASE_DIR}/db.sqlite", echo=True)

session = scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )
)

@event.listens_for(engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Model = declarative_base()

class TimeStampedModel(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class User(TimeStampedModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(88), nullable=False)
    last_name = Column(String(88), nullable=False)
    email = Column(String(320), nullable=False, unique=True)

    preference = relationship("Preference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.first_name} {self.last_name}"


class Preference(TimeStampedModel):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(80), nullable=False)
    currency = Column(String(3), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = relationship("User", back_populates="preference")

class Address(TimeStampedModel):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    road_name = Column(String(88), nullable=False)
    postcode = Column(String(88), nullable=False)
    city = Column(String(88), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = relationship("User", back_populates="addresses", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="addresses")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.city}"

class Role(Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(88), nullable=False)
    slug = Column(String(88), nullable=False, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.name}"

class UserRole(TimeStampedModel):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

databasefinish = Model.metadata.create_all(engine)

st.title("database") 
st.table(databasefinish)
