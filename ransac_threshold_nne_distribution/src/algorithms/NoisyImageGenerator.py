


import csv
from os import path
from typing import List
import numpy as np
import random
import datetime
from skimage import io
import os
import Util

WHITE=255


class NoisyImageGenerator(object):
    def __init__(self, salt_pepper_ratio:float, max_distance_between_points:float,output_folder:str,width:float, height:float,max_lines:int):
        self._salt_pepper_ratio=salt_pepper_ratio
        self._max_distance_between_points=max_distance_between_points
        self._output_folder=output_folder
        self._image_width=width
        self._image_height=height
        self._max_lines=max_lines
        self._noisy_image:np.ndarray=None
        random.seed(datetime.datetime.now())
    
    @property
    def filename(self):
        """Generates a filename based on parameters supplied in the constructore."""
        return ("%s-LINECOUNT-%d-SP-%.3f-MAXD-%.1f.png") % ("NoisyImage", self._max_lines,self._salt_pepper_ratio,self._max_distance_between_points)        

    @property
    def count_of_blackpixels(self):
        """Returns the  count of blackpixels in the generatd image."""
        all_white_indices=np.where(self._noisy_image == WHITE)
        count_of_white=len(all_white_indices[0])
        count_of_black=self._noisy_image.shape[0]*self._noisy_image.shape[1] - count_of_white
        return count_of_black

    @property
    def total_pixel_count(self):
        """The total number of pixels in the image."""
        return self._noisy_image.shape[0]*self._noisy_image.shape[1]

    @total_pixel_count.setter
    def total_pixel_count(self, value):
        self._total_pixel_count = value

    def create_noisy_image(self):
        noisy_image=Util.generate_noisy_image(width=self._image_width, height=self._image_height,salt_pepper=self._salt_pepper_ratio)

        for line_index in range(0,self._max_lines):
            #alternate the lines left edge to right edge, top edge to bottom edge
            if (line_index%2 ==0):                
                random_x_first=(self._image_width)*random.random()
                random_x_second=self._image_width - random_x_first
                bottom_edge=0
                top_edge=self._image_height
                noisy_image=Util.superimpose_straight_line_between_2_points(noisy_image,start_x=random_x_first, start_y=bottom_edge, end_x=random_x_second, end_y=top_edge, max_distance=self._max_distance_between_points)
            else:
                left_edge=0
                right_edge=self._image_width
                random_y_first=(self._image_height)*random.random()
                random_y_second=self._image_height -random_y_first
                noisy_image=Util.superimpose_straight_line_between_2_points(noisy_image,start_x=left_edge, start_y=random_y_first, end_x=right_edge, end_y=random_y_second, max_distance=self._max_distance_between_points)

        
        absolute_filepath=os.path.join(self._output_folder,self.filename)
        io.imsave(absolute_filepath,noisy_image)
        self._noisy_image=noisy_image
        pass
