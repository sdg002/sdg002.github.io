# Objective 
## First objective
Given any continuous set of points in a field of noisy points, can we eliminate the noisy points and determine the curve

## Second objective
Give 2 or more continous curves in a field of noisy points, can we not only eliminate the noisy points but also identify the 2 continuous curves

# What are the curves?
## Circle
## Parabola
## Cubic
## Sine

# How to set PYTHONPATH?
From inside VSCODE, you can do the following to both the Python Debug Console and Python Console
```
$env:PYTHONPATH="$env:USERPROFILE%\MyTrials\MyGithubPage\simple-geometry"
```

# Installing via Anaconda
Summarizing my failed attempt to using Conda
## What did I install?
Installed miniconda because it has a smaller disk foot print

## How to install a package using Anaconda?
- Start menu
- Launch Anaconda (Miniconda) prompt
- `conda install scikit-geometry -c conda-forge`
- `conda list` should show your package
## Where does Anaconda install the packages?
%USERPROFILE%\miniconda3

# What next?
- Generate noisy images for the aforementioned
- Gnerate a data file for every image, for future processing (what did you do before?)


# Think of an easier way to generate images with multiple curves
## Existing flow
```
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.curvetype="spiral"
    generator.max_consecutive_distance=max_distance_between_2_points
    prefix=generator.generate_filename_prefix()
    generator.output_file=create_new_absolute_filename(prefix)
    generator.generate_curve()

```


## Desired flow
```
    generator=GenericCurveGenerator(width=img_width,height=img_height)
    generator.saltpepper=salt_pepper_noise
    generator.max_consecutive_distance=max_distance_between_2_points
    generator.output_file="c:/blah.png"
    generator.generate_curve(["circle", "parabola","spiral"])

```