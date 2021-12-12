import itertools


#
#   Demo of how to calll a function with all possible combination of parameters for a function
#   Every parameter has a list of candidate values
#   Using itertools.product(listofcandidates1,listofcandidates2,listofcandidates3)
#
#

counter=0


class Model():
    """a demo class."""
    def __init__(self):
        self.__counter=0
        pass
    def increment(self):
        self.__counter=self.__counter+1
    
    @property
    def counter(self):
        """The counter property."""
        return self.__counter
    

def some_function(x1:int, x2:int, x3:int,x4:int, model:Model):
    global counter
    counter=counter+1
    model.increment()
    print(f"x1={x1} x2={x2} x3={x3},x4={x4} counter={counter}, model_counter={model.counter}");

x1_params=[1,2,3]
x2_params=[10,20,30,40]
x3_params=[100,200]
x4_params=[111]
print("Testing itertools")
rootmodel=Model()
print(f"Initial value of counter={rootmodel.counter}")

for xs in itertools.product(x1_params, x2_params, x3_params,x4_params):
    x1=xs[0]
    x2=xs[1]
    x3=xs[2]
    x4=xs[3]
    some_function(x1,x2,x3,x4,rootmodel)


print(f"Completed iteration, model counter={rootmodel.counter}")
