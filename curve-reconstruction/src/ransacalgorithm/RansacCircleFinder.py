import numpy as np
from .RansacCircleInfo import RansacCircleInfo
from skimage.measure import CircleModel, ransac
from typing import List
from sklearn.neighbors import KDTree
import statistics
import simplegeometry as sg
from .StoppingCriteria import StoppingCriteria
import math


class RansacCircleFinder(object):
    """Sequentially finds circles from the given points"""
    def __init__(self, pixels:np.ndarray,width:float,height:float,nnd_threshold_factor:float,max_ransac_trials:float):
        self.__width=width
        self.__height=height
        self.__all_black_points=pixels
        self.__min_inliers_allowed=3 # A circle is selected only if it has these many inliers
        self.__min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to
        self.__mean_nne_threshold_factor=nnd_threshold_factor #This will be multiplied by the mean nearest neighbour distance. 0.5, 0.25 are good values
        self.__max_ransac_trials=max_ransac_trials
        self.__stopping_criteria:StoppingCriteria=None
        self.__max_models_to_find=math.nan
        self.__counter=0
        self.__first_ransac_threshold=math.nan
        self.__current_ransac_threshold=math.nan
        self.__ransac_threshold_spike_factor=math.nan

    @property
    def stopping_criteria(self)->StoppingCriteria:
        """The stopping_criteria property."""
        return self.__stopping_criteria

    @stopping_criteria.setter
    def stopping_criteria(self, value)->StoppingCriteria:
        self.__stopping_criteria = value

    @property
    def max_models(self):
        """The total no of Lines to find. This is used for the stopping criteria"""
        return self.__max_models_to_find
    @max_models.setter
    def max_models(self, value):
        self.__max_models_to_find = value

    @property
    def ransac_threshold_spike_factor(self):
        """Used as a stopping criteria. When the ratio of the current ransac threshold to the original ransac threshold exceeds this value, the search is stopped"""
        return self.__ransac_threshold_spike_factor
    
    @ransac_threshold_spike_factor.setter
    def ransac_threshold_spike_factor(self, value):
        self.__ransac_threshold_spike_factor = value

    def validateparams(self):
        if (self.stopping_criteria == StoppingCriteria.RANSAC_THRESHOLD_SPIKE):
            if (math.isnan(self.ransac_threshold_spike_factor)):
                raise Exception("The property ransac threshold spike factor has not been set")
        elif (self.stopping_criteria == StoppingCriteria.MAX_OBJECTS):
            if (math.isnan(self.max_models)):
                raise Exception("The property max models has not been set")
        else:
            raise Exception(f"Invalid stopping criteria:{self.stopping_criteria}")

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
        self.validateparams()
        print(f"Going to run RANSAC with stopping criteria={self.stopping_criteria}")
        circle_results:List[RansacCircleInfo]=[]
        starting_points=self.__all_black_points
        while True:
            if (len(starting_points) <= self.__min_samples):
                print("No more points available. Terminating search for RANSAC")
                break
            (mean_nnd,self.__current_ransac_threshold)=self.determine_ransac_threshold(starting_points)
            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_circle(starting_points,max_distance=self.__current_ransac_threshold)
            if (self.__counter==0):
                self.__first_ransac_threshold=self.__current_ransac_threshold

            if (len(inlier_points) < self.__min_inliers_allowed):
                print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self.__min_inliers_allowed))
                break
            
            canstop=self.evaluate_ifcanstop()
            if (canstop):
                break
            
            starting_points=inliers_removed_from_starting
            
            circle_equation:sg.CircleModel
            circle_equation=self.create_circlemodel_from_scikit_model(scikitmodel=model)

            all_possible_inliers=self.find_inliers_from_all_points(circle_equation=circle_equation, threshold=self.__current_ransac_threshold)
            
            ransac_model=RansacCircleInfo(all_possible_inliers,model)
            ransac_model.mean_nnd=mean_nnd
            ransac_model.ransac_threshold=self.__current_ransac_threshold
            circle_results.append(ransac_model)
            print(f"Found a RANSAC circle with center {self.__counter}, {ransac_model.center} and radius={ransac_model.radius}, inliers={len(inlier_points)} , ransac_threshold={self.__current_ransac_threshold}, mean nnnd={mean_nnd} threshold_factory={self.__mean_nne_threshold_factor}")
            self.__counter+=1            
        print(f"Total ransac circles found:{len(circle_results)}")
        return circle_results
    
    def evaluate_ifcanstop(self):
        if (self.__stopping_criteria == StoppingCriteria.RANSAC_THRESHOLD_SPIKE):
            delta_threshold=self.__current_ransac_threshold-self.__first_ransac_threshold
            ratio=(self.__current_ransac_threshold/self.__first_ransac_threshold)
            return ratio>self.__ransac_threshold_spike_factor
        elif (self.__stopping_criteria == StoppingCriteria.MAX_OBJECTS):
            return (self.__counter >= self.__max_models_to_find)
        else:
            raise Exception(f"Unsupported stopping criteria:{self.__stopping_criteria}")

    def create_circlemodel_from_scikit_model(self,scikitmodel)->sg.CircleModel:
        c=sg.CircleModel(center_x=scikitmodel.params[0],center_y=scikitmodel.params[1],radius=scikitmodel.params[2])
        return c

    #
    #Iterate over all the data points , returns those points which are within threshold distance of the model circle circumfrence
    #
    def find_inliers_from_all_points(self,circle_equation:sg.CircleModel,threshold:float):
        resulting_inlier_tuples=[]
        center=sg.Point(circle_equation.X,circle_equation.Y)
        for black_pixel in self.__all_black_points:
            black_point=sg.Point(black_pixel[0],black_pixel[1])
            
            radial_distance=sg.Point.euclidean_distance(point1=black_point, point2=center)
            if (abs(radial_distance - circle_equation.R) > threshold):
                continue
            resulting_inlier_tuples.append((black_point.X,black_point.Y))
        arr=np.array(resulting_inlier_tuples)
        return arr

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
