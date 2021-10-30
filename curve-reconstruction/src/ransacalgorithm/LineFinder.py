from src.Point import Point
from .RansacLineInfo import RansacLineInfo
import numpy as np
from skimage.measure import LineModelND, ransac
from typing import List
from sklearn.neighbors import KDTree
import statistics
import simplegeometry as sg


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
        self.compute_max_ransac_trials()

    def compute_max_ransac_trials(self):
        count_of_pixels=len(self.__all_black_points)
        self.__MAX_RANSAC_TRIALS=int(count_of_pixels*(count_of_pixels-1)/2)
        pass

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
        print(f"Starting RANSAC line determination using max trials={self.__MAX_RANSAC_TRIALS}")
        line_results:List[RansacLineInfo]=[]
        starting_points=self.__all_black_points
        all_inliers=[]
        for index in range(0,self.__max_models_to_find):
            if (len(starting_points) <= self.__min_samples):
                print("No more points available. Terminating search for RANSAC")
                break
            (mean_nnd,ransac_threshold)=self.determine_ransac_threshold(starting_points)
            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_line(starting_points,max_distance=ransac_threshold)
            if (len(inlier_points) < self.__min_inliers_allowed):
                print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self.__min_inliers_allowed))
                break
            all_inliers.extend(inlier_points)
            #
            #New idea on 25 Oct - Inliers that have been removed could be a legitimate member of a subsequently discovered line
            #Consider the scenario of a 2 strong lines. The intersecting point belongs to both the lines.
            #Problem - The second RANSAC line is penalized because the point of intersection has already been added to the first RANSAC line
            #Accumulate all inlier points in a List
            #For every new line that is discovered, check the accumulator to see if any point can be a member
            #If yes, then add this point to the inlier_points
            #
            starting_points=inliers_removed_from_starting

            line_equation=self.create_linemodel_from_scikit_model(model)
            all_possible_inliers=self.find_inliers_from_all_points(line_equation=line_equation, threshold=ransac_threshold)
            ransac_model=RansacLineInfo(all_possible_inliers,model)
            ransac_model.mean_nnd=mean_nnd
            ransac_model.ransac_threshold=ransac_threshold
            line_results.append(ransac_model)
            print(f"\tFound RANSAC line with {len(ransac_model.inliers)} inliers, line number {index},mean nnnd={mean_nnd} ,nnd_threshold={self.__mean_nne_threshold_factor},ransac_threshold={ransac_threshold},line info:{ransac_model}" )
        return line_results

    def find_inliers_from_all_points(self,line_equation:sg.LineModel, threshold:float)->np.ndarray:
        resulting_inlier_tuples=[]
        for black_pixel in self.__all_black_points:
            black_point=Point(black_pixel[0],black_pixel[1])
            perp_distance=line_equation.compute_distance(point=black_point)
            if (perp_distance > threshold):
                continue
            resulting_inlier_tuples.append((black_point.X,black_point.Y))
        pass
        arr=np.array(resulting_inlier_tuples)
        return arr

    def create_linemodel_from_scikit_model(self,scikitmodel)->sg.LineModel:
        origin=sg.Point(scikitmodel.params[0][0],scikitmodel.params[0][1])
        unitvector=sg.Point(scikitmodel.params[1][0],scikitmodel.params[1][1])

        first_point=origin
        second_point=sg.Point(first_point.X + unitvector.X*10, first_point.Y+unitvector.Y*10)
        lineequation=sg.LineModel.create_line_from_2points(first_point.X,first_point.Y, second_point.X, second_point.Y)

        return lineequation

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

    @property
    def max_ransac_trials(self):
        """The max_ransac_trials property."""
        return self.__MAX_RANSAC_TRIALS

    @max_ransac_trials.setter
    def max_ransac_trials(self, value):
        self.__MAX_RANSAC_TRIALS = value
