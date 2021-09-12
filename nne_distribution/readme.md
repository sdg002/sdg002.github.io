# Overview
This folder contains the supporting files for my Medium article [Surprising behaviour of the average nearest neighbour distance in a cluster of points](https://medium.com/mlearning-ai/surprising-behaviour-of-the-average-nearest-neighbour-distance-in-a-cluster-of-points-dce671b86c3b)

![Mean Nearest Neighbour Distance comparison of 2 approaches ](images/side_by_side_comparison.png)



# Source files
These are files under the **src** folder

## AverageDistanceBetween2Points.py
Demonstrates a Monte Carlo approach to detemine the average nearest neighbour distance between 2 randomly picked points in an unit square. This is a classical problem which has an elegant theoretical solution - but a very difficult one. The source code presents a very approach.

## AverageNND.py 
In this file we fill a square with progressively increasing number of random points and for every distribution we calculate the mean distance

## SimpleModelWithNPoints.py
In this file we implement the simple calculation of the formula to estimate the mean nearest neighbour distance and demonstrate the hyperbolic behaviour by plotting the results.
```
mean_distance=1/(math.sqrt(point_count)+1)
```

