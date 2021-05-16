
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

    def write_input_rows_to_csv(filename:str,input_rows:List[InputRow]):
        with open(filename, mode='w', newline='') as csv_file:
            testimage_writer=csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            testimage_writer.writerow(["imagefile","salt_pepper","max_distance","line_count","total_pixels","black_pixels"])            
            for row in input_rows:
                testimage_writer.writerow([row.imagefile,row.salt_pepper,row.max_distance,row.line_count,row.total_pixels,row.black_pixels])
        pass

    """Read all input images from the specified CSV file and creates a data object for every line"""
    @staticmethod
    def read_input_rows_from_csv(filename:str)->List[InputRow]:
        input_file=csv.DictReader(open(filename))
        results=[]
        for row_dict in input_file:
            input_row=InputRow()
            input_row.imagefile=row_dict["imagefile"]
            input_row.salt_pepper=float(row_dict["salt_pepper"])
            input_row.line_count=int(row_dict["line_count"])
            input_row.total_pixels=int(row_dict["total_pixels"])
            input_row.black_pixels=int(row_dict["black_pixels"])
            input_row.max_distance=int(row_dict["max_distance"])

            results.append(input_row)
        return results

    @staticmethod
    def read_result_rows_from_csv(filename:str)->List[OutputRow]:
        output_file=csv.DictReader(open(filename))
        results=[]
        for row_dict in output_file:
            output_row=OutputRow()
            output_row.imagefile=row_dict["inputimagefile"]
            output_row.outputimagefile=row_dict["outputimagefile"]
            output_row.thresholdfactor=row_dict["thresholdfactor"]
            output_row.actualthreshold=row_dict["threshold"]
            results.append(output_row)
        return results
        