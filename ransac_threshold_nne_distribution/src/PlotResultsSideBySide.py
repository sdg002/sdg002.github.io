import csv
from os import path
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import os
from data import *
from algorithms.Util import Util

from data.InputRow import InputRow
from data.OutputRow import OutputRow
from data.CsvHelper import CsvHelper
from itertools import groupby


def experiment():
    path1="C:/Users/saurabhd/MyTrials/MyGithubPage/ransac_threshold_nne_distribution/src/history/Candidate3-factor-1.0/in/noisy_image_with_1_line-SP-0.970-MAXD-3.0.png"
    path2="C:/Users/saurabhd/MyTrials/MyGithubPage/ransac_threshold_nne_distribution/src/history/Candidate3-factor-1.0/out/sequential-ransac-noisy_image_with_1_line-SP-0.970-MAXD-5.0-tfac-1.00.png"
    image1=mpimg.imread(path1)
    image2=mpimg.imread(path2)

    max_rows=4
    fig, axes = plt.subplots(nrows=max_rows, ncols=2)

    for row in range(0,max_rows):
        axes[row][0].imshow(image1)
        axes[row][0].axis('off')
        axes[row][0].set_title("Image left")
        #axes[row][0].set_facecolor('blue') #did not work

        axes[row][1].imshow(image2)
        axes[row][1].axis('off')
        axes[row][1].set_title("Image right")
        #axes[row][1].set_facecolor('red') #did not work
        pass
    #fig.patch.set_facecolor('blue') #this changes the background of the entire plot, not just the individual image
    fig.tight_layout()
    fig.suptitle("Title centered above all subplots", fontsize=14)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1.0)
    #plt.title("Some title") #this did not work, instead it overwrote the title of the last subplot
    plt.show()



def create_subplots(maintitle:str, left_image_files:List[str], right_image_files:List[str]):
    if (len(left_image_files) != len(right_image_files)):
        raise Exception("The count of left files did not match the count of right files")
    print("Title=%s Count of input files=%d" % (maintitle,len(left_image_files)))

    max_rows=len(left_image_files)
    fig, axes = plt.subplots(nrows=max_rows, ncols=2)
    for row in range(0,max_rows):
        image_left=mpimg.imread(left_image_files[row])
        left_image_filename=os.path.basename(left_image_files[row])

        image_right=mpimg.imread(right_image_files[row])
        right_image_filename=os.path.basename(right_image_files[row])

        axes[row][0].imshow(image_left)
        axes[row][0].axis('off')        
        axes[row][0].set_title(left_image_filename)

        axes[row][1].imshow(image_right)
        axes[row][1].axis('off')
        axes[row][1].set_title(right_image_filename)
        pass
    fig.tight_layout()
    fig.suptitle(maintitle, fontsize=14)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1.0)
    plt.show()

def filter_images_for_salt_pepper(salt_pepper:float,filenames:List[str])->List[str]:
    pattern=("SP-%.3f" % (salt_pepper))
    filtered_filenames=list(filter(lambda x: pattern in x,filenames))
    return filtered_filenames

def filter_images_with_pattern(pattern:str, filenames:List[str])->List[str]:
    filtered_filenames=list(filter(lambda x: pattern in x,filenames))
    return filtered_filenames
'''
For every file in sourcefiles, find the file in target which matches
This helps in ordering the 2 sets of files. every item in sourcefiles has a matching entry in resultfiles at the same index
'''
def get_result_files_with_matching_filenamepattern(sourcefiles:List[str], resultfiles:List[str])->List[str]:
    if (len(sourcefiles) != len(resultfiles)):
        raise Exception("The count of files in source=%d did not match the count of files in results=%d" % (len(sourcefiles),len(resultfiles)))
    ordered_result_files=[]
    for sourcefile in sourcefiles:
        source_base_name=os.path.basename(sourcefile)
        source_base_name_noextension=os.path.splitext(source_base_name)[0]
        resultfiles_which_match_sourcefile=list(filter(lambda f: source_base_name_noextension in os.path.basename(f),resultfiles))
        if (len(resultfiles_which_match_sourcefile)>1):
            raise Exception("Found more than 1 result files which match file name of source %s" % (source_base_name))
        ordered_result_files.append(resultfiles_which_match_sourcefile[0])
    return ordered_result_files

def start():
    current_folder=os.path.dirname(__file__)
    
    folder_with_result_images=os.path.join(current_folder,"history/Candidate3-factor-1.0/out")
    folder_with_input_images=os.path.join(current_folder,"history/Candidate3-factor-1.0/in")

    result_image_files=glob.glob(folder_with_result_images+"/"+"*.png")
    input_image_files=glob.glob(folder_with_input_images+"/"+"*.png")

    salt_pepper_ratios=[0.9, 0.92, 0.95, 0.97,0.99]
    num_lines=[1,2]
    for num_line in num_lines:
        num_line_pattern=("%d_line") % (num_line)
        for salt_pepper_ratio in salt_pepper_ratios:
            input_images_with_salt_pepper:List[str]=filter_images_for_salt_pepper(salt_pepper=salt_pepper_ratio, filenames=input_image_files)
            input_images_with_salt_pepper_and_num_line=filter_images_with_pattern(pattern=num_line_pattern, filenames=input_images_with_salt_pepper)

            result_images_with_salt_pepper:List[str]=filter_images_for_salt_pepper(salt_pepper=salt_pepper_ratio, filenames=result_image_files)
            result_images_with_salt_pepper_and_num_line=filter_images_with_pattern(pattern=num_line_pattern, filenames=result_images_with_salt_pepper)

            result_images_ordered:List[str]= get_result_files_with_matching_filenamepattern(sourcefiles=input_images_with_salt_pepper_and_num_line, resultfiles=result_images_with_salt_pepper_and_num_line)
            title=("Salt pepper ratio=%.3f,  number of lines=%d") % (salt_pepper_ratio,num_line)
            create_subplots(title, left_image_files=input_images_with_salt_pepper_and_num_line, right_image_files=result_images_ordered)
#start()

# to be done
# order the results on MAXD when displaying on matplotlib
# Why yellow background

def find_results_csv_from_input_csv(inputfilename:str):
    #temp implementation
    if ("small_dataset_1line" not in inputfilename):
        return None
    return "C:\\Users\\saurabhd\\MyTrials\\MyGithubPage\\ransac_threshold_nne_distribution\\src\\out\\small_dataset_1line.results\\result_image.csv"

def generate_report_for_input_csv(input_images_csvfile:str):
    input_image_folder=os.path.dirname(input_images_csvfile)
    results_csv_file=find_results_csv_from_input_csv(inputfilename=input_images_csvfile)
    if (results_csv_file == None):
        print(f"\tNo results csv found for {Util.display_leaf_folders_from_path(path=input_image_folder,count=3)}")        
        return

    input_rows=CsvHelper.read_input_rows_from_csv(filename=input_images_csvfile)
    result_rows=CsvHelper.read_result_rows_from_csv(filename=results_csv_file)
    #input_rows_by_salt_pepper=sorted(input_rows, key=lambda x:x.salt_pepper)
    #we will go with the expectation that the input rows in the CSV is in the order we desire
    for salt_pepper_key,g in groupby(input_rows, key=lambda x:x.salt_pepper):
        files_in_group=list(g)
        print(f"\tProcessing salt_pepper={salt_pepper_key}, found {len(files_in_group)} input files")
        for file_in_group in files_in_group:
            matching_result_rows=list(filter(lambda x: x.imagefile == file_in_group.imagefile , result_rows))
            print(f"\t\t{file_in_group.imagefile}...result files={len(matching_result_rows)}...max_distance={file_in_group.max_distance}")
            for result_file in matching_result_rows:
                print(f"\t\t\t{result_file.outputimagefile}...tfac={result_file.thresholdfactor}...threshold={result_file.actualthreshold}")

    # for input_row in input_rows:
    #     matching_result_rows=list(filter(lambda x: x.imagefile == input_row.imagefile,result_rows))
    #     #you were here, try teh group by approach #first group by salt, then sort on max distance

    pass

def main():
    print("This script will search for input CSV files generated by Salt-Pepper script")
    output_folder=os.path.join(os.path.dirname(__file__),"Out/")    
    input_csv_files=glob.glob(output_folder+"/**/*input*.csv",recursive=True)
    print("Found %d files" % (len(input_csv_files)))
    if (len(input_csv_files) == 0):
        print("No CSV files found with input images. Quitting")
        return

    for file_index in range(0,len(input_csv_files)):
        input_csv_file=input_csv_files[file_index]
        print(f"\t{Util.display_leaf_folders_from_path(path=input_csv_file, count=3)}")

    print("Going to generate friendly report")
    for file_index in range(0,len(input_csv_files)):
        input_csv_file=input_csv_files[file_index]
        print(f"\tProcessing file...{Util.display_leaf_folders_from_path(path=input_csv_file, count=3)}")
        generate_report_for_input_csv(input_images_csvfile=input_csv_file)
        print("----------------------------")

    pass

if __name__ == "__main__":
    main()
