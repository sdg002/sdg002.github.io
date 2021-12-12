
from typing import List
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from .Circle import Circle
from .Line import Line
from .sqllitebase import Base  #common file for Base type, otherwise cannot find circles table

class SqliteWrapper(object):
    """Manages the creation of a Sqlite database and adding/deleting records."""
    def __init__(self, filename:str):
        super(SqliteWrapper, self).__init__()
        self.__filename=filename
        self.__engine=None
        self.__initialize()

    def __initialize(self):
        #create the connection here
        cnstring=f"sqlite:///{self.__filename}"
        self.__engine = db.create_engine(cnstring, echo=True)  
        Base.metadata.create_all(self.__engine)

    def add_circles(self,circles:List[Circle]):
        Session = sessionmaker(bind = self.__engine)
        session = Session()
        for circle in circles:
            session.add(circle)
        session.commit()

    def add_lines(self,lines:List[Line]):
        Session = sessionmaker(bind = self.__engine)
        session = Session()
        for line in lines:
            session.add(line)
        session.commit()

    def delete_all_circles(self):
        sql = 'DELETE FROM circles'
        connection = self.__engine.connect()
        r_set=connection.execute(sql)
        print(f"No of circles deleted {r_set.rowcount}")
        pass

    def delete_all_lines(self):
        sql = 'DELETE FROM lines'
        connection = self.__engine.connect()
        r_set=connection.execute(sql)
        print(f"No of circles deleted {r_set.rowcount}")
        pass

    def delete_all_objects(self):
        self.delete_all_circles()
        self.delete_all_lines()

    def get_all_circles(self)->List[Circle]:
        Session = sessionmaker(bind = self.__engine)
        session = Session()
        result = session.query(Circle).all()
        circles=[]
        for row in result:
            circles.append(row)
        return circles

    def get_all_lines(self)->List[Circle]:
        Session = sessionmaker(bind = self.__engine)
        session = Session()
        result = session.query(Line).all()
        lines=[]
        for row in result:
            lines.append(row)
        return lines