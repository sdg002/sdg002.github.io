import sys
from typing import List
import numpy as np
import os
from numpy.lib.function_base import diff
import skimage
import skimage.io
from skimage.measure import CircleModel, ransac
from CircleFinder import CircleFinder
from LineFinder import LineFinder
from RansacCircleInfo import RansacCircleInfo
from RansacLineInfo import RansacLineInfo
import simplegeometry as sg
from RootModel import RootModel
from OutputGenerator import *
import statistics
from sklearn.cluster import DBSCAN



'''
    Plots the tuple of points
'''
def superimpose_points(points:List[tuple],width:float, height:float):
    new_image=np.full([height,width,3],255,dtype='int')
    colors=[(0,255,0),(255,255,0),(0,0,255)]  #todo change to Red,Green,Blue
    for point_index in range(0,len(points)):
        point=points[point_index]
        color=colors[point_index % len(colors)]
        x=int(round(point[0]))
        y=int(round(point[1]))
        print(f"x={x} y={y}")
        if (x >= width) or (x < 0):
            continue
        if (y >= height) or (y < 0):
            continue
        new_y=height-y-1
        new_image[new_y][x][0]=color[0]
        new_image[new_y][x][1]=color[1]
        new_image[new_y][x][2]=color[2]
    return new_image

'''
    returns a numpy array with shape (N,2) N points, x=[0], y=[1]
    The coordinate system is Cartesian
'''
def read_black_pixels(imagefilename:str):
    np_image=skimage.io.imread(imagefilename,as_gray=True)
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



def find_circles(model:RootModel):
    circle_results:List[RansacCircleInfo]=[]
    for ransac_threshold_factor in model.RANSAC_THRESHOLD_FACTORS:
        finder=CircleFinder(pixels=model.black_pixels,width=model.image_width,height=model.image_height, max_models=model.MAX_CIRCLES , nnd_threshold_factor=ransac_threshold_factor)        
        circles= finder.find()
        circle_results.extend(circles)
    model.ransac_circles=circle_results
    pass

def find_consecutive_differences(values:List[float]):
    results=[]
    for index in range(0,len(values)-1):
        diff=values[index+1]-values[index]
        results.append(diff)
    return results

def find_circle_clusters(model:RootModel):
    circle:RansacCircleInfo
    clustered_circles=[]
    #
    #Cluster processing can be parameterized by writing a central function which accepts the following
    #   RANSAC circle
    #   epislon threshold
    #   minp points
    #Call this function via itertools.product
    #
    for circle in model.ransac_circles:
        projected_inliers=circle.projected_inliers
        thetas=list(map(lambda x: x[2], projected_inliers))
        diffs=find_consecutive_differences(thetas)
        median=statistics.median(diffs)
        epsilon=median*model.DBSCAN_EPISOLON_THRESHOLD_FACTOR[0]  #should use itertools
        new_datapoints_2d=list(map(lambda x: [x], thetas))
        data_points=np.array(new_datapoints_2d)
        dbs=DBSCAN(eps=epsilon, min_samples=model.DBSCAN_MINPOINTS[0]) #we  should use all the values and use itertools
        dbs.fit(new_datapoints_2d)
        
        count_of_outliers=len(list(filter(lambda  l: l==-1, dbs.labels_)))
        set_of_clusters=set(filter(lambda  l: l!=-1, dbs.labels_))
        print(f"Found {len(set_of_clusters)} clusters in RANSAC circle , outliers:{count_of_outliers}, initial points={len(thetas)}")
        permissible_lower_limit_of_points=model.MIN_INLIERS_FACTOR_AFTER_CLUSTERING[0]* len(circle.inlier_points) #Should use itertools
        clusterable_point_indices=np.where(dbs.labels_ != -1)
        for cluster_index in set_of_clusters:
            cluster_point_indices=np.where(dbs.labels_ == cluster_index)
            new_inliers=projected_inliers[list(cluster_point_indices[0])]
            new_inliers_notheta=new_inliers[:,0:2]
            if (len(new_inliers) < permissible_lower_limit_of_points):
                print(f"\tThe count of inliers:{len(new_inliers)} is less than the threshold:{permissible_lower_limit_of_points}. Skipping circle")
                continue
            new_circle = RansacCircleInfo(new_inliers_notheta,circle.model)
            print(f"\tGoing to create a new circle at index {cluster_index}, points={len(new_inliers)}, median arc separation={circle.radius * median}, original radius={circle.radius} new radius={new_circle.radius} original center={circle.center} newcenter={new_circle.center}")
            clustered_circles.append(new_circle)
        #THE ABOVE WORKS - 
        # https://stackoverflow.com/questions/44887695/execute-function-on-all-possible-combinations-of-parameters
        # You should examine the resulting images - before it is too late
        # How to see results? Use the same function and use Model.clustered_circles
        # TIDY UP THE CODE, 
        print(f"Found {len(clustered_circles)} circles")
    model.clustered_circles=clustered_circles
    print(f"Found a total of {len(model.clustered_circles)} circles from {len(model.ransac_circles)} ransac circles")
    pass

def find_lines(model:RootModel):
    line_results:List[RansacCircleInfo]=[]
    for ransac_threshold_factor in model.RANSAC_THRESHOLD_FACTORS:
        finder=LineFinder(pixels=model.black_pixels,width=model.image_width,height=model.image_height, max_models=model.MAX_LINES, nnd_threshold_factor=ransac_threshold_factor)
        lines=finder.find()
        line_results.extend(lines)
    model.ransac_lines=line_results
    pass

def read_image(model:RootModel):
    all_black_points,width,height=read_black_pixels(model.filename)
    model.black_pixels=all_black_points
    model.image__width=width
    model.image_height=height

def process_file(filename:str):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path=os.path.join(folder_script,"data/",filename)

    model=RootModel()
    model.filename=absolute_path

    fullpathtoscript=os.path.realpath(__file__)
    model.output_folder=os.path.join(os.path.dirname(fullpathtoscript),"out/")

    read_image(model)

    find_circles(model) 
    find_circle_clusters(model)
    #OutputGenerator.plot_circles_with_projections(model) 
    
    #temporary commenting out to speed up 
    # find_lines(model)  
    # OutputGenerator.plot_lines_with_projections(model=model)

    #the line result - does it work? worked once , did not work second time
    #you were here - move on to finding circles with some continuitt
    #use the median distance as the epsilon


    pass


if (__name__ =="__main__"):
    print("Inside main")
    process_file(filename='cubic.W=500.H=200.MAXD=8.SP=0.99.26.png')
    #process_parabola(inputfilename='parabola.W=500.H=200.MAXD=8.SP=0.99.39.png')
    ##find_circles(inputfilename='cubic.W=500.H=200.MAXD=8.SP=0.99.26.png')
    #works fine for cubic
    #not well for parabola
    #run recursively for cubic - see if it generates 2 sensible circles




    # you were here
    #     Find a way to superimpose the results
    #     Find a way to capture the results in a JSON that can be viewed later on 
    #         probably superimposition images in a sub-folder, keep it simple, top level JSON

    #     RansacCircleInfo
    #         Add property 'projected_points'
    #         Add property 'arc_length'
    #         Add property 'arc_fraction'

    # result0 and result1 appear to have captured the circles on the cubic curve
    # You have the cirlces
    # Now get the lines
    # Eliminate the portions of the circles which have lesser density
    # How to estimate density? N * median gap
    # Project points on Cirlce
    # Try joining the lines and circles in a MC fashion, find the best candidate, longest candidate
