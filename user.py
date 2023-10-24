from models.base import Base as TimeStampedModel
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey

class User (TimeStampedModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firt_name = Column(String(88), nullable=False)
    last_name = Column(String(88), nullable=False)
    email = Column(String(320), nullable=False, unique=True)

    preference = relationship("Preference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="users")



    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.firt_name} {self.last_name}"


class Preference(TimeStampedModel):
    __tablename__ ="preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(80), nullable=False)
    currency = Column(String(3), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = relationship("User", back_populates="preference")

class Address(TimeStampedModel):
    __tablename__ = "addresses"
    road_name = Column(String(88), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    read_name = Column(String(88), nullable=False)
    postcode = Column(String(88), nullable=False)
    city = Column(String(88), nullable=False)
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)

    user = relationship("User", back_populates="addresses", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="addresses")


    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.city}"
    
class Role(TimeStampedModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(88), nullable=False)
    slug = Column(String(88), nullable=False, unique=True)

    users = relationship("User", secondary="user_roles",  back_populates="roles")


    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.name}"
    

class UserRole(TimeStampedModel):
    __tablename__ = "user_roles"

    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


    