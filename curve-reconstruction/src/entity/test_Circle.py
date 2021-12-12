from genericpath import isfile
import unittest
from entity import *
import os, sys


class Test_Circle(unittest.TestCase):
    
    def init_sqlitefile(self):
        self._absolute_path_db=None
        dbfilename="unittest.entity.db"
        fullpathtoscript=os.path.realpath(__file__)
        folder_script=os.path.dirname(fullpathtoscript)
        self._absolute_path_db=os.path.join(folder_script,"out/",dbfilename)
        if (os.path.isfile(self._absolute_path_db)):
            os.remove(self._absolute_path_db)

    def test_create_circle(self):
        self.init_sqlitefile()
        dbwrapper=SqliteWrapper(filename=self._absolute_path_db)
        dbwrapper.delete_all_objects()
        expected_c1=Circle(x=1.1,y=1.2, radius=1.3, id=1,arc_start=1.5, arc_end=2.5)
        expected_c2=Circle(x=2.1,y=2.2, radius=2.3, id=2, arc_start=2.5, arc_end=3.5)
        dbwrapper.add_circles([expected_c1,expected_c2])
        persisted_circles=dbwrapper.get_all_circles()

        self.assertEqual(persisted_circles[0].id,expected_c1.id)
        self.assertEqual(persisted_circles[1].id,expected_c2.id)
        self.assertAlmostEquals(persisted_circles[0].arc_start,expected_c1.arc_start,1)
        self.assertAlmostEquals(persisted_circles[0].arc_end,expected_c1.arc_end,1)

        self.assertAlmostEquals(persisted_circles[1].arc_start,expected_c2.arc_start,1)
        self.assertAlmostEquals(persisted_circles[1].arc_end,expected_c2.arc_end,1)
        pass

    def test_mean_angular_separation(self):
        circle=Circle(x=1.1,y=1.2, radius=1.3, id=1,arc_start=1.5, arc_end=2.5, points=12)
        actual_angular_distance=circle.mean_angular_distance
        expected_angular_distance=(2.5-1.5)/circle.points
        self.assertAlmostEquals(actual_angular_distance,expected_angular_distance,1)
