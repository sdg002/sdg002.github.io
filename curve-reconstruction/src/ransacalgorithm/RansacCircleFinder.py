import numpy as np
from .RansacCircleInfo import RansacCircleInfo
from skimage.measure import CircleModel, ransac
from typing import List
from sklearn.neighbors import KDTree
import statistics

class RansacCircleFinder(object):
    """Sequentially finds circles from the given points"""
    def __init__(self, pixels:np.ndarray,width:float,height:float,max_models:int,nnd_threshold_factor:float,max_ransac_trials:float):
        self.__width=width
        self.__height=height
        self.__all_black_points=pixels
        self.__max_models_to_find=max_models
        self.__min_inliers_allowed=3 # A circle is selected only if it has these many inliers
        self.__min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to
        self.__mean_nne_threshold_factor=nnd_threshold_factor #This will be multiplied by the mean nearest neighbour distance. 0.5, 0.25 are good values
        self.__max_ransac_trials=max_ransac_trials

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
        pass

    def find(self)->List[RansacCircleInfo]:
        print(f"Going to run RANSAC with MAX_RANSAC_TRIALS={self.__max_ransac_trials} , MAX MODELS={self.__max_models_to_find}")
        circle_results:List[RansacCircleInfo]=[]
        starting_points=self.__all_black_points
        for index in range(0,self.__max_models_to_find):
            if (len(starting_points) <= self.__min_samples):
                print("No more points available. Terminating search for RANSAC")
                break
            (mean_nnd,ransac_threshold)=self.determine_ransac_threshold(starting_points)
            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_circle(starting_points,max_distance=ransac_threshold)
            if (len(inlier_points) < self.__min_inliers_allowed):
                print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self.__min_inliers_allowed))
                break
            starting_points=inliers_removed_from_starting
            ransac_model=RansacCircleInfo(inlier_points,model)
            ransac_model.mean_nnd=mean_nnd
            ransac_model.ransac_threshold=ransac_threshold
            circle_results.append(ransac_model)
            print(f"Found a RANSAC circle with center {index}, {ransac_model.center} and radius={ransac_model.radius}, inliers={len(inlier_points)} , ransac_threshold={ransac_threshold}, mean nnnd={mean_nnd} threshold_factory={self.__mean_nne_threshold_factor}")
        print(f"Total ransac circles found:{len(circle_results)}")
        return circle_results
    
    def __extract_first_ransac_circle(self,data_points, max_distance:int):
        """
        Accepts a numpy array with shape N,2  N points, with coordinates x=[0],y=[1]
        Returns 
            A numpy array with shape (N,2), these are the inliers of the just discovered ransac line
            All data points with the inliers removed
            The model line
        """
            
        model_robust, inliers = ransac(data_points, CircleModel, min_samples=self.__min_samples,residual_threshold=max_distance, max_trials=self.__max_ransac_trials)
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
