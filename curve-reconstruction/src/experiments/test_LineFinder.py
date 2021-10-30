import os
import unittest
import skimage
import skimage.io
import numpy as np
from .RansacLineInfo import RansacLineInfo
from .LineFinder import LineFinder
#import simplegeometry as sg


class Test_LineFinder(unittest.TestCase):
    """docstring for Test_LineFinder."""

    def read_test_image(self,filenameonly:str):
        folder_script=os.path.dirname(__file__)
        imagefilename=os.path.join(folder_script,"test",filenameonly)
        np_image=skimage.io.imread(imagefilename,as_gray=True)
        black_white_threshold=0
        if (np_image.dtype == 'float'):
            black_white_threshold=0.5
        elif (np_image.dtype == 'uint8'):
            black_white_threshold=128
        else:
            raise Exception("Invalid dtype %s " % (np_image.dtype))
        indices=np.where(np_image <= black_white_threshold)
        width=np_image.shape[1]
        height=np_image.shape[0]
        cartesian_y=height-indices[0]-1
        np_data_points=np.column_stack((indices[1],cartesian_y)) 
        return np_data_points, width,height
    
    def test_with_2_large_perpendicular_lines(self):
        all_black_points,width,height=self.read_test_image(filenameonly="simple_image_with_perpendicular_lines.png")

        finder=LineFinder(pixels=all_black_points,width=width,height=height, max_models=3, nnd_threshold_factor=0.5)
        finder.max_ransac_trials=10000
        lines=finder.find()
        self.assertGreaterEqual(len(lines),2)
        desired_lines=list(filter(lambda l: l.ransac_threshold < 2.0,lines))
        self.assertEqual(len(desired_lines),2)
        pass

    def test_when_more_than_1_ransac_line_then_inliers_should_be_shared(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two_simple_lines.png")

        finder=LineFinder(pixels=all_black_points,width=width,height=height, max_models=3, nnd_threshold_factor=0.5)
        finder.max_ransac_trials=500
        lines=finder.find()
        self.assertEqual(len(lines),2)

        actual_count_of_shared_points=1
        self.assertEqual(len(all_black_points),len(lines[0].inliers)+len(lines[1].inliers)-actual_count_of_shared_points)
