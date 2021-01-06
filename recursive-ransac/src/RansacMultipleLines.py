import numpy as np
from matplotlib import pyplot as plt
from typing import Union, Any, List, Optional, cast, Dict

from skimage.measure import LineModelND, ransac
import os
from skimage import io
import math
import datetime

min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to.
#min_inliers_allowed=5 #Custom parameter  - A line is selected only if these many inliers are found

class RansacLineInfo(object):
    """Helper class to manage the information about the RANSAC line."""
    def __init__(self, inlier_points:np.ndarray, model:LineModelND):
        self.inliers=inlier_points #the inliers that were detected by RANSAC algo
        self.model=model    #The LinearModelND that was a result of RANSAC algo

    @property
    def unitvector(self):
        """The unitvector of the model. This is an array of 2 elements (x,y)"""
        return self.model.params[1]

def read_black_pixels(imagefilename:str):
    #returns a numpy array with shape (N,2) N points, x=[0], y=[1]
    #The coordinate system is Cartesian
    np_image=io.imread(imagefilename,as_gray=True)
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

def extract_first_ransac_line(data_points:[], max_distance:int):
    """
    Accepts a numpy array with shape N,2  N points, with coordinates x=[0],y=[1]
    Returns 
         A numpy array with shape (N,2), these are the inliers of the just discovered ransac line
         All data points with the inliers removed
         The model line
    """
    
    
    model_robust, inliers = ransac(data_points, LineModelND, min_samples=min_samples,
                                   residual_threshold=max_distance, max_trials=1000)
    results_inliers=[]
    results_inliers_removed=[]
    for i in range(0,len(data_points)):
        if (inliers[i] == False):
            #Not an inlier
            results_inliers_removed.append(data_points[i])
            continue
        x=data_points[i][0]
        y=data_points[i][1]
        results_inliers.append((x,y))
    return np.array(results_inliers), np.array(results_inliers_removed),model_robust

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

def superimpose_all_inliers(ransac_lines,width:float, height:float):
    #Create an RGB image array with dimension heightXwidth
    #Draw the points with various colours
    #return the array

    new_image=np.full([height,width,3],255,dtype='int')
    colors=[(0,255,0),(255,255,0),(0,0,255)]
    for line_index in range(0,len(ransac_lines)):
        color=colors[line_index % len(colors)]
        ransac_lineinfo:RansacLineInfo=ransac_lines[line_index]
        inliers=ransac_lineinfo.inliers 
        y_min=inliers[:,1].min()
        y_max=inliers[:,1].max()
        x_min=inliers[:,0].min()
        x_max=inliers[:,0].max()
        plottable_points=generate_plottable_points_along_line(ransac_lineinfo.model, xmin=x_min,xmax=x_max, ymin=y_min,ymax=y_max)
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

def extract_multiple_lines_and_save(inputfilename:str,iterations:int, max_distance:int,min_inliers_allowed:int):
    """
    min_inliers_allowed - a line is selected only if it has more than this inliers. The search process is halted when this condition is met
    max_distance - This is the RANSAC threshold distance from a line for a point to be classified as inlier
    """
    print("---------------------------------------")
    print("Processing: %s" % (inputfilename))
    folder_script=os.path.dirname(__file__)
    absolute_path=os.path.join(folder_script,"images/",inputfilename)

    results:List[RansacLineInfo]=[]
    all_black_points,width,height=read_black_pixels(absolute_path)
    print("Found %d pixels in the file %s" % (len(all_black_points),inputfilename))
    starting_points=all_black_points
    for index in range(0,iterations):
        if (len(starting_points) <= min_samples):
            print("No more points available. Terminating search for RANSAC")
            break
        inlier_points,inliers_removed_from_starting,model=extract_first_ransac_line(starting_points,max_distance=max_distance)
        if (len(inlier_points) < min_inliers_allowed):
            print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),min_inliers_allowed))
            break
        starting_points=inliers_removed_from_starting
        results.append(RansacLineInfo(inlier_points,model))
        print("Found %d RANSAC lines" % (len(results)))
    superimposed_image=superimpose_all_inliers(results,width,height)
    #Save the results
    filename_noextension=os.path.splitext(inputfilename)[0]
    folder_script=os.path.dirname(__file__)
    file_result=os.path.join(folder_script,"./out/",("result-%s.png") % (filename_noextension))
    io.imsave(file_result,superimposed_image)
    print("Results saved to file %s" % (file_result))




# extract_multiple_lines_and_save("SmallCross.png",5)
# extract_multiple_lines_and_save("SmallCrossWithNoise.png",5)
# extract_multiple_lines_and_save("2ProminentLine.png",5)
#todo some problem in one of the above lines, excpetion

# extract_multiple_lines_and_save("1SmallLineWithNoise.png",iterations= 5,max_distance=1, min_inliers_allowed=15)
# extract_multiple_lines_and_save("2ProminentLineWithNoise.png",5,max_distance=3, min_inliers_allowed=5)
# extract_multiple_lines_and_save("3ProminentLineWithNoise.png",5, max_distance=3,min_inliers_allowed=5)
#extract_multiple_lines_and_save("WheelSpoke.png",iterations= 30,max_distance=1, min_inliers_allowed=50)
extract_multiple_lines_and_save("WheelSpokeNoise.png",iterations= 30,max_distance=1, min_inliers_allowed=50)