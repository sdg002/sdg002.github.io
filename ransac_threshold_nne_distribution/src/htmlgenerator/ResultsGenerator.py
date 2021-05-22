from typing import List
from algorithms.ResultsViewModel import ResultsViewModel
from data.InputRow import InputRow
from data.OutputRow import OutputRow
import os
import shutil


class ResultsGenerator(object):
    """Generates a HTML file from an instance of the results view model."""
    def __init__(self, viewmodel:ResultsViewModel,filename:str):
        self.__viewmodel=viewmodel
        self.__filename=filename
        if (os.path.exists(self.__filename)==True):
            os.remove(self.__filename)

    def __append_html(self,htmlfragment):
        file_object=open(self.htmlfilename,"a")
        file_object.write(htmlfragment)
        file_object.write("\n")
        pass

    @property
    def viewmodel(self):
        """Returns the view model"""
        return self.__viewmodel

    @property
    def htmlfilename(self):
        """The path to the HTML file."""
        return self.__filename

    @property
    def currentfolder(self):
        """The folder in which the current Python file resides."""
        return os.path.dirname(__file__)

    def copy_cssfile(self):
        htmldir=os.path.dirname(self.htmlfilename)
        new_cssfile=os.path.join(htmldir,"results.css")
        source_cssfile=os.path.join(self.currentfolder,"results.css")
        shutil.copy(source_cssfile,new_cssfile)

    def start_body(self):
        #link to exernal CSS
        frag=""
        frag=frag+"<html><head>"
        frag=frag+"<link rel=\"stylesheet\" href='results.css' />"
        frag=frag+"</head>"
        frag=frag+"<body>"
        self.__append_html(frag)

    def close_body(self):
        frag=""
        frag=frag+"</body>"
        frag=frag+"</html>"
        self.__append_html(frag)

    def print_salt_pepper(self,salt_pepper):
        frag=f"<h3 class='saltpepper'>Salt pepper ratio={salt_pepper}</h3>"
        self.__append_html(frag)
        pass

    def print_maxdistance(self,max_distance:float):
        frag=f"<h3 class='maxdistance'>Max distance between points on line={max_distance}</h3>"
        self.__append_html(frag)
        pass

    def render_image(self,input_image_file:str,caption:str):
        frag=""
        frag=frag+"<figure>"
        frag=frag+f"<img src='{input_image_file}' class='input'/>"
        frag=frag+"<figcaption>"
        frag=frag+caption
        frag=frag+"</figcaption>"
        frag=frag+"</figure>"
        self.__append_html(frag)
    
    def generate_caption_for_input_image(self,mean_nnd:float):
        frag=""
        frag=frag+"Input image<br />"
        frag=frag+f"Mean nearest neighbour distance={mean_nnd}<br />"
        frag=frag+"<br />"
        return frag

    def generate_caption_for_result_image(self,ransac_threshold_factor:float,ransac_threshold:float):
        frag=""
        frag=frag+"Result image<br />"
        frag=frag+f"Ransac threshold factor={ransac_threshold_factor}<br />"
        frag=frag+f"Actual Ransac threshold={ransac_threshold}<br />"
        return frag

    def print_line(self):
        self.__append_html("<hr/>")
    
    def print_startresultsblock(self):
        self.__append_html("<div class='result'>")

    def print_endresultsblock(self):
        self.__append_html("</div>")

    def get_absolutepath_inputimage(self,filename:str):
        return os.path.join(self.viewmodel.inputfolder,filename)

    def get_absolutepath_resultimage(self,filename:str):
        return os.path.join(self.viewmodel.resultsfolder,filename)

    def generate_report(self):
        self.copy_cssfile()
        self.start_body()
        self.print_line()
        salt_pepper_ratios:List[float]=self.viewmodel.get_saltpepperratios()
        for salt_pepper in salt_pepper_ratios:
            input_rows_with_salt_pepper:List[input_row]=self.viewmodel.get_inputrows_with_salt_pepper(salt_pepper_ratio=salt_pepper)
            print(f"\tProcessing salt_pepper={salt_pepper}, found {len(input_rows_with_salt_pepper)} input files")
            for input_row in input_rows_with_salt_pepper:
                self.print_startresultsblock()
                self.print_salt_pepper(salt_pepper)
                self.print_maxdistance(max_distance=input_row.max_distance)

                input_image_caption=self.generate_caption_for_input_image(mean_nnd=2.11)
                input_image_absolute_filename=self.get_absolutepath_inputimage(input_row.imagefile)
                self.render_image(input_image_absolute_filename,input_image_caption)
                
                matching_result_rows=self.viewmodel.get_results_from_inputrow(input_row)
                print(f"\t\tProcessing input image:{input_row.imagefile}...result files={len(matching_result_rows)}...max_distance={input_row.max_distance}")
                for result_file in matching_result_rows:
                    print(f"\t\t\t{result_file.outputimagefile}...tfac={result_file.thresholdfactor}...threshold={result_file.actualthreshold}")
                    result_image_absolute_filename=self.get_absolutepath_resultimage(result_file.outputimagefile)

                    result_image_caption=self.generate_caption_for_result_image(ransac_threshold_factor=0.333, ransac_threshold=1.1)
                    self.render_image(result_image_absolute_filename,result_image_caption)  
                self.print_endresultsblock()
                self.print_line()
        self.close_body()
        pass
