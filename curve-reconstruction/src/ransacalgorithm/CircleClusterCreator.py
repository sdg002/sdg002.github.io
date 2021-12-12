from typing import List
#from RootModel import RootModel
from .RansacCircleInfo import RansacCircleInfo
import itertools
import statistics
import numpy as np
from sklearn.cluster import DBSCAN

class CircleClusterCreator(object):
    """Splits a Ransac Circle into cluster of circles depending on angular spacing."""
    def __init__(self):
        pass

    def find_consecutive_differences(self,values:List[float]):
        results=[]
        for index in range(0,len(values)-1):
            diff=values[index+1]-values[index]
            results.append(diff)
        return results

    def create_single_cluster(self,ransaccircle:RansacCircleInfo,dbscan_epsilon_threshold:float, dbscan_minpt:float, min_permitted_inlier_factor:float)->List[RansacCircleInfo]:
        clustered_circles=[]

        projected_inliers=ransaccircle.projected_inliers
        thetas=list(map(lambda x: x[2], projected_inliers))
        diffs=self.find_consecutive_differences(thetas)
        median=statistics.median(diffs)
        epsilon=median*dbscan_epsilon_threshold
        new_datapoints_2d=list(map(lambda x: [x], thetas))
        data_points=np.array(new_datapoints_2d)
        dbs=DBSCAN(eps=epsilon, min_samples=dbscan_minpt)
        dbs.fit(new_datapoints_2d)

        count_of_outliers=len(list(filter(lambda  l: l==-1, dbs.labels_)))
        set_of_clusters=set(filter(lambda  l: l!=-1, dbs.labels_))
        print(f"Found {len(set_of_clusters)} clusters in RANSAC circle , outliers:{count_of_outliers}, initial points={len(thetas)}")
        permissible_lower_limit_of_points=min_permitted_inlier_factor* len(ransaccircle.inlier_points) 
        clusterable_point_indices=np.where(dbs.labels_ != -1)
        for cluster_index in set_of_clusters:
            cluster_point_indices=np.where(dbs.labels_ == cluster_index)
            new_inliers=projected_inliers[list(cluster_point_indices[0])]
            new_inliers_notheta=new_inliers[:,0:2]
            if (len(new_inliers) < permissible_lower_limit_of_points):
                print(f"\tThe count of inliers:{len(new_inliers)} is less than the threshold:{permissible_lower_limit_of_points}. Skipping circle")
                continue
            new_circle = RansacCircleInfo(new_inliers_notheta,ransaccircle.model)
            print(f"\tGoing to create a new circle at index {cluster_index}, points={len(new_inliers)}, median arc separation={new_circle.radius * median}, original radius={ransaccircle.radius} new radius={new_circle.radius} original center={ransaccircle.center} newcenter={new_circle.center}")
            new_circle.ransac_threshold=ransaccircle.ransac_threshold
            new_circle.mean_nnd=ransaccircle.mean_nnd
            new_circle.dbscan_epsilon=epsilon
            new_circle.dbscan_minpts=dbscan_minpt
            clustered_circles.append(new_circle)

        return clustered_circles

    def create_clusters(self,ransaccircles:List[RansacCircleInfo], dbscan_epsilon_thresholds:List[float],dbscan_min_pts:List[float], min_allowedinliers_factor:List[float])->List[RansacCircleInfo]:
        new_circles=[]
        for xs in itertools.product(ransaccircles,dbscan_epsilon_thresholds,dbscan_min_pts, min_allowedinliers_factor):
            circle  =xs[0]
            epsilon_threshold =xs[1]
            min_pt  =xs[2]
            min_permitted_inlier_factor=xs[3]
            clustered_circles=self.create_single_cluster(ransaccircle=circle,dbscan_epsilon_threshold= epsilon_threshold, dbscan_minpt= min_pt,min_permitted_inlier_factor=min_permitted_inlier_factor)
            new_circles.extend(clustered_circles)
        return new_circles
