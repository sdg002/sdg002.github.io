import numpy as np
import random
import math

from numpy.core.numeric import NaN
from numpy.lib import utils
from RansacLineInfo import  RansacLineInfo
from typing import List

WHITE_COLOR:int=255
BLACK_COLOR:int=0

'''
Generates a monochrome image with specified width and height.
Noise is generated as per the ration salt_pepper. 
salt=white pixel and pepper=black pixel
'''
def generate_noisy_image(width:int, height:int,salt_pepper:float):
    image = np.zeros([height,width,1],dtype=np.uint8)
    for y in range(0,height):
        for x in range(0,width):
            r=random.random()
            if (r > salt_pepper):
                image[y][x][0]=0
            else:
                image[y][x][0]=WHITE_COLOR

    return image


def euclidean_distance(x1:float,y1:float, x2:float,y2:float):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
#
#Create a dotted line which starts from the specified start point and ends at the specified end point
#The distance between consecutive points should not exceed max_distance
#
def superimpose_straight_line_between_2_points(input_image:np.ndarray,start_x:float, start_y:float, end_x:float, end_y:float, max_distance:float):
    width=input_image.shape[1]
    height=input_image.shape[0]

    distance_start_end=euclidean_distance(x1=start_x, y1=start_y, x2=end_x, y2=end_y)
    unit_vector=((end_x-start_x)/distance_start_end, (end_y-start_y)/distance_start_end)

    delta=distance_start_end/2 #some random value
    last_t=0
    max_t=distance_start_end
    last_point=(start_x,start_y)
    min_distance=max_distance/2

    results=list()

    while True:
        new_t=last_t+delta
        if (new_t > max_t):
            break
        next_point=(start_x+unit_vector[0]*new_t,start_y+unit_vector[1]*new_t)
        consecutive_distance=euclidean_distance(x1=last_point[0], y1=last_point[1], x2=next_point[0], y2=next_point[1])
        if (consecutive_distance < max_distance and consecutive_distance > min_distance):
            results.append(next_point)
            last_t=new_t
            last_point=next_point
            continue
        elif (consecutive_distance <= min_distance):
            delta=delta*1.5
            continue
        elif (consecutive_distance >= max_distance):
            delta=delta*0.5
            continue
        else:
            continue

    for point in results:
        x=int(round(point[0]))
        y=int(round(height-point[1]))
        if (x<0 or x >= width):
            continue
        if (y<0 or y >= height):
            continue
        input_image[y][x][0]=BLACK_COLOR
    return input_image
    pass

def superimpose_all_ransac_lines(image:np.ndarray,line_results:List[RansacLineInfo]):
    #to be done
    #Draw all Randsac lines and inliers on top of the image
    #See method superimpose_all_inliers in SequentialRansac.py
    pass
