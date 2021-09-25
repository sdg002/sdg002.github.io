import numpy as np

from typing import Union, Any, List, Optional, cast, Dict

from skimage.measure import LineModelND, ransac
import os
from skimage import io
import math
import datetime
from skimage.measure import LineModelND, ransac
import numpy as np
import simplegeometry as sg
from src.LineModel import LineModel


class RansacLineInfo(object):
    """Helper class to manage the information about the RANSAC line."""
    def __init__(self, inlier_points:np.ndarray, model:LineModelND):
        self._inliers=inlier_points #the inliers that were detected by RANSAC algo
        self._model=model    #The LinearModelND that was a result of RANSAC algo
        self._lineequation=None
    
    @property
    def unitvector(self)->sg.Point:
        """The unitvector of the model."""
        return sg.Point(self._model.params[1][0],self._model.params[1][1])

    @property
    def origin(self)->sg.Point:
        """The origin point through which the line passes."""
        return sg.Point(self._model.params[0][0],self._model.params[0][1])

    @property
    def inliers(self)->List[sg.Point]:
        """The inliers that were detected by the Ransac algorithm"""
        points = list(map(lambda p: sg.Point(p[0],p[1]), self._inliers))
        return points
    #Optimize here by using a backing property for the calculated Points

    @property
    def projected_inliers(self)->List[sg.Point]:
        """The projection of the inliers on the Ransac line"""
        projected_points=sg.LineModel.compute_projection_of_points(self.standard_equation,self.inliers)
        return projected_points


    @property
    def scikit_model(self):
        """The scikit model"""
        return self._model

    @property
    def nearest_neighbour_distance_statistic(self):
        """The nearest neighbour distance statistic in the input image that was used for producing this result."""
        return self.__nearest_neighbour_distance_statistic

    @nearest_neighbour_distance_statistic.setter
    def nearest_neighbour_distance_statistic(self, value):
        self.__nearest_neighbour_distance_statistic = value


    @property
    def ransac_threshold(self):
        """The ransac threshold that was used for producing this result"""
        return self._ransac_hreshold

    @ransac_threshold.setter
    def ransac_threshold(self, value):
        self._ransac_hreshold = value
    
    def __str__(self) -> str:
        return f"unit vector={self.unitvector}  origin={self.origin}"

    @property
    def standard_equation(self):
        """The equation in standard form. ax+by+c"""
        if (self._lineequation != None):
            return self._lineequation
                
        first_point=self.origin
        second_point=sg.Point(first_point.X + self.unitvector.X*10, first_point.Y+self.unitvector.Y*10)
        self._lineequation=sg.LineModel.create_line_from_2points(first_point.X,first_point.Y, second_point.X, second_point.Y)
        return self._lineequation
