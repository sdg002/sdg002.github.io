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

white_color=255
width=100
random.seed(datetime.datetime.now().second)

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


def generate_filename(basename:str,salt_pepper:float):
    return ("%s-%.3f.png") % (basename, salt_pepper)


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

def generate_image_with_salt_pepper_noise(salt_pepper:float):
    print("--------------------------------------------------")
    print("Generating noisy image with salt_pepper=%f" % (salt_pepper))
    #
    noisy_image=Util.generate_noisy_image(width=width, height=width,salt_pepper=salt_pepper)
    new_filename=generate_filename(basename="noisy_image", salt_pepper=salt_pepper)
    save_image(image=noisy_image,filename=new_filename)
    display_count_of_blackwhite_pixels(noisy_image)
    #
    # img = np.zeros([width,width,1],dtype=np.uint8)
    # superimpose_random_straight_line(image=img, max_distance=10)
    #replace_pixels_with_noise(noisy_image,salt_pepper)

generate_image_with_salt_pepper_noise(salt_pepper=0.5)
generate_image_with_salt_pepper_noise(salt_pepper=0.6)
generate_image_with_salt_pepper_noise(salt_pepper=0.7)
generate_image_with_salt_pepper_noise(salt_pepper=0.8)
generate_image_with_salt_pepper_noise(salt_pepper=0.9)
generate_image_with_salt_pepper_noise(salt_pepper=0.92)
generate_image_with_salt_pepper_noise(salt_pepper=0.95)
generate_image_with_salt_pepper_noise(salt_pepper=0.97)
generate_image_with_salt_pepper_noise(salt_pepper=0.99)

