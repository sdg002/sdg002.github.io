from typing import List
import numpy as np
import math
import matplotlib.pyplot as plt


def plot(points_count:List,  means:List):
    plt.title("Plot of simple mathematical model versus N")
    plt.ylim([0, 0.5])
    plt.scatter(points_count,means, marker='.', s=5)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    plt.show()
    pass

lst_pointcount=[]
lst_meandistance=[]
for point_count in range(2,2000):
    mean_distance=1/(math.sqrt(point_count)+1)
    lst_pointcount.append(point_count)
    lst_meandistance.append(mean_distance)
    print("Calculated NN distance using simple model with value %f for %d points" % (mean_distance,point_count))

plot(lst_pointcount, lst_meandistance)
