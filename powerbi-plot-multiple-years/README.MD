# Power BI - A line chart with multiple years of Sales/Time series Data - So many options!

# Problem statement
<< show a picture of a PBI line visual which describes what we want to visualize >>
<< to be done >>
Describe the problem. Looks so simple, but gets complex with increasing functional complexity
Something about the domain here - Commodity price

What does the data analyst want  - *Give me the best way to visualize the data so that I can easily spot trends and make projections*


# About the data
<< describe the data >>
Show a partial table, screen grab from Power BI
Mention that this was synthetic
Describe the columns
- Date column is ISO
- The Commodity price column is 

# About the data used in this exercise?
Talk about the accompanying Python Code
<< to be done >>


# Data intro sheet
- Show a table with all years
- Have 2 columns. For every year show Min and Max dates (this will bring up missing dates)
- Have 1 column. Display total count of records in every year 

# Iteration 1 - Multiple visuals - 1 visual for every year  (IGNORE FOR NOW, BEGIN WITH MULTIPLE)
In a single report, there will be multiple visuals (1 per year)
stacked vertically
- Set the Start and End date values on the X axis manually for each visual
- Set the Title property manually
- Set the Y axis lower and upper limits to some hard code values

Make sure all Y axis have the same scale

<< to be done>>

# Iteration 1.1 -Multiple visuals - 1 visual for every year (master-detail) (IGNORE FOR NOW, BEGIN WITH MULTIPLE)
Similar to Iteration 1 , but right click and drill through on a Visual and jump to a sheet with a larger view
- A single detail sheet
- Use measures to customize the Title property
- Show tooltips on the Visual
- Set the Y axis lower and upper limits to a Measure which returns hard coded values

# Iterarion 1.2 - Multiple visuals - Handle missing dates (IGNORE FOR NOW, BEGIN WITH MULTIPLE)
- The first year of the series 
# Iteration 1.5 -1 visual - Aggregate by Month (NOT SURE IF THIS FITS IN HERE)

to be done
<< here we are putting all Years in a single visual>>
this is similar to previous Iteration, but for the added drill down capability


YOU WERE HERE, CHANGE TO MONTH TEXT FROM MONTH NUMBER



# Iteration 2.0 - All years in a single visual (single curve)
<< use a zoom slider >>

- We are sliding from start to end
- Continuous view
- Possibility of a zoom slider
- Do not set any upper and lower limits to the Y axis

# Iteration 2.1 - All years in a single visual - Fill missing trailing and leading dates (single curve, )
- Explain the problem of the missing dates
- Set the Y axis lower and upper limits to a Measure which returns hard coded values
- Use 2 measures to set the lower and upper limits of the X axis

# Iteration 2.2 - All years in a single visual - Select the Year(s)
- The need to turn off/on selective years
- A legend with years
- We are using the custom measures to fill in gaps along X axis
- 

# Iteration 3 - All years in a single visual (1 curve for every year)
- The need to turn off/on selective years
- A legend with years
<< Talk about the need for additional column DayNoOfYear >>
<< Multiple lines >>


# Iteration 3.1 - Zoom sliders (investigate)
- How to restore to non-zoom
- 

# Iteration 3.2 - Changing from continuous to categorical
<< to be done, continuation of I3>>


# Iteration 4 -  Using tooltips to zoomin
- to be done
- See my notes in the notebook
- How do you come out of the Calendar context? Use another Date table perhaps?

# Iteration X - Small multiples (WE MAY NOT NEED THIS, IF WE ARE NOT DOING MULTIPLE VISUALS)
<< to be done >>


# Accompanying files in Github
Provide link to Github
Explain the repo structure
<< to be done >>

# To be done
- Improve the synthetic data generation (slowly risising, with some randomness)