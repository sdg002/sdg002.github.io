#
#Placeholder Python file to test Sqlite operations
#
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from entity import *

import os
from datetime import datetime



def read_database(dbwrapper:SqliteWrapper):
    print("Fetching circles")
    circles=dbwrapper.get_all_circles()
    for c in circles:
        print(f"\t{c}")
    lines=dbwrapper.get_all_lines()
    for line in lines:
        print(f"\t{line}")


if (__name__ =="__main__"):
    print("Inside main")
    dbfilename="demo.entity.db"
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path_db=os.path.join(folder_script,"out/",dbfilename)

    dbwrapper=SqliteWrapper(filename=absolute_path_db)
    dbwrapper.delete_all_objects()
    print(f"Deleted all objects complete")
    now=datetime.now()
    c1=Circle(x=1.1,y=1.2, radius=1.3, id=now.second+1)  #the id has to be specified
    c2=Circle(x=2.1,y=2.2, radius=2.3, id=now.second+2, arc_start=1.5, arc_end=2.5)
    dbwrapper.add_circles([c1,c2])

    l1=Line(id=1, start_x=1.1, start_y=1.2, end_x=10.1, end_y=10.2, points=1234)
    l2=Line(id=2, start_x=2.1, start_y=2.2, end_x=20.1, end_y=20.2, points=1234)
    dbwrapper.add_lines([l1,l2])
    read_database(dbwrapper)
    print(f"Reading all objects complete")
