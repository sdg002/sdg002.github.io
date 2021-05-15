#
#In this program I am generating a Salt+Pepper noise via manual random number generator
#Approach
#   Iterate over all cells in the array
#   If random > salt_pepper then set pixel to black
#
#   The count of white and black pixels appear to tally with the probabilty , i.e. salt_pepper




from os import linesep, path
from typing import List
import numpy as np
import random
from numpy.lib.type_check import imag
from skimage import io
import os
import datetime
import math;
import Util
import csv
from NoisyImageGenerator import NoisyImageGenerator

IMAGE_WIDTH=150
IMAGE_HEIGHT=100


# print line coordinates as json string within csv
# remove all the rest
# make this script repeatable and not having to make changes. Prompt for action
# salt_pepper_ratios=[0.9, 0.92, 0.95, 0.97,0.99]
# max_distances=[2,3,5,7,10]
# salt_pepper_ratios=[ 0.95, 0.97,0.99]
# max_distances=[2,3,5]


def generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios:List[float],max_distances:List[float],sub_folder:str,lines_count:int):
    if (not sub_folder):
        raise Exception("Subfolder must be specified")
    
    folder_script=os.path.dirname(__file__)
    folder_results=os.path.join(folder_script,"./out/",sub_folder)
    if (os.path.exists(folder_results)==False):
        print("The folder %s was not found. Creating" % (folder_results))
        os.mkdir(folder_results)
        print("The folder %s was created" % (folder_results))
    print("Results will be generated in the output folder %s" % (folder_results))
    csv_output=os.path.join(folder_results,"input_images.csv")
    count_of_images=0
    with open(csv_output, mode='w', newline='') as csv_file:
        testimage_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        testimage_writer.writerow(["imagefile","salt_pepper","max_distance","line_count","total_pixels","black_pixels"])
        for salt_pepper in salt_pepper_ratios:
            for max_distance in max_distances:
                generator=NoisyImageGenerator(salt_pepper_ratio=salt_pepper, max_distance_between_points=max_distance, output_folder=folder_results,width=IMAGE_WIDTH, height=IMAGE_HEIGHT, max_lines=lines_count)
                generator.create_noisy_image()
                outputfile=generator.filename
                count_of_black_pixels=generator.count_of_blackpixels
                total_pixels=generator.total_pixel_count
                print("Generated noisy image with salt-pepper=%f, max_distance=%f , filename=%s, black_pixels=%d total_pixels=%d" % (salt_pepper,max_distance,outputfile, count_of_black_pixels,total_pixels))
                testimage_writer.writerow([outputfile,salt_pepper,max_distance,lines_count,count_of_black_pixels,total_pixels])
                count_of_images+=1
    print("Total images generated=%d" % (count_of_images))


generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.99],max_distances=[2,3,5], sub_folder="very_small_dataset_2lines", lines_count=2)
generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.95, 0.97,0.99],max_distances=[2,3,5], sub_folder="small_dataset_2lines", lines_count=2)
generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.95, 0.97,0.99],max_distances=[2,3,5], sub_folder="small_dataset_1line", lines_count=1)

