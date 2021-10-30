import sys
from typing import List
import numpy as np
import os
from numpy.lib.function_base import diff
import skimage
import skimage.io
from skimage.measure import CircleModel, ransac
from ransacalgorithm import RansacCircleInfo
from ransacalgorithm import RansacCircleFinder
from ransacalgorithm import RansacLineInfo 
from ransacalgorithm import LineFinder
import simplegeometry as sg
from RootModel import RootModel
from OutputGenerator import *
import statistics
from sklearn.cluster import DBSCAN
from ransacalgorithm import CircleClusterCreator


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
    print(f"Image was read, width={width}   height={height} count of black pixels={len(all_black_points)}  total pixels={width*height}")
    model.black_pixels=all_black_points
    model.image__width=width
    model.image_height=height

def find_circles(model:RootModel):
    circle_results:List[RansacCircleInfo]=[]
    for ransac_threshold_factor in model.RANSAC_THRESHOLD_FACTORS:
        finder=RansacCircleFinder(pixels=model.black_pixels,width=model.image_width,height=model.image_height, max_models=model.MAX_CIRCLES , nnd_threshold_factor=ransac_threshold_factor , max_ransac_trials=model.MAX_RANSAC_TRIALS)
        circles= finder.find()
        circle_results.extend(circles)
    model.ransac_circles=circle_results
    pass

def find_circle_clusters(model:RootModel):
    cluster_creator=CircleClusterCreator()
    clustered_circles=cluster_creator.create_clusters(ransaccircles=model.ransac_circles , dbscan_epsilon_thresholds=model.DBSCAN_EPISOLON_THRESHOLD_FACTOR ,dbscan_min_pts=model.DBSCAN_MINPOINTS, min_allowedinliers_factor=model.MIN_INLIERS_FACTOR_AFTER_CLUSTERING)
    model.clustered_circles=clustered_circles
    print(f"Found a total of {len(model.clustered_circles)} circles from {len(model.ransac_circles)} ransac circles")


def process_file(filename:str):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path=os.path.join(folder_script,"data/",filename)

    model=RootModel()
    model.filename=absolute_path

    fullpathtoscript=os.path.realpath(__file__)
    model.output_folder=os.path.join(os.path.dirname(fullpathtoscript),"out/")

    read_image(model)

    #temp commenting 
    find_circles(model) 
    find_circle_clusters(model)
    OutputGenerator.plot_clustered_circles_with_projections(model) 
    
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
    #process_file(filename='parabola.W=500.H=200.MAXD=8.SP=0.99.39.png')
    #process_file(filename='parabola.small.png')
    #process_file(filename='parabola.narrow.png')
    #process_file(filename='parabola.patch1.png')
