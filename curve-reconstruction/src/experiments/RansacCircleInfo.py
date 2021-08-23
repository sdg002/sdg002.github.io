
from typing import Tuple
from skimage.measure import CircleModel, ransac
import numpy as np

class RansacCircleInfo(object):
    """
    Helper class to manage information about a RANSAC circle"""
    def __init__(self, inlier_points:np.ndarray, model:CircleModel):
        self.__inliers=inlier_points
        self.__model=model
    
    def __checkforinitialization(self):
        if (self.__model == None):
            raise Exception("The class has not been initialized with a CircleModel")
        # if (self.__inliers == None):
        #     raise Exception("The class has not been initialized with inliers")
        

    @property
    def model(self)->CircleModel:
        """The Circle model."""
        return self.__model

    @property
    def inlier_points(self)->np.ndarray:
        """The inlier_points property."""
        return self.__inliers

    @property
    def center(self)->Tuple:
        """Returns the center as a tuple (x,y)."""
        self.__checkforinitialization();
        return (self.model.params[0],self.model.params[1])

    @property
    def radius(self)->float:
        """Returns the radius"""
        self.__checkforinitialization();
        return self.model.params[2]

