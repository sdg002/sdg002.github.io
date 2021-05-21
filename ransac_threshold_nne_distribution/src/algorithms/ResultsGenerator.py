from typing import List
from algorithms.ResultsViewModel import ResultsViewModel
from data.InputRow import InputRow
from data.OutputRow import OutputRow


class ResultsGenerator(object):
    """Generates a HTML file from an instance of the results view model."""
    def __init__(self, viewmodel:ResultsViewModel,filename:str):
        self.__viewmodel=viewmodel
        self.__filename=filename

    @property
    def viewmodel(self):
        """Returns the view model"""
        return self.__viewmodel

    @property
    def filename(self):
        """The path to the HTML file."""
        return self.__filename

    def generate_report(self):        
        salt_pepper_ratios:List[float]=self.viewmodel.get_saltpepperratios()
        for salt_pepper in salt_pepper_ratios:
            input_rows_with_salt_pepper:List[input_row]=self.viewmodel.get_inputrows_with_salt_pepper(salt_pepper_ratio=salt_pepper)
            print(f"\tProcessing salt_pepper={salt_pepper}, found {len(input_rows_with_salt_pepper)} input files")
            for input_row in input_rows_with_salt_pepper:
                matching_result_rows=self.viewmodel.get_results_from_inputrow(input_row)
                print(f"\t\tProcessing input image:{input_row.imagefile}...result files={len(matching_result_rows)}...max_distance={input_row.max_distance}")
                for result_file in matching_result_rows:
                    print(f"\t\t\t{result_file.outputimagefile}...tfac={result_file.thresholdfactor}...threshold={result_file.actualthreshold}")

        pass