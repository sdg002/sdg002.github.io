
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