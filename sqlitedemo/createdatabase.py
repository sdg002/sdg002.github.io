import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import inspect

Base = declarative_base()

#
#Customers ORM class
#
class Customers(Base):
   __tablename__ = 'customers'
   
   id = Column(Integer, primary_key = True)
   name = Column(String)
   address = Column(String)
   email = Column(String)
   def __repr__(self) -> str:
        return f"Name: '{self.name}'; Address: '{self.address}'; Email: '{self.email}'"

def add_customer(session):
    now=datetime.now()
    c1=Customers(name=f"john {now.microsecond}", address="blah address", email=f"john-{now.microsecond}@cool.com")
    session.add(c1)
    session.commit()
    print(f"Added new customer with the name {c1.name}")
    return c1
    pass

def add_multiple_customers(session):
    count=7
    now=datetime.now()
    for index in range(0,count):
        c1=Customers(name=f"john {now.second+index}", address="blah address", email=f"john-{now.second+index}@cool.com")
        print(f"Added new customer with the name {c1.name}")
        session.add(c1)
    session.commit()
    pass

def query_all_customers(session):
 
    result = session.query(Customers).all()
    for row in result:
        print(row)

def delete_all_customers(connection):
    sql = 'DELETE FROM customers'
    r_set=connection.execute(sql)
    print(f"No of Records deleted {r_set.rowcount}")


def main():
    print("Create a simple SQLite database file")
    engine = db.create_engine('sqlite:///mysqlite.db', echo=True)
    print("SQLite database file created")
    connection = engine.connect()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    delete_all_customers(connection=connection)
    add_multiple_customers(session)
    #c=add_customer(session)
    #print(inspect.getmembers(c)) #how to get all members
    #print(inspect.getmembers, inspect.isfunction) #when you want all function members
    query_all_customers(session)

if (__name__ =="__main__"):
    main()

