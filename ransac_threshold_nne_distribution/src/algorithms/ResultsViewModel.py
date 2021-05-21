from typing import List
from data.InputRow import InputRow
from data.OutputRow import OutputRow

class ResultsViewModel(object):
    """Holds all the inputs data and results data and provides methods to emti these records."""
    def __init__(self,inputrows:List[InputRow], outputrows:List[OutputRow]):
        self.__inputrows=inputrows
        self.__outputrows=outputrows

    @property
    def inputrows(self):
        """The inputrows property."""
        return self.__inputrows
        
    @property
    def outputrows(self):
        """The outputrows property."""
        return self.__outputrows

    def get_saltpepperratios(self)->List[float]:
       unique_salt_pepper=set(map(lambda x: x.salt_pepper, self.inputrows))
       return unique_salt_pepper

    def get_inputrows_with_salt_pepper(self,salt_pepper_ratio:float):
        results=filter(lambda x: x.salt_pepper == salt_pepper_ratio, self.inputrows)
        return list(results)

    def get_results_from_inputrow(self,inputrow:InputRow)->List[OutputRow]:
        results=filter(lambda x: x.imagefile == inputrow.imagefile, self.outputrows)
        return list(results)
