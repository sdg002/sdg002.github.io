
class OutputRow(object):
    """docstring for OutputRow."""
    def __init__(self,):
        super(OutputRow, self).__init__()
        self.__inputfilename=None

    @property
    def imagefile(self):
        """The name of the input image file."""
        return self.__inputfilename
        
    @imagefile.setter
    def imagefile(self, value):
        self.__inputfilename = value

    @property
    def outputimagefile(self):
        """The name of the image file where the RANSAC results were saved."""
        return self._outputimagefile

    @outputimagefile.setter
    def outputimagefile(self, value):
        self._outputimagefile = value

    @property
    def actualthreshold(self):
        """The actualthreshold value used for the RANSAC calcualtions."""
        return self._actualthreshold

    @actualthreshold.setter
    def actualthreshold(self, value):
        self._actualthreshold = value

    @property
    def thresholdfactor(self):
        """The thresholdfactor property that was used to generate this RANSAC output."""
        return self.__thresholdfactor

    @thresholdfactor.setter
    def thresholdfactor(self, value):
        self.__thresholdfactor = value


    def __repr__(self):
        return f'input imagefile={self.imagefile}, outputimagefile={self.outputimagefile} , threshold factor={self.actualthreshold}, threshold factor={self.thresholdfactor}'
