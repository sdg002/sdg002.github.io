import numpy as np
from RansacLineInfo import  RansacLineInfo
import skimage.io
from typing import List
from sklearn.neighbors import KDTree
import statistics
from skimage.measure import LineModelND, ransac

'''
RANSAC parameter - The minimum number of data points to fit a model to.
'''
MIN_SAMPLES=3  #how many points in a single sampling
MAX_TRIALS_FACTOR=0.5 #influences how many randmon samples to pick
MIN_ALLOWABLE_THRESHOLD=1.0  #if the nearest neighbour statistic is zero then this should be used for the RANSAC threshold

class SequentialRansac(object):
    """
    Implements sequential RANSAC on the specified image file
    https://scikit-image.org/docs/stable/auto_examples/transform/plot_ransac.html
    """
    def __init__(self, path:str,max_lines_to_find:int,ransac_threshold_factor:float):
        super(SequentialRansac, self).__init__()
        self._path = path
        self._max_lines=max_lines_to_find
        self._image_array=None
        self._ransac_threshold_factor=ransac_threshold_factor
        self._min_inliers_allowed=3
        self._black_points=None
        
    @property
    def black_points(self):
        """Returns a numpy array of all the  black_points in the image."""
        if (self._black_points is not None):
            return self._black_points

        np_image=self.image_array
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
        self._black_points=np_data_points
        return self._black_points

        return self._black_points

    @property
    def image_array(self):
        """Gets the Numpy image_array."""
        if (self._image_array is None):
            self._image_array = skimage.io.imread(self._path)
        return self._image_array

    @property
    def width(self):
        """The width property."""
        return self.image_array.shape[1]

    @property
    def height(self):
        """The height property."""
        return self.image_array.shape[0]

    def __calculate_ransac_threshold_from_nearest_neighbour_estimate(self, points:np.ndarray)->float:
        tree = KDTree(points)
        nearest_dist, nearest_ind = tree.query(points, k=2)
        nne_distances=list(nearest_dist[0:,1:].flatten())
        mean=statistics.mean(nne_distances)
        median=statistics.median(nne_distances)
        stdev=statistics.stdev(nne_distances)
        distance_from_line=median 
        print("\tMean=%f, Median=%f, Stddev=%f calculated " % (mean,median,stdev))
        if (distance_from_line == 0.0):
            return MIN_ALLOWABLE_THRESHOLD
        else:
            return distance_from_line

    def __extract_first_ransac_line(self,data_points:List, ransac_threshold:int, max_trials:int):
        model_robust, inliers = ransac(data_points, LineModelND, min_samples=MIN_SAMPLES,residual_threshold=ransac_threshold, max_trials=max_trials)
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

    def run_sequential_ransac(self)->List[RansacLineInfo]:
        results:List[RansacLineInfo]=[]
        width=self.width
        height=self.height

        starting_points=self.black_points
        for index in range(0,self._max_lines):
            
            nearest_neighbour_estimate=self.__calculate_ransac_threshold_from_nearest_neighbour_estimate(starting_points) 
            ransac_threshold=nearest_neighbour_estimate*self._ransac_threshold_factor

            number_of_samples_to_draw=(int(MAX_TRIALS_FACTOR* len(starting_points)))**2

            print("\tAttempting RANSAC using threshold factor=%f, nearest neighbour estimate=%f ,calculated threshold=%f, black pixel count=%d, max_samples=%d," % (self._ransac_threshold_factor, nearest_neighbour_estimate,ransac_threshold,len(starting_points), number_of_samples_to_draw))
            min_needed_points=MIN_SAMPLES*2
            if (len(starting_points) <= min_needed_points):
                print("No more points available. Terminating search for RANSAC. Available points=%d Cutt off points count=%d" % (len(starting_points),min_needed_points))
                break

            inlier_points,inliers_removed_from_starting,model=self.__extract_first_ransac_line(data_points=starting_points,ransac_threshold=ransac_threshold, max_trials=number_of_samples_to_draw) 
            if (len(inlier_points) < self._min_inliers_allowed):
                print("\tNot sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),self._min_inliers_allowed))
                break
            print("\tFound RANSAC line with %d inliers, line number %d" % (len(inlier_points),index))
            starting_points=inliers_removed_from_starting
            results.append(RansacLineInfo(inlier_points,model))        
        
        return results

