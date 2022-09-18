from cmath import pi
import math
import sys

def calculate_number_of_polygon_sides(iteration:int):
    return 4*math.pow(2, iteration)

def calculate_polygon_side(iteration:int):
    if iteration == 0:
        return math.sqrt(2)
    
    r=1    
    ad=calculate_polygon_side(iteration=iteration-1)/2
    cd_square=(r*r) - (ad*ad)
    dc1=r-math.sqrt(cd_square)
    s_n =  math.sqrt((dc1*dc1) + (ad*ad))
    return s_n

def calculate_pie(iterations:int):
    num_of_sides=calculate_number_of_polygon_sides(iteration=iterations)
    print(f"Number of sides ={num_of_sides}")
    polygon_side_length=calculate_polygon_side(iteration=iterations)
    print(f"Polygon side length ={polygon_side_length}")
    perimeter=num_of_sides*polygon_side_length
    print(f"Perimenter ={perimeter}")
    radius=1
    pie=perimeter/(2*radius)
    return pie


if __name__ == "__main__":
    iterations=int(sys.argv[1])
    print(f"Number of iterations ={iterations}")
    pie=calculate_pie(iterations=iterations)
    print(f"Iterations={iterations}     pie={pie}")
