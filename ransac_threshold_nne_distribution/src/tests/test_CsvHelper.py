import unittest
from data.OutputRow import OutputRow
from data.CsvHelper import CsvHelper
import os

class Test_CSvHelper(unittest.TestCase):

    def test_write_results_to_csv(self):
        row1=OutputRow()
        row1.imagefile="file1.png"
        row1.outputimagefile="output1.png"
        row1.actualthreshold=1.1
        row1.thresholdfactor=11

        row2=OutputRow()
        row2.imagefile="file2.png"
        row2.outputimagefile="output2.png"
        row2.actualthreshold=1.1
        row2.thresholdfactor=11

        results_filename="test_output.csv"
        folder_script=os.path.dirname(__file__)
        absolute_results_filename=os.path.join(folder_script,"out",results_filename)

        expected_outputrows=[row1,row2]
        CsvHelper.write_results_to_csv(filename=absolute_results_filename,output_rows=expected_outputrows)
        self.assertTrue(os.path.exists(absolute_results_filename))

        results_filehandle=open(absolute_results_filename,"r")
        actual_lines=list(results_filehandle)
        results_filehandle.close()
        
        self.assertEquals(len(actual_lines),1+len(expected_outputrows))

        self.assertTrue("inputimagefile,outputimagefile,threshold,thresholdfactor" in actual_lines[0])
        self.assertTrue(f"{row1.imagefile},{row1.outputimagefile},{row1.actualthreshold},{row1.thresholdfactor}" in actual_lines[1])
        pass

        