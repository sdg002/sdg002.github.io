from typing import List
from RansacCircleInfo import RansacCircleInfo
from RansacLineInfo import RansacLineInfo

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from entity import *

class RootModel(object):
    """docstring for RootModel."""
    def __init__(self):
        self.MAX_CIRCLES=11 #Max number of circles to find
        self.MAX_LINES=20 #Max number of lines to find
        self.RANSAC_THRESHOLD_FACTORS=[0.25,0.5]  #Multiplied by mean nearest neighbour distance to arrive at Ransac threshold
        self.DBSCAN_EPISOLON_THRESHOLD_FACTOR=[2] # Multiplied by median gap or median angular distance to arrive at the Epsilon parameter for the DBSCAN cluster detection algorithm
        self.DBSCAN_MINPOINTS=[3,6,10]  #min points parameter for DBSCAN algorithm
        self.MIN_INLIERS_FACTOR_AFTER_CLUSTERING=[0.1,0.25] #A clustered circle is discarded if it has inliers below (threshold*original_inliers)
        self.__abstracted_lines=[]
        self.__abstracted_circles=[]

    @property
    def filename(self):
        """The filename property."""
        return self._filename
    @filename.setter
    def filename(self, value):
        self._filename = value
    
    @property
    def ransac_circles(self)->List[RansacCircleInfo]:
        """The RansacCircles property."""
        return self._RansacCircles

    @ransac_circles.setter
    def ransac_circles(self, value:List[RansacCircleInfo]):
        self._RansacCircles = value        

    @property
    def ransac_lines(self)->List[RansacLineInfo]:
        """The ransac_lines property."""
        return self._ransac_lines
        
    @ransac_lines.setter
    def ransac_lines(self, value:List[RansacLineInfo]):
        self._ransac_lines = value

    @property
    def image_width(self):
        """The image_width property."""
        return self.image__width
    @image_width.setter
    def image_width(self, value):
        self.image__width = value

    @property
    def image_height(self):
        """The image_height property."""
        return self._image_height
    @image_height.setter
    def image_height(self, value):
        self._image_height = value

    @property
    def black_pixels(self):
        """The black_pixels property."""
        return self._black_pixels
    @black_pixels.setter
    def black_pixels(self, value):
        self._black_pixels = value

    @property
    def output_folder(self):
        """The output_folder where the resulting images will be created."""
        return self._output_folder
    @output_folder.setter
    def output_folder(self, value):
        self._output_folder = value

    @property
    def clustered_circles(self)->List[RansacCircleInfo]:
        """Circles obtained after finding clusters in the RANSAC circles."""
        return self._clustered_circles

    @clustered_circles.setter
    def clustered_circles(self, value:List[RansacCircleInfo]):
        self._clustered_circles = value

    @property
    def abstracted_lines(self)->List[Line]:
        """The abstracted lines property."""
        return self.__abstracted_lines

    @property
    def abstracted_circles(self)->List[Circle]:
        """The abstracted circles property."""
        return self.__abstracted_circles
