import numpy as np
from RansacCircleInfo import RansacCircleInfo
from skimage.measure import CircleModel, ransac
from typing import List


class CircleFinder(object):
    """Sequentially finds circles from the given points"""
    def __init__(self, pixels:np.ndarray,width:float,height:float,max_models:int, ransac_threshold:float):
        self.__width=width
        self.__height=height
        self.__all_black_points=pixels
        self.__max_models_to_find=max_models
        self.__min_inliers_allowed=3 # A circle is selected only if it has these many inliers
        self.__min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to
        self.__ransac_threshold_distance =ransac_threshold #Chnage name of variable
        
    def find(self)->List[RansacCircleInfo]:
        circle_results:List[RansacCircleInfo]=[]
        starting_points=self.__all_black_points
        for index in range(0,self.__max_models_to_find):
            if (len(starting_points) <= self.__min_samples):
                print("No more points available. Terminating search for RANSAC")
                break
            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_circle(starting_points,max_distance=self.__ransac_threshold_distance)
            if (len(inlier_points) < self.__min_inliers_allowed):
                print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self.__min_inliers_allowed))
                break
            starting_points=inliers_removed_from_starting
            rascal_model=RansacCircleInfo(inlier_points,model)
            circle_results.append(rascal_model)
            print(f"Found a RANSAC circle with center {rascal_model.center} and radius={rascal_model.radius}")
        return circle_results
    
    def __extract_first_ransac_circle(self,data_points, max_distance:int):
        """
        Accepts a numpy array with shape N,2  N points, with coordinates x=[0],y=[1]
        Returns 
            A numpy array with shape (N,2), these are the inliers of the just discovered ransac line
            All data points with the inliers removed
            The model line
        """
            
        model_robust, inliers = ransac(data_points, CircleModel, min_samples=self.__min_samples,residual_threshold=max_distance, max_trials=1000)
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
