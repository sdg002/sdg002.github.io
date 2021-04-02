#
#We will select N randmon points in an unit square and then compute the mean nearest-neighbour distance
#We will then plot the mean NN distance vs N
#
#

from typing import List
import numpy as np
import os
import random
from numpy.core.fromnumeric import mean
from skimage import io
from sklearn.neighbors import KDTree
import math
import statistics
import matplotlib.pyplot as plt


class NearestNeighbourDistance(object):
    """docstring for NearestNeighbourDistance."""
    def __init__(self, squaresize:float,point_count:int, iterations:int):
        super(NearestNeighbourDistance, self).__init__()
        self.__squaresize=squaresize
        self.__point_count=point_count
        self.__iterations=iterations
    
    def compute_mean(self):
        means_across_iterations=[]
        for iteration in range(0,self.__iterations):
            random_array=np.random.random((self.__point_count,2))
            tree = KDTree(random_array)
            nearest_dist, nearest_ind = tree.query(random_array, k=2)  # k=2 nearest neighbors where k1 = identity
            mean_distances_current_iterations=list(nearest_dist[0:,1:].flatten())
            mean=statistics.mean(mean_distances_current_iterations)
            means_across_iterations.append(mean)
        return statistics.mean(means_across_iterations)

def plot(points_count:List,  means:List):
    plt.title("Outcome of Monte Carlo simulation to calculate mean nearest neighbour distance")
    plt.ylim([0, 0.5])
    plt.xlabel("Number of points (N)")
    plt.ylabel("Mean nearest neighbour distance")
    plt.scatter(points_count,means, marker='.', s=5)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    plt.show()
    pass


lst_pointcount=[]
lst_meandistance=[]
iterations=50
max_points=2000
for point_count in range(2,max_points):
    nn=NearestNeighbourDistance(squaresize=1,point_count=point_count,iterations=iterations)
    mean_distance=nn.compute_mean()
    lst_pointcount.append(point_count)
    lst_meandistance.append(mean_distance)
    print("Computed mean NN distance of %f for %d points" % (mean_distance,point_count))

plot(lst_pointcount, lst_meandistance)
