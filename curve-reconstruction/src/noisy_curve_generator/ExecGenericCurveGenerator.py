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
salt_pepper_noise=0.90 #.95
max_distance_between_2_points= 20#15
#20 is a good upper limit with sp=0.95
#10 is a good lower limit, anything less then it becomes crowded

def create_new_absolute_filename(prefix):
    folder_script=os.path.dirname(__file__)
    folder_results=os.path.join(folder_script,"./out/")
    count_of_files=len(os.listdir(folder_results))
    new_filename=("%s.%d.png" % (prefix,count_of_files))
    file_result=os.path.join(folder_script,"./out/",new_filename)
    return file_result

def generate_sine():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.90
    generator.curvetype="sine"
    generator.max_consecutive_distance=20
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
    generator.saltpepper=0.90
    generator.curvetype="cubic"
    generator.max_consecutive_distance=15
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_parabola():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.80
    generator.curvetype="parabola"
    generator.max_consecutive_distance=10
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_spiral():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.90
    generator.curvetype="spiral"
    generator.max_consecutive_distance=10
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_circle():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.80
    generator.curvetype="circle"
    generator.max_consecutive_distance=15
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

def generate_diagonallines():
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=0.95
    generator.curvetype="diagonallines"
    generator.max_consecutive_distance=15
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()



#generate_spiral()
#generate_cubic()
#generate_sine()
#generate_cosine()
#generate_parabola()
pass
if (__name__ =="__main__"):
    generate_diagonallines()
