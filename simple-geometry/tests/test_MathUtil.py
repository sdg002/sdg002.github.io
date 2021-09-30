from src.MathUtil import MathUtil
import unittest
import math


class Test_test_MathUtil(unittest.TestCase):
    def test_atan2_0to2pi(self):
        yx_values=[(+1,+1,45.0),(+1,-1,135.0),(-1,-1,225.0),(-1,+1,315.0)]
        for yx_value in yx_values:
            expected_value=yx_value[2]
            actual_value=MathUtil.atan2_0to2pi(yx_value[0], yx_value[1]) * 180/math.pi
            self.assertAlmostEqual(expected_value,actual_value,1)
        pass