from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  

    author = relationship('User', back_populates='blogs')  
