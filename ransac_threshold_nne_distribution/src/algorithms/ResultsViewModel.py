from typing import List
from data.InputRow import InputRow
from data.OutputRow import OutputRow

class ResultsViewModel(object):
    """Holds all the inputs data and results data and provides methods to emti these records."""
    def __init__(self,inputrows:List[InputRow], outputrows:List[OutputRow],inputfolder:str, resultsfolder:str):
        self.__inputrows=inputrows
        self.__outputrows=outputrows
        self.__inputfolder=inputfolder
        self.__resultsfolder=resultsfolder

    @property
    def inputfolder(self):
        """The absolute folder which contains the input images"""
        return self.__inputfolder

    @property
    def resultsfolder(self):
        """The absolute folder which contains the result images"""
        return self.__resultsfolder
    
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
       l=list(unique_salt_pepper)
       l.sort()
       return l

    def get_inputrows_with_salt_pepper(self,salt_pepper_ratio:float):
        results=filter(lambda x: x.salt_pepper == salt_pepper_ratio, self.inputrows)
        return list(results)

    def get_results_from_inputrow(self,inputrow:InputRow)->List[OutputRow]:
        results=filter(lambda x: x.imagefile == inputrow.imagefile, self.outputrows)
        return list(results)
