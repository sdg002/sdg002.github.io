import numpy as np
from matplotlib import pyplot as plt

from skimage.measure import LineModelND, ransac
import os
from skimage import io
import math
import datetime


def read_image_array_as_cartesian_data_points(imagefilename):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,imagefilename)
    np_image=io.imread(file_noisy_curve,as_gray=True)
    black_white_threshold=0
    if (np_image.dtype == 'float'):
        black_white_threshold=0.5
    elif (np_image.dtype == 'uint8'):
        black_white_threshold=128
    else:
        raise Exception("Invalid dtype %s " % (np_image.dtype))
    indices=np.where(np_image <= black_white_threshold)
    width=np_image.shape[1]
    height=np_image.shape[0]
    cartesian_y=height-indices[0]-1
    np_data_points=np.column_stack((indices[1],cartesian_y)) 
    return np_data_points, width,height

def find_line(data_points:np.ndarray,width,height):
    distance_from_line=2
    model_robust, inliers = ransac(data_points, LineModelND, min_samples=3,
                                   residual_threshold=distance_from_line, max_trials=1000)

    line_x = np.arange(0, width)
    line_y = model_robust.predict_y(line_x)
    blank_image=np.ones((height,width),dtype='float')
    for i in range(0,len(line_x)):
        x=int(line_x[i])
        y=height - int(line_y[i]) -1
        if (x >= width) or (y >= height):
            continue
        blank_image[y][x]=0.0

    pass
    return blank_image

def save_image(new_image_array:np.ndarray, imagefilename:str):
    filename_noextension=os.path.splitext(imagefilename)[0]
    folder_script=os.path.dirname(__file__)
    file_result=os.path.join(folder_script,"./out/",("result-%s.png") % (filename_noextension))
    io.imsave(file_result,new_image_array)


def extract_best_ransac_line(imagefile:str):
    """
    Extracts the best possible line using scikit learn's RANSAC function
    and creates a new image in the Out folder with this line
    """
    image,width,height=read_image_array_as_cartesian_data_points(imagefile)
    new_image=find_line(image,width,height)
    save_image(new_image,imagefile)
    pass




extract_best_ransac_line("1SmallLineWithNoise.png")
extract_best_ransac_line("1SmallLineWithNoise.png")


