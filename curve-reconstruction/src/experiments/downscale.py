import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
import os
import skimage
import skimage.io

#
#https://scikit-image.org/docs/dev/auto_examples/transform/plot_rescale.html
#
def test_scikitsnippet():
    image = color.rgb2gray(data.astronaut())

    image_rescaled = rescale(image, 0.25, anti_aliasing=False)
    image_resized = resize(image, (image.shape[0] // 4, image.shape[1] // 4),
                        anti_aliasing=True)
    image_downscaled = downscale_local_mean(image, (4, 3))

    fig, axes = plt.subplots(nrows=2, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(image, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled, cmap='gray')
    ax[1].set_title("Rescaled image (aliasing)")

    ax[2].imshow(image_resized, cmap='gray')
    ax[2].set_title("Resized image (no aliasing)")

    ax[3].imshow(image_downscaled, cmap='gray')
    ax[3].set_title("Downscaled image (no aliasing)")

    ax[0].set_xlim(0, 512)
    ax[0].set_ylim(512, 0)
    plt.tight_layout()
    plt.show()

def get_absolute_path_from_input_filename(filename:str):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path=os.path.join(folder_script,"data/",filename)
    return absolute_path

def get_absolute_path_from_output_filename(filename:str):
    fullpathtoscript=os.path.realpath(__file__)
    folder_script=os.path.dirname(fullpathtoscript)
    absolute_path=os.path.join(folder_script,"out/",filename)
    return absolute_path

def test_rescale(filename:str,fraction:float,anti_aliasing:bool):
    absolute_input_path=get_absolute_path_from_input_filename(filename=filename)
    image=skimage.io.imread(absolute_input_path,as_gray=True)
    image_rescaled_no_antialiasing = rescale(image, fraction, anti_aliasing=anti_aliasing)

    image_resized_antialiasing = resize(image, ( round(image.shape[0] *fraction), round(image.shape[1] * fraction)),anti_aliasing=True)

    skimage.io.imsave(get_absolute_path_from_output_filename(filename=f"result.rescaled.antialising={anti_aliasing}.f={fraction}.{filename}"),image_rescaled_no_antialiasing)
    skimage.io.imsave(get_absolute_path_from_output_filename(filename=f"result.resized.antialising={anti_aliasing}.f={fraction}.{filename}"),image_resized_antialiasing)
    pass


if (__name__ =="__main__"):
    print("Inside main")
    #test_scikitsnippet()
    test_rescale(filename="cubic.W=500.H=200.MAXD=8.SP=0.99.26.png",fraction=0.5,anti_aliasing=True)
    test_rescale(filename="cubic.W=500.H=200.MAXD=8.SP=0.99.26.png",fraction=0.5,anti_aliasing=False)
    test_rescale(filename="cubic.W=500.H=200.MAXD=8.SP=0.99.26.png",fraction=0.25,anti_aliasing=True)
    test_rescale(filename="cubic.W=500.H=200.MAXD=8.SP=0.99.26.png",fraction=0.25,anti_aliasing=False)
