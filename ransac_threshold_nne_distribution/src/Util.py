import numpy as np
import math

from numpy.core.numeric import NaN
from numpy.lib import utils
from RansacLineInfo import  RansacLineInfo
from typing import List
from skimage.measure import LineModelND, ransac
import datetime

WHITE_COLOR:int=255
BLACK_COLOR:int=0

'''
Generates a monochrome image with specified width and height.
Noise is generated as per the ration salt_pepper. 
salt=white pixel and pepper=black pixel
'''
def generate_noisy_image(width:int, height:int,salt_pepper:float):
    np.random.seed(datetime.datetime.now().second)
    image = np.zeros([height,width,1],dtype=np.uint8)
    for y in range(0,height):
        for x in range(0,width):
            r=np.random.random()
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

def generate_plottable_points_along_line(model:LineModelND, xmin:int,xmax:int, ymin:int, ymax:int):
    """
    Computes points along the specified line model
    The visual range is 
    between xmin and xmax along X axis
        and
    between ymin and ymax along Y axis
    return shape is [[x1,y1],[x2,y2]]
    """
    unit_vector=model.params[1]
    slope=abs(unit_vector[1]/unit_vector[0])
    x_values=None
    y_values=None
    if (slope > 1):
        y_values=np.arange(ymin, ymax,1)
        x_values=model.predict_x(y_values)
    else:        
        x_values=np.arange(xmin, xmax,1)
        y_values=model.predict_y(x_values)

    np_data_points=np.column_stack((x_values,y_values)) 
    return np_data_points


def superimpose_all_ransac_lines(image:np.ndarray,ransac_lines:List[RansacLineInfo]):
    #to be done
    #Draw all Randsac lines and inliers on top of the image
    #See method superimpose_all_inliers in SequentialRansac.py
    
    width=image.shape[1]
    height=image.shape[0]

    #new_image=np.array(image, copy=True)
    new_image=np.full([height,width,3],255,dtype='int')

    colors=[(255,0,0),(255,255,0),(0,0,255)]
    for line_index in range(0,len(ransac_lines)):
        color=colors[line_index % len(colors)]
        ransac_lineinfo:RansacLineInfo=ransac_lines[line_index]
        inlier_points=ransac_lineinfo.inliers 
        y_values=list(map(lambda p:p.Y,inlier_points))
        x_values=list(map(lambda p:p.X,inlier_points))

        y_min=min(y_values)
        y_max=max(y_values)
        x_min=min(x_values)
        x_max=max(x_values)
        plottable_points=generate_plottable_points_along_line(ransac_lineinfo.scikit_model, xmin=x_min,xmax=x_max, ymin=y_min,ymax=y_max)
        for point in plottable_points:
            x=int(round(point[0]))
            if (x >= width) or (x < 0):
                continue
            y=int(round(point[1]))
            if (y >= height) or (y < 0):
                continue
            new_y=height-y-1
            new_image[new_y][x][0]=color[0]
            new_image[new_y][x][1]=color[1]
            new_image[new_y][x][2]=color[2]
    return new_image


    raise Exception("Could not complete ")
    pass
