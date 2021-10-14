from genericpath import isfile
import unittest
from entity import *
import os, sys
import math

class Test_Circle(unittest.TestCase):
    
    def init_sqlitefile(self):
        self._absolute_path_db=None
        dbfilename="unittest.entity.db"
        fullpathtoscript=os.path.realpath(__file__)
        folder_script=os.path.dirname(fullpathtoscript)
        self._absolute_path_db=os.path.join(folder_script,"out/",dbfilename)
        if (os.path.isfile(self._absolute_path_db)):
            os.remove(self._absolute_path_db)

    def test_create_line(self):
        self.init_sqlitefile()
        dbwrapper=SqliteWrapper(filename=self._absolute_path_db)
        dbwrapper.delete_all_objects()
        expected_line1=Line(id=1, start_x=1.1, start_y=1.2, end_x=10.1, end_y=10.2, points=101)
        expected_line2=Line(id=2, start_x=2.1, start_y=3.2, end_x=20.1, end_y=30.1, points=201)
        dbwrapper.add_lines([expected_line1,expected_line2])
        persisted_lines=dbwrapper.get_all_lines()

        self.assertEqual(persisted_lines[0].id,expected_line1.id)
        self.assertEqual(persisted_lines[1].id,expected_line2.id)
        self.assertAlmostEquals(persisted_lines[0].start_x,expected_line1.start_x,delta=0.01)
        self.assertAlmostEquals(persisted_lines[0].start_y,expected_line1.start_y,delta=0.01)

        self.assertAlmostEquals(persisted_lines[1].end_x,expected_line2.end_x,delta=0.01)
        self.assertAlmostEquals(persisted_lines[1].end_y,expected_line2.end_y,delta=0.01)
        pass

    def test_mean_separation(self):
        line=Line(id=1, start_x=1.0, start_y=1.0, end_x=2.0, end_y=2.0, points=101)
        actual_angular_distance=line.mean_distance
        actual_length=math.sqrt((line.start_x-line.end_x)**2 +(line.start_y-line.end_y)**2)
        expected_mean_distance=actual_length/line.points
        self.assertAlmostEquals(line.mean_distance,expected_mean_distance,1)
