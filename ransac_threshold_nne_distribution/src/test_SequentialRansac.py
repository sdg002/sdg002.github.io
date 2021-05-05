import unittest
from SequentialRansac import SequentialRansac
import os
import skimage.io
from RansacLineInfo import  RansacLineInfo
from typing import List

class Test_SequentialRansac(unittest.TestCase):

    def test_constructor(self):
        folder_script=os.path.dirname(__file__)
        test_image_file=os.path.join(folder_script,"test","simple_image_with_perpendicular_lines.png")

        seq=SequentialRansac(path=test_image_file,max_lines_to_find=2,ransac_threshold_factor=0.25)
        image=seq.image_array
        self.assertEqual(image.shape[1],200)
        self.assertEqual(image.shape[0],100)

        self.assertEqual(seq.width,200)
        self.assertEqual(seq.height,100)
        pass

    def test_image_with_two_perpendicular_lines(self):
        folder_script=os.path.dirname(__file__)
        test_image_file=os.path.join(folder_script,"test","simple_image_with_perpendicular_lines.png")

        seq=SequentialRansac(path=test_image_file,max_lines_to_find=2,ransac_threshold_factor=0.25)
        resulting_lines:List[RansacLineInfo]=seq.run_sequential_ransac()
        self.assertEqual(len(resulting_lines),2)

        horizontal_line:RansacLineInfo=None
        vertical_line:RansacLineInfo=None
        if (resulting_lines[0].unitvector.X == 0):
            vertical_line=resulting_lines[0]
            horizontal_line=resulting_lines[1]
        else:
            vertical_line=resulting_lines[1]
            horizontal_line=resulting_lines[0]

        all_x_vertical_line=list(map(lambda p: p.X, vertical_line.inliers))
        all_y_vertical_line=list(map(lambda p: p.Y, vertical_line.inliers))

        all_x_horizontal_line=list(map(lambda p: p.X, horizontal_line.inliers))
        all_y_horizontal_line=list(map(lambda p: p.Y, horizontal_line.inliers))


        self.assertEqual(max(all_x_vertical_line),100,"All inliers along the vertical line should have a constant value of X=100")
        self.assertLessEqual(max(all_y_vertical_line),100,"The max of the inliers along the vertical line should have a max Y of 100")
        self.assertLessEqual(min(all_y_vertical_line),1,"The min of the inliers along the vertical line should have a max Y of 1")

        self.assertEqual(max(all_y_horizontal_line),51,"All inliers along the horizontal  line should have a constant value of Y=51")
        self.assertLessEqual(max(all_x_horizontal_line),200,"The max of the inliers along the horizontal line should have a max X of 200")
        self.assertLessEqual(min(all_x_horizontal_line),1,"The min of the inliers along the horizontal line should have a max X of 1")
        
        pass

if __name__ == '__main__':
    unittest.main()
