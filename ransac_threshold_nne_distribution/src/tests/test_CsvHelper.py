import csv
import unittest
from data.OutputRow import OutputRow
from data.InputRow import InputRow
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
        absolute_results_filename=self.get_absolute_filename_under_testfolder(filename=results_filename)

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

    def test_write_inputimages_to_csv(self):
        all_input_rows=[]

        row1=InputRow()
        row1.imagefile="some image file 1"
        row1.total_pixels=101
        row1.black_pixels=2
        row1.salt_pepper=0.3
        row1.max_distance=4
        row1.line_count=1
        all_input_rows.append(row1)

        row2=InputRow()
        row2.imagefile="some image file 2"
        row2.total_pixels=102
        row2.black_pixels=300
        row2.salt_pepper=0.3
        row2.max_distance=2
        row2.line_count=2
        all_input_rows.append(row2)

        input_filename="test_input.csv"
        absolute_filename=self.get_absolute_filename_under_testfolder(filename=input_filename)
        CsvHelper.write_input_rows_to_csv(filename=absolute_filename,input_rows=all_input_rows)

        results_filehandle=open(absolute_filename,"r")
        actual_lines=list(results_filehandle)
        results_filehandle.close()

        self.assertEquals(len(actual_lines),1+len(all_input_rows))
        self.assertTrue("imagefile,salt_pepper,max_distance,line_count,total_pixels,black_pixels" in actual_lines[0])
        self.assertTrue(f"{row1.imagefile},{row1.salt_pepper},{row1.max_distance},{row1.line_count},{row1.total_pixels},{row1.black_pixels}" in actual_lines[1])
        self.assertTrue(f"{row2.imagefile},{row2.salt_pepper},{row2.max_distance},{row2.line_count},{row2.total_pixels},{row2.black_pixels}" in actual_lines[2])


    """
    Returns the absolute path of the specified file under the current script\out folder
    """
    def get_absolute_filename_under_testfolder(self,filename:str):
        folder_script=os.path.dirname(__file__)
        absolute_results_filename=os.path.join(folder_script,"out",filename)
        return absolute_results_filename
        pass