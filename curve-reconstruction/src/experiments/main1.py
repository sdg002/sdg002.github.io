from typing import List
import numpy as np
import os
import skimage
import skimage.io
from skimage.measure import CircleModel, ransac
from CircleFinder import CircleFinder
from RansacCircleInfo import RansacCircleInfo


max_distance=2 #8,4 #use NNE as an estimate
max_circles=10 #how many models to find

'''
    Plots the tuple of points
'''
def superimpose_points(points:List[tuple],width:float, height:float):
    new_image=np.full([height,width,3],255,dtype='int')
    colors=[(0,255,0),(255,255,0),(0,0,255)]
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

def find_circles(inputfilename:str):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path=os.path.join(folder_script,"data/",inputfilename)
    print(f"Inside parabola {absolute_path}")
    all_black_points,width,height=read_black_pixels(absolute_path)
    print("Found %d pixels in the file %s" % (len(all_black_points),inputfilename))

    
    circle_results:List[RansacCircleInfo]=[]

    finder=CircleFinder(pixels=all_black_points,width=width,height=height, max_models=max_circles,ransac_threshold=max_distance )
    circle_results:List[RansacCircleInfo]
    circle_results = finder.find()

    print(f"Total no of circles found={len(circle_results)}")

    #
    '''
    you were here
        Find a way to superimpose the results
        Find a way to capture the results in a JSON that can be viewed later on 
            probably superimposition images in a sub-folder, keep it simple, top level JSON

        RansacCircleInfo
            Add property 'projected_points'
            Add property 'arc_length'
            Add property 'arc_fraction'
    '''
    pass


if (__name__ =="__main__"):
    print("Inside main")
    #process_parabola(inputfilename='parabola.W=500.H=200.MAXD=8.SP=0.99.39.png')
    find_circles(inputfilename='cubic.W=500.H=200.MAXD=8.SP=0.99.26.png')
    #works fine for cubic
    #not well for parabola
    #run recursively for cubic - see if it generates 2 sensible circles

