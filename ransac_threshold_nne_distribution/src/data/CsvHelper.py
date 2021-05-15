
from data.InputRow import InputRow
from typing import List
from .OutputRow import OutputRow
import csv

class CsvHelper(object):
    """CsvHelper is a class that facilitates writing and reading  to/from CSV files"""
    def __init__(self):
        super(CsvHelper, self).__init__()

    """ Write all objects of test results in the specified array into a CSV format at the specified file"""
    @staticmethod
    def write_results_to_csv(filename:str, output_rows:List[OutputRow]):
        csvcolumns=["inputimagefile","outputimagefile","threshold","thresholdfactor"]
        with open(filename, mode='w', newline='') as csv_file:
            testimage_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            testimage_writer.writerow(csvcolumns)
            for output_row in output_rows:
                testimage_writer.writerow([output_row.imagefile,output_row.outputimagefile,output_row.actualthreshold,output_row.thresholdfactor])
        pass 

    """Read all input images from the specified CSV file and creates a data object for every line"""
    @staticmethod
    def read_input_rows_from_csv(filename:str)->List[InputRow]:
        input_file=csv.DictReader(open(filename))
        results=[]
        for row_dict in input_file:
            input_row=InputRow(row_dict)
            results.append(input_row)
        return results