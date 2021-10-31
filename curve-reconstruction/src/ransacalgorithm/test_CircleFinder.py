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
        self.assertGreaterEqual(len(first_circle.inlier_points),105)

        for circle_result in range(0,max_circle_results):
            self.superimpose_resulting_circle(imagefilename="one_simple_circle.png", resultfilename=f"one_simple_circle.{circle_result}.superimposed.png",circle=ransac_circles[circle_result])

        pass

    