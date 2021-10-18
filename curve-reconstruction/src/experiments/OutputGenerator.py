import simplegeometry as sg
from RootModel import RootModel
import skimage.io
import os

class OutputGenerator(object):
    """Responsible for generating output images with superimposed points."""
    def __init__(self):
        pass

    @classmethod
    def plot_ransac_circles_with_projections(cls,model:RootModel):
        inputfilepath:str=model.filename
        circles=model.ransac_circles
        
        print(f"Superimposing circles on base image: {inputfilepath}")
        for result_index in range(0,len(circles)):
            circle=circles[result_index]
            np_blank_image=skimage.io.imread(inputfilepath,as_gray=True)
            np_blank_image.fill(1)
            new_filename=f"circle-result-{result_index}-inlier-{len(circle.inlier_points)}-threshold-{round(circle.ransac_threshold,2)}-nnd-{round(circle.mean_nnd,2)}.png"
            absolute_path=os.path.join(model.output_folder,new_filename)
            print(f"Got a circle {circle}, saving to file {absolute_path}")
            points_list = list(map(lambda x: sg.Point(x[0],x[1]) , circle.projected_inliers ))
            np_newimage=sg.Util.superimpose_points_on_image(np_blank_image,points_list,255,0,0)
            skimage.io.imsave(absolute_path,np_newimage)
        pass

    @classmethod
    def plot_clustered_circles_with_projections(cls,model:RootModel):
        inputfilepath:str=model.filename
        circles=model.clustered_circles
        
        print(f"Superimposing clustered circles on base image: {inputfilepath}")
        for result_index in range(0,len(circles)):
            circle=circles[result_index]
            np_blank_image=skimage.io.imread(inputfilepath,as_gray=True)
            np_blank_image.fill(1)
            new_filename=f"circle-clustered-{result_index}-inlier-{len(circle.inlier_points)}-threshold-{round(circle.ransac_threshold,2)}-nnd-{round(circle.mean_nnd,2)}.png"
            absolute_path=os.path.join(model.output_folder,new_filename)
            print(f"Got a circle {circle}, saving to file {absolute_path}")
            points_list = list(map(lambda x: sg.Point(x[0],x[1]) , circle.projected_inliers ))
            np_newimage=sg.Util.superimpose_points_on_image(np_blank_image,points_list,255,0,0)
            skimage.io.imsave(absolute_path,np_newimage)
        pass


    @classmethod
    def plot_lines_with_projections(cls,model:RootModel):
        inputfilepath:str=model.filename

        print(f"Superimposing lines on base image: {inputfilepath}")
        for result_index in range(0,len(model.ransac_lines)):
            line=model.ransac_lines[result_index]
            np_blank_image=skimage.io.imread(inputfilepath,as_gray=True)
            np_blank_image.fill(1)
            new_filename=f"line-result-{result_index}-inlier-{len(line.projected_inliers)}-threshold-{round(line.ransac_threshold,2)}-nnd-{round(line.mean_nnd,2)}.png"
            absolute_path=os.path.join(model.output_folder,new_filename)
            print(f"Got a line {line}, saving to file {absolute_path}")

            points_list=line.projected_inliers
            np_newimage=sg.Util.superimpose_points_on_image(np_blank_image,points_list,255,0,0)
            skimage.io.imsave(absolute_path,np_newimage)
        pass
