
from typing import Tuple
from skimage.measure import CircleModel, ransac
import numpy as np
from skimage.util import dtype
import simplegeometry as sg
import  math

class RansacCircleInfo(object):
    """
    Helper class to manage information about a RANSAC circle"""
    def __init__(self, inlier_points:np.ndarray, model:CircleModel):
        self.__inliers=inlier_points
        self.__model=model
        self.__projected_inliers=None
        self.__center=None
    
    def __checkforinitialization(self):
        if (self.__model == None):
            raise Exception("The class has not been initialized with a CircleModel")
        if (self.__center == None):
            self.__center = sg.Point(self.model.params[0],self.model.params[1])
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
    def center(self)->sg.Point:
        """Returns the center as a tuple (x,y)."""
        self.__checkforinitialization();
        #return (self.model.params[0],self.model.params[1])
        return self.__center

    @property
    def radius(self)->float:
        """Returns the radius"""
        self.__checkforinitialization();
        return self.model.params[2]

    def __str__(self) -> str:
        return f"center={self.center}  radius={self.radius}"

    
    @property
    def projected_inliers(self):
        """
        The projection of the inliers on the circle model and in sequence
        Each item in the array represents the projection of an inlier (x,y,theta)
        x,y are the cartesian coordinates
        theta is the angular orientation the vector (center to projection) makes with the X axis
        """
        if (self.__projected_inliers != None):
            return self.__projected_inliers
        total_points=self.inlier_points.shape[0]
        np_temp=np.empty(dtype='float', shape=[len(self.inlier_points),3])
        for index in range(0,total_points):
            inlier_x=self.inlier_points[index][0] 
            inlier_y=self.inlier_points[index][1]
            vector=sg.Vector(inlier_x-self.center.X,inlier_y-self.center.Y)
            unit_vector=vector.UnitVector
            projected_x=unit_vector.X *self.radius
            projected_y=unit_vector.Y *self.radius
            np_temp[index][0]=projected_x+self.center.X
            np_temp[index][1]=projected_y+self.center.Y
            #We want to use 0 to 2pi range for the angles so that the points can be sorted
            theta=sg.MathUtil.atan2_0to2pi(unit_vector.Y,unit_vector.X)
            np_temp[index][2]=theta
        
        lst_temp=list(map(lambda x:(x[0],x[1],x[2]),np_temp))
        lst_temp_sorted=sorted(lst_temp, key=lambda x:x[2])
        self.__projected_inliers=np.array(lst_temp_sorted)
        return self.__projected_inliers
    
    @property
    def ransac_threshold(self):
        """The ransac_threshold that was used for determing this circle."""
        return self._ransac_threshold
    @ransac_threshold.setter
    def ransac_threshold(self, value):
        self._ransac_threshold = value

    @property
    def mean_nnd(self):
        """The mean nearest neighbour distance of the image that was used for determining this circle."""
        return self._mean_nnd
    @mean_nnd.setter
    def mean_nnd(self, value):
        self._mean_nnd = value