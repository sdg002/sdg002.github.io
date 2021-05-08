#
#In this program I am generating a Salt+Pepper noise via manual random number generator
#Approach
#   Iterate over all cells in the array
#   If random > salt_pepper then set pixel to black
#
#   The count of white and black pixels appear to tally with the probabilty , i.e. salt_pepper




import numpy as np
import random
from numpy.lib.type_check import imag
from skimage import io
import os
import datetime
import math;
import Util

WHITE=255
IMAGE_WIDTH=150
IMAGE_HEIGHT=100
random.seed(datetime.datetime.now())

def replace_pixels_with_noise(image:np.ndarray, prob_noise:float):
    height=image.shape[0]
    width=image.shape[1]
    for y in range(0,height):
        for x in range(0,width):
            r=random.random()
            if (r > prob_noise):
                image[y][x][0]=0
            else:
                image[y][x][0]=255


def generate_filename(basename:str,salt_pepper:float, max_distance:float):
    return ("%s-SP-%.3f-MAXD-%.1f.png") % (basename, salt_pepper,max_distance)


def save_image(image:np.ndarray,filename):
    folder_script=os.path.dirname(__file__)
    folder_results=os.path.join(folder_script,"./out/")
    absolute_filepath=os.path.join(folder_script,"./out/",filename)
    io.imsave(absolute_filepath,image)
    print("Image saved to fileL%s" % (absolute_filepath))
    pass

def display_count_of_blackwhite_pixels(image:np.ndarray):
    all_white_indices=np.where(image == 255)
    count_of_white=len(all_white_indices[0])
    count_of_black=image.shape[0]*image.shape[1] - count_of_white
    print("Total white=%d   Total black=%d" % (count_of_white, count_of_black))
    print("Actual salt_pepper=%f" % (count_of_white/(count_of_white+count_of_black)))
    pass


'''
    max_distance = the maximum allowed distance between 2 consecutive RANSAC points
'''
def superimpose_random_straight_line(image:np.ndarray, max_distance:float):
    image_width=image.shape[1]
    image_height=image.shape[0]
    y1=0
    x1=random.random() * image_width

    y2=image_height-1
    x2=random.random() * image_width

    #you were here - how to generate the points of a straight line
    vector=(x2-x1,y2-y1)
    magnitude=math.sqrt( (vector[0])**2 + (vector[1])**2)
    uni_vector=(vector[0]/magnitude, vector[1]/magnitude )

    t=0.5
    x_start=x1
    y_start=y1
    while (True):
        x_new=x1 + t*uni_vector[0]
        y_new=y1 + t*uni_vector[1]
        gap=math.sqrt( (x_new-x_start)**2 + (y_new-y_start)**2 )
        if (gap > max_distance):
            t=t*0.5
            continue
        if (gap <= max_distance):
            t=t*1.5

        #record x_new and y_new
        x_start=x_new
        y_start=y_new

    return image

'''
    Creates a noisy image comprising of black and white pixels with specified salt-pepper ratio
    One random line is generated where the points are separated with the specified distance
'''
def generate_image_with_salt_pepper_noise_and_1_line(salt_pepper:float, max_distance_between_points:float):
    print("--------------------------------------------------")
    print("Generating noisy image with 1 line, salt_pepper=%f , max_distance=%f" % (salt_pepper, max_distance_between_points))
    
    noisy_image=Util.generate_noisy_image(width=IMAGE_WIDTH, height=IMAGE_HEIGHT,salt_pepper=salt_pepper)
    display_count_of_blackwhite_pixels(noisy_image)

    random_x_first=(IMAGE_WIDTH)*random.random()
    random_x_second=IMAGE_WIDTH - random_x_first

    bottom_edge=0
    top_edge=IMAGE_HEIGHT

    noisy_image=Util.superimpose_straight_line_between_2_points(noisy_image,start_x=random_x_first, start_y=bottom_edge, end_x=random_x_second, end_y=top_edge, max_distance=max_distance_between_points)
    
    new_filename=generate_filename(basename="noisy_image_with_1_line", salt_pepper=salt_pepper, max_distance=max_distance_between_points)
    save_image(image=noisy_image,filename=new_filename)

def generate_image_with_salt_pepper_noise_and_2_lines(salt_pepper:float, max_distance_between_points:float):
    print("--------------------------------------------------")
    print("Generating noisy image with 2 lines,salt_pepper=%f , max_distance=%f" % (salt_pepper, max_distance_between_points))
    
    noisy_image=Util.generate_noisy_image(width=IMAGE_WIDTH, height=IMAGE_HEIGHT,salt_pepper=salt_pepper)
    display_count_of_blackwhite_pixels(noisy_image)

    random_x_first=(IMAGE_WIDTH)*random.random()
    random_x_second=IMAGE_WIDTH - random_x_first
    bottom_edge=0
    top_edge=IMAGE_HEIGHT

    noisy_image_with_first_line=Util.superimpose_straight_line_between_2_points(noisy_image,start_x=random_x_first, start_y=bottom_edge, end_x=random_x_second, end_y=top_edge, max_distance=max_distance_between_points)

    left_edge=0
    right_edge=IMAGE_WIDTH
    random_y_first=(IMAGE_HEIGHT)*random.random()
    random_y_second=IMAGE_HEIGHT -random_y_first

    noisy_image_with_second_line=Util.superimpose_straight_line_between_2_points(noisy_image_with_first_line,start_x=left_edge, start_y=random_y_first, end_x=right_edge, end_y=random_y_second, max_distance=max_distance_between_points)
    
    new_filename=generate_filename(basename="noisy_image_2_lines", salt_pepper=salt_pepper, max_distance=max_distance_between_points)
    save_image(image=noisy_image_with_second_line,filename=new_filename)


def generate_images_with_various_degrees_of_salt_pepper_ratios():
    salt_pepper_ratios=[0.9, 0.92, 0.95, 0.97,0.99]
    max_distances=[2,3,5,7,10]
    for salt_pepper in salt_pepper_ratios:
        for max_distance in max_distances:
            generate_image_with_salt_pepper_noise_and_1_line(salt_pepper=salt_pepper, max_distance_between_points=max_distance)
            generate_image_with_salt_pepper_noise_and_2_lines(salt_pepper=salt_pepper, max_distance_between_points=max_distance)


generate_images_with_various_degrees_of_salt_pepper_ratios()
