from typing import List
from RansacCircleInfo import RansacCircleInfo
from RansacLineInfo import RansacLineInfo

class RootModel(object):
    """docstring for RootModel."""
    def __init__(self):
        self.MAX_CIRCLES=11 #Max number of circles to find
        self.MAX_LINES=20 #Max number of lines to find
        self.RANSAC_THRESHOLD_FACTORS=[0.25,0.5]
        pass

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

