from cmath import pi
from itertools import count
import math

from typing import List
import matplotlib.pyplot as plt
import numpy as np



def calculate_points_on_circle(radius:float, x:float, y:float, num_sides:int)->List:
    thetas=np.linspace(start=0.0,stop=2*math.pi,num=num_sides+1, endpoint=True)
    x_values=np.cos(thetas)*radius
    y_values=np.sin(thetas)*radius
    
    #
    # theta=2*math.pi/num_sides
    # degrees_per_radians=180/math.pi
    # angular_position=0
    # for i in range(0,num_sides):
    #     angular_position=angular_position+theta
    #     x=math.cos(angular_position)*radius
    #     y=math.sin(angular_position)*radius
    #     print(f"index={i} angle={angular_position*degrees_per_radians} x,y={x},{y}")
    # pass
    return (x_values,y_values)

def get_chord_start_end(start_theta:float, end_theta:float, radius:float,center_x:float, center_y:float):
    chord_start_x = math.cos(start_theta)*radius
    chord_start_y = math.sin(start_theta)*radius

    chord_end_x = math.cos(end_theta)*radius
    chord_end_y = math.sin(end_theta)*radius

    vec_x=chord_end_x-chord_start_x
    vec_y=chord_end_y-chord_start_y
    chord_vector=np.array([vec_x, vec_y])

    t=np.linspace(start=0.0,stop=1.0, num=100)

    func_x=lambda tx:  chord_start_x + tx*chord_vector[0]
    vfunc_x=np.vectorize(func_x)
    new_x=vfunc_x(t)

    func_y=lambda ty:  chord_start_y + ty*chord_vector[1]
    vfunc_y=np.vectorize(func_y)
    new_y=vfunc_y(t)

    return (new_x,new_y)

def plot_circle(radius:float,center_x:float,center_y:float):
    theta = np.linspace(0, 2*np.pi, 100)
    x = radius*np.cos(theta)+center_x
    y = radius*np.sin(theta)+center_y
    plt.plot(x,y)

def plot():
    print("try plotting")

    r= 2
    num_sides=16
    plot_circle(radius=r,center_x=0, center_y=0)

    thetas=np.linspace(start=0.0,stop=2*math.pi,num=num_sides+1, endpoint=True)

    
    for index in range(0,num_sides):
        if index == num_sides-1:
            start_theta=thetas[0]
            end_theta=thetas[num_sides-1]  
        else:
            start_theta=thetas[index]
            end_theta=thetas[index+1]  
        chord_x,chord_y=get_chord_start_end(start_theta=start_theta, end_theta=end_theta, radius=r,center_x=0, center_y=0)  
        plt.plot(chord_x,chord_y)
    #this works
    # chord_x,chord_y=get_chord_start_end(start_theta=0, end_theta=math.pi/3, radius=r,center_x=0, center_y=0)
    # plt.plot(chord_x,chord_y)
    plt.axis('equal')
    plt.show()    
    pass

def main():
    print("do something")
    #polygon_points:List=calculate_points_on_circle(radius=1.0, x=0.0, y=0.0,num_sides=4)
    plot()

if __name__ == "__main__":
    #main()
    plot()
