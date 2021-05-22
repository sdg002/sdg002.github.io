

from typing import List
import csv

from numpy.core.numeric import NaN


class InputRow(object):
    """Represents a row in the CSV file which has input images."""
    def __init__(self):
        self.__impagefile=None
        self.__salt_pepper=NaN
        self.__line_count=NaN
        self.__total_pixels=NaN
        self.__black_pixels=NaN
        self.__max_distance=NaN
        
    @property
    def imagefile(self):
        """The name of the image file used as an input to the algorithm"""
        return self.__impagefile

    @imagefile.setter
    def imagefile(self,value):
        self.__impagefile=value

    @property
    def salt_pepper(self):
        """
        The salt pepper ration in the input image 
        """
        return float(self.__salt_pepper)

    @salt_pepper.setter
    def salt_pepper(self,value):
        self.__salt_pepper=value
    

    @property
    def line_count(self):
        """Count of expected lines in the input image """
        return int(self.__line_count)

    @line_count.setter
    def line_count(self,value):
        """Count of expected lines in the input image """
        self.__line_count=value

    @property
    def total_pixels(self):
        """The count of all pixels in the image."""
        return int(self.__total_pixels)

    @total_pixels.setter
    def total_pixels(self, value):
        self.__total_pixels = value

    @property
    def black_pixels(self):
        """The count of black pixels in the image."""
        return int(self.__black_pixels)

    @black_pixels.setter
    def black_pixels(self, value):
        self.__black_pixels = value

    @property
    def max_distance(self):
        """The maximum distance between consecutive points in the expected line in this test image."""
        return float(self.__max_distance)

    @max_distance.setter
    def max_distance(self, value):
        self.__max_distance = value

    def __repr__(self):
        return f'imagefile={self.imagefile} , salt_pepper={self.salt_pepper}, line_count={self.line_count}  , total_pixels={self.total_pixels}  black_pixels={self.black_pixels}'

