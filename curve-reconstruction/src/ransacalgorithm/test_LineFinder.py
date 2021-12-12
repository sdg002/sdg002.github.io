import os
import unittest
import skimage
import skimage.io
import numpy as np

from ransacalgorithm.StoppingCriteria import StoppingCriteria
from .RansacLineInfo import RansacLineInfo
from .RansacLineFinder import RansacLineFinder
import simplegeometry as sg


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

    def assertCommonInliers(self,line1:RansacLineInfo,line2:RansacLineInfo):
        common_inliers=self.find_common_inliers(line1=line1,line2=line2)
        self.assertGreater(len(common_inliers),0,"There must be some common inliers")
        pass

    def find_common_inliers(self,line1:RansacLineInfo,line2:RansacLineInfo):
        line1_inliers = line1.inliers
        line2_inliers = line2.inliers

        results=[]
        for line1_inlier in line1_inliers:
            for line2_inlier in line2_inliers:
                if ((line1_inlier.X == line2_inlier.X) and (line1_inlier.Y == line2_inlier.Y)):
                    common_point=sg.Point(line1_inlier.X,line1_inlier.Y)
                    results.append(common_point)
        return results

    def test_with_2_large_perpendicular_lines_and_maxobjects_stopping_criteria(self):
        all_black_points,width,height=self.read_test_image(filenameonly="simple_image_with_perpendicular_lines.png")

        finder=RansacLineFinder(pixels=all_black_points,width=width,height=height, nnd_threshold_factor=0.5)
        finder.max_ransac_trials=10000
        finder.stopping_criteria=StoppingCriteria.MAX_OBJECTS
        finder.max_models=2
        lines=finder.find()
        self.assertGreaterEqual(len(lines),2)

        larger_line=None
        shorter_line=None
        if (len(lines[0].inliers) > len(lines[1].inliers)):
            larger_line=lines[0]
            shorter_line=lines[1]
        else:
            larger_line=lines[1]
            shorter_line=lines[0]

        self.assertGreater(len(larger_line.inliers),195)
        self.assertGreater(len(shorter_line.inliers),95)
        self.assertCommonInliers(lines[0],lines[1])

    def test_when_more_than_1_ransac_line_and_maxobjects_stopping_criteria_then_inliers_should_be_shared(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two_simple_lines.png")

        finder=RansacLineFinder(pixels=all_black_points,width=width,height=height, nnd_threshold_factor=0.5)
        finder.stopping_criteria=StoppingCriteria.MAX_OBJECTS
        finder.max_models=2
        finder.max_ransac_trials=500
        lines=finder.find()
        self.assertEqual(len(lines),2)

        actual_count_of_shared_points=1
        self.assertEqual(len(all_black_points),len(lines[0].inliers)+len(lines[1].inliers)-actual_count_of_shared_points)
        self.assertCommonInliers(lines[0],lines[1])

    def test_when_more_than_1_ransac_line_and_ransacthresholdspike_stopping_criteria_then_inliers_should_be_shared(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two_simple_lines.png")

        finder=RansacLineFinder(pixels=all_black_points,width=width,height=height,  nnd_threshold_factor=0.5)
        finder.stopping_criteria=StoppingCriteria.RANSAC_THRESHOLD_SPIKE
        finder.ransac_threshold_spike_factor=2
        finder.max_ransac_trials=500
        lines=finder.find()
        self.assertEqual(len(lines),2)

        self.assertCommonInliers(lines[0],lines[1])

    def test_with_2_large_perpendicular_lines_and_ransacthresholdspike_stopping_criteria(self):
        all_black_points,width,height=self.read_test_image(filenameonly="simple_image_with_perpendicular_lines.png")

        finder=RansacLineFinder(pixels=all_black_points,width=width,height=height, nnd_threshold_factor=0.5)
        finder.stopping_criteria=StoppingCriteria.RANSAC_THRESHOLD_SPIKE
        finder.ransac_threshold_spike_factor=2
        finder.max_ransac_trials=10000
        lines=finder.find()
        self.assertEquals(len(lines),2)

        larger_line=None
        shorter_line=None
        if (len(lines[0].inliers) > len(lines[1].inliers)):
            larger_line=lines[0]
            shorter_line=lines[1]
        else:
            larger_line=lines[1]
            shorter_line=lines[0]

        self.assertGreater(len(larger_line.inliers),195)
        self.assertGreater(len(shorter_line.inliers),95)
        self.assertCommonInliers(lines[0],lines[1])
