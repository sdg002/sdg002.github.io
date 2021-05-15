
from typing import List
from .OutputRow import OutputRow


class CsvHelper(object):
    """CsvHelper is a class that facilitates writing and reading  to/from CSV files"""
    def __init__(self):
        super(CsvHelper, self).__init__()

    @staticmethod
    def write_results_to_csv(filename:str, output_rows:List[OutputRow]):
        pass        