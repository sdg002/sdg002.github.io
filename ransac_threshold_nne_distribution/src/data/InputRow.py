

from typing import List
import csv


class InputRow(object):
    """Represents a row in the CSV file which has input images."""
    def __init__(self,row_dict):
        self.__impagefile=row_dict["imagefile"]
        self.__salt_pepper=float(row_dict["salt_pepper"])
        self.__line_count=int(row_dict["line_count"])
    
    @property
    def imagefile(self):
        """The name of the image file used as an input to the algorithm"""
        return self.__impagefile

    @property
    def salt_pepper(self):
        """
        The salt pepper ration in the input image 
        """
        return self.__salt_pepper

    @property
    def line_count(self):
        """Count of expected lines in the input image """
        return self.__line_count

    def __repr__(self):
        return f'imagefile={self.__impagefile} , salt_pepper={self.__salt_pepper}'

'''
    Parses the specified file and converts all lines into objects
'''
def read_input_rows_from_file(filename:str)->List[InputRow]:
    input_file=csv.DictReader(open(filename))
    results=[]
    for row_dict in input_file:
        input_row=InputRow(row_dict)
        results.append(input_row)
    return results