from sqlalchemy import Column, Integer, String, Float
from .sqllitebase import Base #shared file for Base type, otherwise cannot find table circles

class Line(Base):
    """Represents a Line object"""
    __tablename__ = 'lines'
    id = Column(Integer, primary_key = True)
    start_x = Column(Float)
    start_y = Column(Float)
    end_x = Column(Float)
    end_y = Column(Float)
    points      = Column(Integer, default=0) #count of points that were discovered
    _mean_distance=-1
    
    def __repr__(self) -> str:
        return f"ID: '{self.id}'; Start={self.start_x},{self.start_y}; End={self.end_y},{self.end_y}; count of points={self.points} mean_distance={self.mean_distance}"

    @property
    def mean_distance(self):
        """The mean distance between the points discovered on this line."""
        return self._mean_distance
