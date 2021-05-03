#
#In this program I am generating a Salt+Pepper noise via manual random number generator
#Approach
#   Iterate over all cells in the array
#   If random > salt_pepper then set pixel to black
#
#   The count of white and black pixels appear to tally with the probabilty , i.e. salt_pepper




import numpy as np
import random
from skimage import io
import os
import datetime

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
    pass


def generate_image_with_salt_pepper_noise(salt_pepper:float):
    print("--------------------------------------------------")
    img = np.zeros([width,width,1],dtype=np.uint8)
    print("Generating noisy image with salt_pepper=%f" % (salt_pepper))
    replace_pixels_with_noise(img,salt_pepper)
    new_filename=generate_filename(basename="noisy_image", salt_pepper=salt_pepper)
    save_image(image=img,filename=new_filename)
    display_count_of_blackwhite_pixels(img)

generate_image_with_salt_pepper_noise(salt_pepper=0.5)
generate_image_with_salt_pepper_noise(salt_pepper=0.6)
generate_image_with_salt_pepper_noise(salt_pepper=0.7)
generate_image_with_salt_pepper_noise(salt_pepper=0.8)
generate_image_with_salt_pepper_noise(salt_pepper=0.9)
generate_image_with_salt_pepper_noise(salt_pepper=0.92)
generate_image_with_salt_pepper_noise(salt_pepper=0.95)
generate_image_with_salt_pepper_noise(salt_pepper=0.97)
generate_image_with_salt_pepper_noise(salt_pepper=0.99)

