from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column
# from datetime import datetime
# from sqlalchemy import DateTime
# from main import session




Base = declarative_base() 


# class TimeStampedModel(Model):
#     __abstract__ = True

#     created_at = Column(DateTime, default=datetime.utcnow())
#     updated_at = Column(DateTime, onupdated=datetime.utcnow())