#
#Placeholder Python file to test Sqlite operations
#
from entity.SqliteWrapper import SqliteWrapper
from entity.Circle import Circle
import os
from datetime import datetime

if (__name__ =="__main__"):
    print("Inside main")
    dbfilename="demo.entity.db"
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path_db=os.path.join(folder_script,"out/",dbfilename)

    dbwrapper=SqliteWrapper(filename=absolute_path_db)
    dbwrapper.delete_all_objects()
    now=datetime.now()
    c1=Circle(x=1.1,y=1.2, radius=1.3, id=now.second+1)  #the id has to be specified
    c2=Circle(x=2.1,y=2.2, radius=2.3, id=now.second+2)
    dbwrapper.add_circles([c1,c2])
