import os
import unittest
import skimage
import skimage.io
import numpy as np
import glob

from ransacalgorithm.RansacCircleInfo import RansacCircleInfo
from .RansacLineInfo import RansacLineInfo
from .RansacCircleFinder import RansacCircleFinder
import simplegeometry as sg


class Test_CircleFinder(unittest.TestCase):
    """docstring for Test_CircleFinder."""

    def purge_outputdir(self):
        folder_script=os.path.dirname(__file__)
        results_dir=os.path.join(folder_script,"out")
        files=glob.glob(results_dir+"/*.*")
        for file in files:
            print(f"Going to delete file {file}")
            os.remove(file)
        pass

    def setUp(self) -> None:
        self.purge_outputdir()

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
    
    def superimpose_resulting_circle(self,imagefilename:str,resultfilename:str,circle:RansacCircleInfo):
        folder_script=os.path.dirname(__file__)
        original_imagefilename=os.path.join(folder_script,"test",imagefilename)
        result_imagefilename=os.path.join(folder_script,"out",resultfilename)
        np_original_image=skimage.io.imread(original_imagefilename,as_gray=True)
        points_list = list(map(lambda x: sg.Point(x[0],x[1]) , circle.inlier_points ))
        np_newimage=sg.Util.superimpose_points_on_image(np_original_image,points_list,255,255,0)
        skimage.io.imsave(result_imagefilename,np_newimage)
        pass

    def test_with_1_circle(self):
        all_black_points,width,height=self.read_test_image(filenameonly="one_simple_circle.png")
        max_circle_results=3
        finder=RansacCircleFinder(pixels=all_black_points,width=width,height=height, max_models=max_circle_results, nnd_threshold_factor=1.0,max_ransac_trials=200)
        ransac_circles=finder.find()
        first_circle=ransac_circles[0]
        self.assertAlmostEquals(first_circle.center.X,45,delta=2)
        self.assertAlmostEquals(first_circle.center.Y,57,delta=2)
        self.assertAlmostEquals(first_circle.radius,28,delta=2)
        self.assertGreaterEqual(len(first_circle.inlier_points),150)

        for circle_result in range(0,max_circle_results):
            self.superimpose_resulting_circle(imagefilename="one_simple_circle.png", resultfilename=f"one_simple_circle.{circle_result}.superimposed.png",circle=ransac_circles[circle_result])

        pass

    def test_with_2_concentric_circles(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two_concentric_circles.png")
        max_circle_results=3
        finder=RansacCircleFinder(pixels=all_black_points,width=width,height=height, max_models=max_circle_results, nnd_threshold_factor=1,max_ransac_trials=200)
        ransac_circles=finder.find()
        outer_circle=None
        inner_circle=None
        if (ransac_circles[0].radius > ransac_circles[1].radius):
            outer_circle=ransac_circles[0]
            inner_circle=ransac_circles[1]
        else:
            outer_circle=ransac_circles[1]
            inner_circle=ransac_circles[0]

        self.assertAlmostEquals(outer_circle.center.X,45,delta=2)
        self.assertAlmostEquals(outer_circle.center.Y,57,delta=2)
        self.assertAlmostEquals(outer_circle.radius,28,delta=2)
        self.assertGreaterEqual(len(outer_circle.inlier_points),120)

        self.assertAlmostEquals(inner_circle.center.X,45,delta=2)
        self.assertAlmostEquals(inner_circle.center.Y,57,delta=2)
        self.assertAlmostEquals(inner_circle.radius,17,delta=2)
        self.assertGreaterEqual(len(inner_circle.inlier_points),95)

        for circle_result in range(0,max_circle_results):
            self.superimpose_resulting_circle(imagefilename="two_concentric_circles.png", resultfilename=f"two_concentric_circles.{circle_result}.superimposed.png",circle=ransac_circles[circle_result])

    def test_with_2_sidebyside_circles(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two_circles-side-by-side.png")
        max_circle_results=3
        finder=RansacCircleFinder(pixels=all_black_points,width=width,height=height, max_models=max_circle_results, nnd_threshold_factor=1,max_ransac_trials=200)
        ransac_circles=finder.find()
        larger_circle=None
        smaller_circle=None
        if (ransac_circles[0].radius > ransac_circles[1].radius):
            larger_circle=ransac_circles[0]
            smaller_circle=ransac_circles[1]
        else:
            larger_circle=ransac_circles[1]
            smaller_circle=ransac_circles[0]

        self.assertAlmostEquals(larger_circle.center.X,45,delta=2)
        self.assertAlmostEquals(larger_circle.center.Y,57,delta=2)
        self.assertAlmostEquals(larger_circle.radius,28,delta=2)
        self.assertGreaterEqual(len(larger_circle.inlier_points),120)

        self.assertAlmostEquals(smaller_circle.center.X,65,delta=2)
        self.assertAlmostEquals(smaller_circle.center.Y,31,delta=2)
        self.assertAlmostEquals(smaller_circle.radius,20,delta=2)
        self.assertGreaterEqual(len(smaller_circle.inlier_points),100)

        for circle_result in range(0,max_circle_results):
            self.superimpose_resulting_circle(imagefilename="two_circles-side-by-side.png", resultfilename=f"two_circles-side-by-side.{circle_result}.superimposed.png",circle=ransac_circles[circle_result])

    def test_with_2_simple_circles_inliers_mustbe_shared(self):
        all_black_points,width,height=self.read_test_image(filenameonly="two-simple-circles.png")
        max_circle_results=3
        finder=RansacCircleFinder(pixels=all_black_points,width=width,height=height, max_models=max_circle_results, nnd_threshold_factor=1,max_ransac_trials=200)
        ransac_circles=finder.find()

        first_circle=ransac_circles[0]
        second_circle=ransac_circles[1]

        for circle_result in range(0,len(ransac_circles)):
            self.superimpose_resulting_circle(imagefilename="two-simple-circles.png", resultfilename=f"two-simple-circles.{circle_result}.superimposed.png",circle=ransac_circles[circle_result])

        first_circle_inliers = list(map(lambda x: sg.Point(x[0],x[1]) , first_circle.inlier_points ))
        second_circle_inliers = list(map(lambda x: sg.Point(x[0],x[1]) , second_circle.inlier_points ))

        count_of_overlaps=0
        for first_circle_inlier in first_circle_inliers:
            for second_circle_inlier in second_circle_inliers:
                if ((first_circle_inlier.X == second_circle_inlier.X) and (first_circle_inlier.Y == second_circle_inlier.Y)):
                    count_of_overlaps=count_of_overlaps+1

        self.assertGreater(count_of_overlaps,1,"There must be 1 or more common inliers between the 2 ransac circles")