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
# Structuring into entities

## Folder structure
- root
    - entity
        - Circle
        - Line
        - SqliteWrapper
    - experiments
    - tests
        - test_CircleEntity
        - test_LineEntity

## Circle entity
- center(Point)
- radius
- Start angle
- End angle
- Number of points
- Mean angular distance between points (read only property)

## Line entity
- unit vector (Point)
- Start (Point)
- End (Point)
- Number of points
- Mean distance between points (read only property)


## SqlLiteWrapper clas
- ctor to initialize a new database, with givne path
- method to add multiple Circle objects
- method to add multiple Line objects
- method DeleteAll() to remove all Circle and Line objects

## Old Work log
- Move find_circle_clusters to CircleFinder (done)
- Clean up and test the movement (done)
- Use the Sine wave using the above
- Create clusters of lines using median separation
- Add Circle to RootModel during detection
- Add Line to RootModel during detection
- Write algorithm to fit Line and Circle
    - Line and Line (fit a line/circle , how many inliers?)
    - Cirle and Line (fit a tangent to Circle, how much cost)
    - Circle and Circle
- ? 

## Challenges with non-patch approach
### Large parabola
- Lack of reliability
- E.g. In case of LARGE parabola, I was able to detect left side completely, but the right was partial (bottom was cut off)
- Possible reason - Change of NNE after the detection of the left side
- Possible reason - The RANSAC Trials count should be proportional to the square of the number of points
- Increased max trials to 1000,000.
- Very slow performance

### Narrow parabola (parabola.narrow)
- The results with NARROW parabola were better - But, I failed to detect the lower circle

### Bottom parabola (parabola.small)
- Did not get the complete bottom circle
- Did get left part of the bottom circle
- Did get partial right part of the bottom circle (Not good, but remember we do not have many points to work with)


##  Work log

# Patch by Patch approach
## Overall idea
- Decide on the dimension of the square patch (W pixels)
- Stride should be W/2 in both axis
- Begin with searching for 1 RANSAC line in each patch
- For every patch, calculate median distance between projected inliers (MD)
- Now, select those patches which have median distance > MD
- For these patches, re-run RANSAC till median distance falls below MD
- Collect all the new RANSAC lines that were found by the above step
- What do we end up with? - The image split into Patches and a collection of RANSAC lines from every Patch

## What do we detect first? Lines or circles
TO BE DONE

## How do we decide the size W of the patch square?
TO BE DONE

# Improving RANSAC

# Stopping criteria - how many circles and lines to detect in a patch
- Option 1 - Specify max circles or max lines. We are already doing this
- Option 2 - When nearest neighbour distance increases to over 2 times the original value

# Need a way to define density of Circle
- Example - Define an arc as 1 degree of arc length. For every such arc, determine how many points are there in that arc. How many such arcs are occupied? (NOT NEEDED BECAUSE OF FUTURE SPLIT VIA CLUSTERING)

# Add new property which gives the Arc of the circle


# Future thoughts
- Try reducing the image and do RANSAC on the entire image
- This might give you the patches to focus 


