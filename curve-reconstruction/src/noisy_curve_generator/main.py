import numpy as np
import os
import skimage
import random
import math

import simplegeometry as sg
from GenericCurveGenerator import GenericCurveGenerator



#
#Create blank image
#
img_back_color=255
img_width=500
img_height=200
salt_pepper_noise= 0.99 #0.95 #0.8 #0.90 #.95
max_distance_between_2_points= 8#10 #20#15
#20 is a good upper limit with sp=0.95
#10 is a good lower limit, anything less then it becomes crowded

def create_new_absolute_filename(prefix):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    folder_results=os.path.join(folder_script,"./out/")
    count_of_files=len(os.listdir(folder_results))
    new_filename=("%s.%d.png" % (prefix,count_of_files))
    file_result=os.path.join(folder_script,"./out/",new_filename)
    return file_result

def generate_sine():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="sine"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()
    pass

def generate_cosine():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.95
    generator.curvetype="cosine"
    generator.max_consecutive_distance=20
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()
    pass

def generate_cubic():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="cubic"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_parabola():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="parabola"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_spiral():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="spiral"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_circle():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="circle"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_diagonallines():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="diagonallines"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    print(generator.output_file)
    print(333)
    generator.generate_curve()



pass
if (__name__ =="__main__"):
    generate_cubic()
    generate_parabola()
    generate_circle()
    generate_spiral()
    generate_sine()
    generate_diagonallines()
