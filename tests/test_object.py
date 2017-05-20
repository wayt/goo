from sqlalchemy import Column, String, Integer, DateTime
from goo.base import Base
from goo.time import utcnow

class TestObject(Base):
    __tablename__ = 'test_object'

    name = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    counter = Column(Integer, nullable=True, default='1')
