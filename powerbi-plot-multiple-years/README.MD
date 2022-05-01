# Power BI line chart with multiple years of Sales/Time series Data - So many options!

# Problem statement
![objective](docs/images/objective.png)
I have 5 years of daily sales data (or any time series data). How do I make the best use of Power BI to spot trends and make projections?
Why am I writing about this? Doesn't Power BI already handle this out of box? The problem is deceptively simple. Yes - Power BI can handle this out of box but there are myriad options and switches that once could toggle. 
I decided to write a step-by-step article so that I could present my journey - starting from the most basic Line Chart of Power BI and then adding more features along the way.


# About the data
![excel_data_view](docs/images/excel_data_view.png)

This data has been synthetically generated over a 5 year period using a Python script. This has just 2 columns: Date and Sales.

# Which version of Power BI Desktop?
All visuals in this article were carried out using Power BI Desktop version 2.104.941

# Data intro sheet
![overview_of_data](docs/images/data_overview.png)
We can see that we have 
- 1800 days of data
- Starting from 17 May 2012 
- Ending on 20 April 2017
- Min sales is 19,791
- Max sales is 23,859

I have turned off the out of box date hierarchy creation form the  "Date and time intelligence" settings. In late stages we will create this hierarchy through custom calculated columns.
![time_intelligence_options](docs/images/time_intelligence.png)

Refer accompanying PBIX "data_overview.pbix"


# All years in a single line - Most basic 
- We have not added any legend
- We have added a zoom slider
- X axis displays the "Date" column in a Continuous fashion
- Y axis displays the "Median Sales" column

![most_basic](docs/images/single_line_most_basic.png)

---

# All years in a single line - Most basic  (Categorical X axis)
- We have not added any legend
- We have added a zoom slider
- X axis displays the "Date" column in a Categorical fashion
- Y axis displays the "Median Sales" column

![most_basic_categorical](docs/images/single_line_most_basic_categorical.png)
Changing to "Categorical" from "Continuous" has radically altered the behaviour of the X-axis.
#### Advantage of Categorical
You get to analyze the data at a very micro level

#### Disadvantage of Categorical
You lose the ability to zoom into the data gradually. You want to a higher level view of the data first.

---

# All years in a single visual (single curve) - Add a Legend on Year
Our "out of box" approach so far is good, but suffers from a few challenges. Namely:
- Difficult to distinguish the Years visually
- Lack of a legend

#### Adding time intelligence
We decided against using the out of box date hierarchy. Lets add some calculated columns to the "Sales" table

```dax
Year = YEAR([date])

MonthNumber = MONTH([Date])

MonthText = FORMAT([Date],"mmmm")

DayNoOfYear = DATEDIFF ( DATE ( YEAR ( sales[date] ), 1, 1 ), sales[date], DAY ) + 1
```
![calculate_columns](docs/images/custom_date_calculated_columns.png)

#### Ensuring MonthText is correctly sorted

![sort_column](docs/images/month_text_sorty_column.png)


##### Finally adding the legend

![single_line_legend](docs/images/single_line_legend.png)

---
# How to reset the Zoom sliders back to their default state (a Home button)?
Zoom sliders are great. They let you quickly narrow down on a region of interest.
![zoom_slider_before](docs/images/zoom_slider_before.png)

How do you go back to the default position in a single click? For those who have used Matplotlib, you would be familiar with the "Home" button.

![matplotlib_toolbar](docs/images/matplotlib_toolbar.png)

![zoom_slider_with_home_button](docs/images/zoom_slider_with_home_button.png)

In the above example, I used a Button linked to a Bookmark which provide a "resetting" like functionality.

---
# Iteration 2.2 - All years in a single visual (single curve) - Select the Year(s)
- The need to turn off/on selective years
- A legend with years
- Slicer with years

---

# Iteration 2.3 - All years in a single visual (single curve) - Fill missing dates on X axis
shifting
- We are using the custom measures to fill in gaps along X axis (Min and Max values of X axis are provided by a measure)

---

# Iteration 2.4 - All years in a single visual (single curve) - Fill missing trailing and leading dates
- Explain the problem of the missing dates
- Problem - The first year and the last year do not have all the days of data. Hence the limts of the X axis keep changing as we select/de-select years 

---

# Iteration 2.5 - Steady Y axis
- Explain the problem. The Y axis keeps jumping
Set the Y axis lower and upper limits to a Measure which returns hard coded values
- Use 2 measures to set the lower and upper limits of the X axis

---

# Iteration 3 - All years in a single visual (1 curve for every year)
- The need to turn off/on selective years
- A legend with years
<< Talk about the need for additional column DayNoOfYear >>
<< Multiple lines >>

---

# Iteration 3.1 - Zoom sliders (investigate)
- How to restore to non-zoom
- 

---

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
- ~~Improve the synthetic data generation (slowly risising, with some randomness)~~
- Can we rest the view when using Zoom sliders?
- 