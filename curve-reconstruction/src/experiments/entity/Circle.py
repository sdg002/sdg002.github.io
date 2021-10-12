
from sqlalchemy import Column, Integer, String, Float

from .sqllitebase import Base #shared file for Base type, otherwise cannot find table circles

class Circle(Base):
    """Represents a Circle object"""
    __tablename__ = 'circles'
    id = Column(Integer, primary_key = True)
    radius = Column(Float)
    x = Column(Float)
    y = Column(Float)
    arc_start   = Column(Float)
    arc_end     = Column(Float)
    
    def __repr__(self) -> str:
        return f"ID: '{self.id}'; Radius: '{self.radius}'; X: '{self.x}'; Y: '{self.y}'; arc_start={self.arc_start}; arc_end={self.arc_end}"

