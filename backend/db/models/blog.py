from datetime import datetime, date
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, Date
from sqlalchemy.orm import relationship

from db.base_class import Base



class Blog(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    created_at = Column(Date, default=date.today())
    is_active = Column(Boolean, default=True)