from skimage.measure import LineModelND, ransac
import numpy as np
from Point import Point
from typing import List

class RansacLineInfo(object):
    """Helper class to manage the information about the RANSAC line."""
    def __init__(self, inlier_points:np.ndarray, model:LineModelND):
        self._inliers=inlier_points #the inliers that were detected by RANSAC algo
        self._model=model    #The LinearModelND that was a result of RANSAC algo

    @property
    def unitvector(self)->Point:
        """The unitvector of the model."""
        return Point(self._model.params[1][0],self._model.params[1][1])

    @property
    def inliers(self)->List[Point]:
        """The inliers that were detected by the Ransac algorithm"""
        points = list(map(lambda p: Point(p[0],p[1]), self._inliers))
        return points

