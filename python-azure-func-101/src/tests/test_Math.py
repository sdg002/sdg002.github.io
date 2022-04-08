import unittest
#import shared_code.Math
from shared_code import Math

class MathTests(unittest.TestCase):
    """Tests for MathTests."""
    def test_add_method(self):
        m=Math()
        result=m.add(100.1,0.2)
        self.assertEqual(100.3, result, 'The Add method should sump up')
        pass

    def test_add_method1(self):
        pass
    