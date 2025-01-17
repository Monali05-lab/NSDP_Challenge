# NSDP_Challenge

## Objective
This project analyzes delays in National Summary Data Page (NSDP) dissemination across various countries. The goal is to process the dataset, extract insights, and create an interactive Power BI report to visualize findings. 

## Instructions to Run the Python Script

## 1. Prerequisities 
- Install the required python libraries by running:
  ```bash
  pip install pandas numpy scipy insights

- Place the input file:
  - nsdp_delays_random.xlsx in the same directory as the python script.

## 2. Run the Script
  - Execute the script.

Output files
Once the script is exceuted, the following CSV files will be generated in the CSV Outputs/folder:
1. Average_Delay_By_Country.csv: Contains average delay by year for each country.
2. Regional_Avrages.csv: Contains average delays by region and year.
3. Outliers.csv: Contains countries identified as statistical outliers and their corresponding delay values.

Instructions to Explore Power BI Report
1. Open the PowerBI report file(NSDP_Challenge.pbix)in Power BI Desktop.

2. Navigate through the following visuals: 
 -Yearly Average Delays by Country: Line chart displaying average delays by year and country
 -Regional Delay Comparisons: Bar chart showing average delays by region for a selected year.
 -Top 5 Countries with Highest Delays: Table displaying top 5 countries with the highest average delays.
 -Outliers Analysis:Scatter plot highlighting countries with significant delay outliers.

 3. Use slicers for Region,Year, and Country to dynamically filter the data.


Assumptions:
-Outlier detection uses the Z-score method with threshold of 1.
-Data cleaning excludes rows with missing or negative Delay (days) and only includes rows where Type is Timeliness.
-Static mapping is used to derive country and region names from ISO codes.



