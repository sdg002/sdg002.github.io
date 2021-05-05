import os
import glob
from typing import List
from RansacLineInfo import  RansacLineInfo
import Util
import skimage.io
from SequentialRansac import SequentialRansac

# Read the image
# use Kdtree to determine nearest neighbour
# Do ransac


def run(inputfilepath:str,outputfolder:str,num_trials:int,threshold_factor:float):
    print("-----------------------------------------")
    print("Going to run RANSAC on the file %s" % inputfilepath)
    seq=SequentialRansac(path=inputfilepath,max_lines_to_find=num_trials,ransac_threshold_factor=threshold_factor)
    line_results:List[RansacLineInfo]=seq.run_sequential_ransac()
    superimposed_image=Util.superimpose_all_ransac_lines(seq.image_array,line_results)


    #Save the results
    inputfilename=os.path.basename(inputfilepath)
    filename_noextension=os.path.splitext(inputfilename)[0]
    file_result=os.path.join(os.path.dirname(__file__),"./out/",("sequential-ransac-%s-tfac-%.2f.png") % (filename_noextension,round(threshold_factor,2)))
    skimage.io.imsave(file_result,superimposed_image)
    print("Results saved to file %s" % (file_result))

    pass


current_folder_with_samples=os.path.join(os.path.dirname(__file__),"In/")
output_folder=os.path.join(os.path.dirname(__file__),"Out/")
THRESHOLD_FACTOR=0.25

def run_selected_filepattern(folder:str,pattern:str,num_trials:int):
    matching_files=glob.glob(folder+"/"+pattern)
    print("Found %d files which match the pattern %s in the folder: %s" % (len(matching_files),pattern,folder))
    for matching_file in matching_files:
        run(inputfilepath=matching_file,outputfolder=output_folder,num_trials=num_trials, threshold_factor=THRESHOLD_FACTOR)



run_selected_filepattern(folder=current_folder_with_samples, pattern="*noisy*.png",num_trials=5000)
