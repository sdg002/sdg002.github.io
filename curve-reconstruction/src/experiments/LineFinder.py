from RansacLineInfo import RansacLineInfo
import numpy as np
from skimage.measure import LineModelND, ransac
from typing import List
from sklearn.neighbors import KDTree
import statistics


class LineFinder(object):
    """Sequentially finds line from the given points using the RANSAC algorithm"""
    def __init__(self, pixels:np.ndarray,width:float,height:float,max_models:int,nnd_threshold_factor:float):
        self.__width=width
        self.__height=height
        self.__all_black_points=pixels
        self.__max_models_to_find=max_models
        self.__min_inliers_allowed=3 # A line is selected only if it has these many inliers
        self.__min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to
        self.__mean_nne_threshold_factor=nnd_threshold_factor #This will be multiplied by the mean nearest neighbour distance. 0.5, 0.25 are good values
        self.__MAX_RANSAC_TRIALS=1000 #total no of samples to draw

    '''
    Use the mean nearest neighbour distance to arrive at the RANSAC threshold
    The function returns a tuple (mean_nearest_neighbour_distance, ransac_threshold)
    '''  
    def determine_ransac_threshold(self,points:np.ndarray)->float:
        tree = KDTree(points)
        nearest_dist, nearest_ind = tree.query(points, k=2)  # k=2 nearest neighbors where k1 = identity
        mean_distances_current_iterations=list(nearest_dist[0:,1:].flatten())
        mean=statistics.mean(mean_distances_current_iterations)
        ransac_thresold= mean * self.__mean_nne_threshold_factor
        return (mean,ransac_thresold)

    def find(self)->List[RansacLineInfo]:
        line_results:List[RansacLineInfo]=[]
        starting_points=self.__all_black_points
        for index in range(0,self.__max_models_to_find):
            if (len(starting_points) <= self.__min_samples):
                print("No more points available. Terminating search for RANSAC")
                break
            (mean_nnd,ransac_threshold)=self.determine_ransac_threshold(starting_points)
            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_line(starting_points,max_distance=ransac_threshold)
            if (len(inlier_points) < self.__min_inliers_allowed):
                print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self.__min_inliers_allowed))
                break
            starting_points=inliers_removed_from_starting
            ransac_model=RansacLineInfo(inlier_points,model)
            ransac_model.mean_nnd=mean_nnd
            ransac_model.ransac_threshold=ransac_threshold
            line_results.append(ransac_model)
            print(f"\tFound RANSAC line with {len(ransac_model.inliers)} inliers, line number {index},mean nnnd={mean_nnd} ,nnd_threshold={self.__mean_nne_threshold_factor},ransac_threshold={ransac_threshold},line info:{ransac_model}" )
        return line_results
        
    def __extract_first_ransac_line(self,data_points, max_distance:int):
        """
        Accepts a numpy array with shape N,2  N points, with coordinates x=[0],y=[1]
        Returns 
            A numpy array with shape (N,2), these are the inliers of the just discovered ransac line
            All data points with the inliers removed
            The model line
        """
        model_robust, inliers = ransac(data_points, LineModelND, min_samples=self.__min_samples,residual_threshold=max_distance, max_trials=self.__MAX_RANSAC_TRIALS)
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
