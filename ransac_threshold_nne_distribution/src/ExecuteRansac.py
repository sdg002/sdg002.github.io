import os
import glob
from typing import List, Pattern

from numpy.lib.function_base import append
from algorithms.RansacLineInfo import  RansacLineInfo
from Util import Util
import skimage.io
from algorithms.SequentialRansac import SequentialRansac
import time
import csv
from data.InputRow import InputRow
import shutil
from data.OutputRow import OutputRow
from data.CsvHelper import CsvHelper


def run(inputfilepath:str,outputfolder:str,max_lines_to_find:int,threshold_factor:float):
    print("-----------------------------------------")
    print("Going to run RANSAC on the file %s" % inputfilepath)
    if (os.path.exists(outputfolder) == False):
        raise Exception(f"The output folder:{outputfolder} was not found")

    if (os.path.exists(inputfilepath) == False):
        raise Exception(f"The input image:{inputfilepath} was not found")

    start=time.time()
    seq=SequentialRansac(path=inputfilepath,max_lines_to_find=max_lines_to_find,ransac_threshold_factor=threshold_factor)
    line_results:List[RansacLineInfo]=seq.run_sequential_ransac()  
    actual_ransac_threshold=0 #TODO return the calculated Treshold as an additional parameter in the run_sequential_ransac() method
    superimposed_image=Util.superimpose_all_ransac_lines(seq.image_array,line_results)
    elapsed_time=(time.time() - start)

    #Save the results
    inputfilename=os.path.basename(inputfilepath)
    filename_noextension=os.path.splitext(inputfilename)[0]
    result_filename=("result-%s-tfac-%.2f.png") % (filename_noextension,round(threshold_factor,2))
    absolute_result_filename=os.path.join(outputfolder,result_filename)
    skimage.io.imsave(absolute_result_filename,superimposed_image)
    print("Results saved to file %s" % absolute_result_filename)
    print("Time elapsed=%f seconds" % (elapsed_time))
    return result_filename,actual_ransac_threshold
    

'''
old code that can be retired once you are done

in_folder_with_samples=os.path.join(os.path.dirname(__file__),"In/")
current_folder_with_unittests=os.path.join(os.path.dirname(__file__),"test/")
output_folder=os.path.join(os.path.dirname(__file__),"Out/")
THRESHOLD_FACTOR=0.25

def run_selected_filepattern(folder:str,pattern:str,max_lines_to_find:int,threshold_factor:float):
    matching_files=glob.glob(folder+"/"+pattern)
    print("Found %d files which match the pattern %s in the folder: %s" % (len(matching_files),pattern,folder))
    for matching_file in matching_files:
        run(inputfilepath=matching_file,outputfolder=output_folder,max_lines_to_find=max_lines_to_find, threshold_factor=threshold_factor)


'''

'''
Creates a new folder at the sibling level of the parent of the CSV file
Example:
    c:\folder1\folder2\input.csv
    will produce
    c:\folder1\folder2.out
'''
def create_empty_folder_for_results(csvfile:str):
    parent_dir=os.path.dirname(csvfile)
    parent_of_parent_dir=os.path.dirname(parent_dir)
    parent_dir_foldername=os.path.split(parent_dir)[1]
    new_foldername_for_results=parent_dir_foldername+".results"
    new_dir_results=os.path.join(parent_of_parent_dir,new_foldername_for_results)
    if (os.path.exists(new_dir_results)==True):
        print(f"The directory {new_dir_results} was found")
        shutil.rmtree(new_dir_results)
        print(f"The directory {new_dir_results} was deleted")
    else:
        print(f"The directory {new_dir_results} does not exist")
    os.mkdir(new_dir_results)
    return new_dir_results

def execute_ransac_on_files(csvfile:str,threshold_factors:List[float]):
    csv_results_file=None # initialize this to the path of a csv file in output_folder, all results will be written here

    input_datarows=CsvHelper.read_input_rows_from_csv(filename=csvfile)
    ransac_results:List[OutputRow]=[]
    new_directory_for_results=create_empty_folder_for_results(csvfile=csvfile)
    new_csv_file_for_results=os.path.join(new_directory_for_results,"result_image.csv")

    input_image_folder=os.path.dirname(csvfile)
    for input_datarow in input_datarows:        
        for threshold_factor in threshold_factors:
            print(f'image={input_datarow.imagefile}, no of expected lines={input_datarow.line_count}, threshold factor={threshold_factor}')
            absolute_input_file=os.path.join(input_image_folder,input_datarow.imagefile)
            (result_filename,actual_threshold)=run(inputfilepath=absolute_input_file,outputfolder=new_directory_for_results,max_lines_to_find=input_datarow.line_count, threshold_factor=threshold_factor)
            result=OutputRow()
            result.imagefile=input_datarow.imagefile
            result.thresholdfactor=threshold_factor
            result.outputimagefile=result_filename
            result.actualthreshold=actual_threshold
            ransac_results.append(result)
            pass
    print(f"Completed processing {len(input_datarows)} image files.")
    CsvHelper.write_results_to_csv(output_rows=ransac_results,filename=new_csv_file_for_results)


def main():
    ###
    #remove this
    execute_ransac_on_files("C:\\Users\saurabhd\\MyTrials\\MyGithubPage\\ransac_threshold_nne_distribution\\src\\out\\very_small_dataset_2lines\\input_images.csv", threshold_factors=[0.5, 0.1])
    return
    ###
    print("This script will search for input CSV files generated by Salt-Pepper script")
    output_folder=os.path.join(os.path.dirname(__file__),"Out/")    
    matching_files=glob.glob(output_folder+"/**/*.csv",recursive=True)
    print("Found %d files" % (len(matching_files)))
    if (len(matching_files) == 0):
        print("No CSV files found with input images. Quitting")
        return


    for file_index in range(0,len(matching_files)):
        matching_file=matching_files[file_index]
        csvfile=os.path.basename(matching_file)
        print("%d......%s" % (file_index,matching_file))
    choice=input("Select the index of the file which you want to run RANSAC on: ")
    ichoice=int(choice)
    if (ichoice < 0 or ichoice >= len(matching_files)):
        print("Choice cannot be less than 0 or greater than %d . Quitting." % (len(matching_files)))
        return
    print("You selected %d" % (ichoice))
    print("file = %s " % (matching_files[file_index]))


if __name__ == "__main__":
    main()

        