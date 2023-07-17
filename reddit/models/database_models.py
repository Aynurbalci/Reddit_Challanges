from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text
Base = declarative_base()
class Post(Base):
    __tablename__ = 'post'

    id = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    score = Column(Integer)
    comment_count = Column(Integer)
    timestamp = Column(DateTime)
    url = Column(String)
    content = Column(Text)
