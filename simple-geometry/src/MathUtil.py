import math

class MathUtil():
    """Utility methods"""
    def __init__(self):
        pass

    #
    #Returns the math.atan2 value given (y,x) but eliminating the negative values by shifting from 0 to 2*pi
    #
    @classmethod
    def atan2_0to2pi(cls, y:float,x:float):
        atan=math.atan2(y,x)
        if (atan > 0):
            return atan
        else:
            return (2*math.pi + atan)

