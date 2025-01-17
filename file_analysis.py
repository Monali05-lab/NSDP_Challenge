import pandas as pd
import numpy as np
import requests
from scipy.stats import zscore

#Static mapping of ISO3 codes to country names and regions 
ISO_COUNTRY_REGION_MAPPING = {
    "DNK": {"Country Name": "Denmark", "Region": "Europe"},
    "DEU": {"Country Name": "Germany", "Region": "Europe"},
    "BRA": {"Country Name": "Brazil", "Region": "South America"},
    "IND": {"Country Name": "India", "Region": "Asia"},
    "FRA": {"Country Name": "France", "Region": "Europe"},
    "EGY": {"Country Name": "Egypt", "Region": "Africa"},
    "JPN": {"Country Name": "Japan", "Region": "Asia"},
    "CAN": {"Country Name": "Canada", "Region": "North America"},
    "ARG": {"Country Name": "Argentina", "Region": "South America"},
    "MEX": {"Country Name": "Mexico", "Region": "North America"},
}

def map_iso_to_country_and_region(df):
    #Map ISO3 codes to country names and regions using a static dictionary. Adds two new columns: 'Country Name' and 'Region'.
    df = df.copy() #Copy the dataframe
    df["Country Name"] = df["Country"].map(lambda x: ISO_COUNTRY_REGION_MAPPING.get(x, {}).get("Country Name", "Unknown"))
    df["Region"] = df["Country"].map(lambda x: ISO_COUNTRY_REGION_MAPPING.get(x, {}).get("Region", "Unknown"))
    return df

def load_data(file_path):
    #Load the dataset from an Excel file.
    return pd.read_excel(file_path)

def clean_and_filter_data(df):
    #Clean and filter the dataset: 
    #Rename columns for consistency
    df.rename(columns={'ISO3 Code': 'Country', 'Delay (days)': 'Delay (days)'}, inplace=True)
    #Filter data to type = 'Timeliness' and exclude records where delay(days) is negative or missing
    df = df[(df['Type'] == 'Timeliness') & (df['Delay (days)'] > 0)]
    print("Filtered Data:")
    print(df.head())
    return df

def calculate_average_delay_by_country(df):
    #Calculate the average delay per year for each country.
    avg_delay = df.groupby(['Country Name', 'Region', 'Year'])['Delay (days)'].mean().reset_index()
    avg_delay.columns = ['Country Name', 'Region', 'Year', 'Average Delay (days)']
    print("Intermediate Result - Average Delay by Country:")
    print(avg_delay.head())
    return avg_delay

def calculate_top_5_countries_with_highest_delays(avg_delay, enriched_data):
    #Identify the top 5 countries with the highests average delays across all years.
    top_5 = (
        avg_delay.groupby(['Country Name', 'Region'])['Average Delay (days)']
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    #Merge with enriched_data to include Country Name
    # top_5 = top_5.merge(enriched_data[['Country', 'Country Name']].drop_duplicates(), on='Country', how='left')
    print("Top 5 Countries with Highest Average Delays:")
    print(top_5)
    return top_5

def calculate_regional_averages(df):
    # Compute the average delay by region for each year.
    regional_avg = df.groupby(['Region', 'Year'])['Delay (days)'].mean().reset_index()
    regional_avg.columns = ['Region','Year','Average Delay (days)']
    print("Regional Averages:")
    print(regional_avg.head()) #Debugging output
    return regional_avg

def identify_region_with_most_improvement(regional_avg):
    #Identify the region with the most improvement in timeliness over the years.
    improvement =( 
        regional_avg.groupby('Region')['Average Delay (days)']
        .agg(['first', 'last'])
        .reset_index()
    )
    improvement['Improvement'] = improvement['first']-improvement['last']
    print("Region with Most Improvement:")
    print(improvement.head())
    return improvement.sort_values('Improvement', ascending=False).head(1)

def detect_outliers(df, threshold=1.0):
    #Identify countries with delays that are satistical outliers using Z-score
    df = df.copy()
    df['Z-score'] = zscore(df['Delay (days)'])
    #Debugging: print zscore distribution
    print("Z-score Dsitribution:")
    # print(df[['Country', 'Country Name', 'Delay (days)', 'Z-score']].head())
    #Detect outliers based on Zscore
    outliers = df[np.abs(df['Z-score']) > threshold][['Country', 'Country Name', 'Delay (days)', 'Z-score']]
    print("Outliers Detected:")
    print(outliers if not outliers.empty else "No outliers detected with the current threshold.")
    return outliers

def export_results(avg_delay, regional_avg, outliers):
    #Export the results to csv files
    avg_delay.to_csv('Average_Delay_By_Country.csv', index=False, header=True)
    regional_avg.to_csv('Regional_Averages.csv', index=False, header=True)
    outliers.to_csv('Outliers.csv', index=False, header=True)

def main():
    #Load the dataset
    file_path = 'nsdp_delays_random.xlsx'
    df = load_data(file_path)

    #Clean and filter the data
    filtered_data = clean_and_filter_data(df)

    #Map ISO codes to country names and regions
    enriched_data = map_iso_to_country_and_region(filtered_data)

    #Perform analyses
    avg_delay_by_country = calculate_average_delay_by_country(enriched_data)
    top_5_countries = calculate_top_5_countries_with_highest_delays(avg_delay_by_country, enriched_data)
    regional_averages = calculate_regional_averages(enriched_data)
    region_improvement = identify_region_with_most_improvement(regional_averages)
    outliers = detect_outliers(enriched_data)

    #Export resuts
    export_results(avg_delay_by_country, regional_averages, outliers)

    #Print key insights
    print("Top 5 Countries with Highest Average Delays")
    print(top_5_countries)
    print("Region wiht Most Improvement:")
    print(region_improvement)
    print("Outliers Detected:")
    print(outliers)

if __name__ == "__main__":
    main()



