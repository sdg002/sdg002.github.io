import datetime
import math
import numpy as np
import random
import statistics


#
#Original problem - Pick 2 points . Produces 0.5251
#
def compute_expected_distance_between_2points_n_trials(max_trials:int):
    seed=datetime.datetime.now().second
    random.seed(seed)
    distances=[]
    for i in range(0,max_trials):
        x1=random.random()
        y1=random.random()
        x2=random.random()
        y2=random.random()

        distance=math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
        distances.append(distance)
    return statistics.mean(distances)

iterations=100000
average=compute_expected_distance_between_2points_n_trials(10000)
print("Average=%f after iterations=%d" % (average,iterations))
