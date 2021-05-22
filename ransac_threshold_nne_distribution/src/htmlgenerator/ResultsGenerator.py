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
        frag=("<h3 class='saltpepper'>Salt pepper ratio=%.2f</h3>" % (salt_pepper))
        self.__append_html(frag)
        pass

    def print_maxdistance(self,max_distance:float):
        frag=f"<h3 class='maxdistance'>Max distance between points on line={max_distance}</h3>"
        self.__append_html(frag)
        pass

    def render_image(self,image_absolute_path:str,caption:str):
        frag=""
        frag=frag+"<figure>"
        frag=frag+f"<img src='{image_absolute_path}' class='input'/>"
        frag=frag+"<figcaption>"
        frag=frag+caption
        frag=frag+"</figcaption>"
        frag=frag+"</figure>"
        self.__append_html(frag)
    
    def generate_caption_for_input_image(self,mean_nnd:float,max_distance:float):
        frag=""
        frag=frag+"Input image<br />"
        frag=frag+f"Mean nearest neighbour distance={mean_nnd}<br />"
        frag=frag+f"Distance between consecutive points on the line={max_distance}<br />"
        frag=frag+"<br />"
        return frag

    def generate_caption_for_result_image(self,ransac_threshold_factor:float,ransac_threshold:float,time:float):
        frag=""
        frag=frag+"Result image<br />"
        frag=frag+f"Ransac threshold factor={ransac_threshold_factor}<br />"
        frag=frag+f"Actual Ransac threshold={ransac_threshold}<br />"
        frag=frag+f"Time taken(s)={time}<br />"
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

                matching_result_rows=self.viewmodel.get_results_from_inputrow(input_row)
                matching_result_rows.sort(key=lambda x:x.thresholdfactor)

                nn_statistic_from_first_result=matching_result_rows[0].nearest_neighbour_distance_statistic
                input_image_caption=self.generate_caption_for_input_image(mean_nnd=nn_statistic_from_first_result, max_distance=input_row.max_distance)
                input_image_absolute_filename=self.get_absolutepath_inputimage(input_row.imagefile)
                self.render_image(image_absolute_path=input_image_absolute_filename,caption=input_image_caption)
                
                
                print(f"\t\tProcessing input image:{input_row.imagefile}...result files={len(matching_result_rows)}...max_distance={input_row.max_distance}")
                for result_row in matching_result_rows:
                    print(f"\t\t\t{result_row.outputimagefile}...tfac={result_row.thresholdfactor}...threshold={result_row.actualthreshold}")
                    result_image_absolute_filename=self.get_absolutepath_resultimage(result_row.outputimagefile)

                    result_image_caption=self.generate_caption_for_result_image(ransac_threshold_factor=result_row.thresholdfactor, ransac_threshold=result_row.actualthreshold,time=result_row.elapsed_time)
                    self.render_image(image_absolute_path=result_image_absolute_filename, caption=result_image_caption)  
                self.print_endresultsblock()
                self.print_line()
        self.close_body()
        pass
