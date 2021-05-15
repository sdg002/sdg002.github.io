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
from data.InputRow import InputRow
from data.CsvHelper import CsvHelper

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
    csv_output_file=os.path.join(folder_results,"input_images.csv")
    input_rows:List[InputRow]=[]

    for salt_pepper in salt_pepper_ratios:
        for max_distance in max_distances:
            generator=NoisyImageGenerator(salt_pepper_ratio=salt_pepper, max_distance_between_points=max_distance, output_folder=folder_results,width=IMAGE_WIDTH, height=IMAGE_HEIGHT, max_lines=lines_count)
            generator.create_noisy_image()
            outputfile=generator.filename
            count_of_black_pixels=generator.count_of_blackpixels
            total_pixels=generator.total_pixel_count
            print("\tGenerated noisy image with salt-pepper=%f, max_distance=%f , filename=%s, black_pixels=%d total_pixels=%d" % (salt_pepper,max_distance,outputfile, count_of_black_pixels,total_pixels))

            new_row=InputRow()
            new_row.imagefile=outputfile
            new_row.total_pixels=total_pixels
            new_row.black_pixels=count_of_black_pixels
            new_row.salt_pepper=salt_pepper
            new_row.max_distance=max_distance
            new_row.line_count=lines_count
            input_rows.append(new_row)

    print("Total images generated=%d" % (len(input_rows)))
    CsvHelper.write_input_rows_to_csv(filename=csv_output_file,input_rows=input_rows)
    print("------------------------------------------------------")



def main():
    generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.99],max_distances=[2,3,5], sub_folder="very_small_dataset_2lines", lines_count=2)
    generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.95, 0.97,0.99],max_distances=[2,3,5], sub_folder="small_dataset_2lines", lines_count=2)
    generate_small_noisy_images_with_salt_pepper_rations_max_distances(salt_pepper_ratios=[ 0.95, 0.97,0.99],max_distances=[2,3,5], sub_folder="small_dataset_1line", lines_count=1)

if __name__ == "__main__":
    main()


