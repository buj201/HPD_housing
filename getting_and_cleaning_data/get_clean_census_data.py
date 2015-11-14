import pandas as pd
import numpy as np
import re

def get_clean_income_data():
    ## Read in median income data from census
    query = 'http://api.census.gov/data/2013/acs5?get=B19013_001E&for=tract:*&in=state:36'
    state_income_data = pd.read_csv('http://api.census.gov/data/2013/acs5?get=B19013_001E&for=tract:*&in=state:36', header=0)
    
    ##Clean the data    
    state_income_data.columns = ['Median_income','State', 'County', 'CT2010','misread']
    state_income_data = state_income_data.drop('misread',axis=1)
    state_income_data['Median_income'] = state_income_data['Median_income'].map(lambda x: re.sub('[^\d]', "", x))
    state_income_data['CT2010'] = state_income_data['CT2010'].map(lambda x: re.sub('[^\d]', "", x))
    
    ##Select rows by county:
    nyc_counties = {'Bronx': 5, 'Kings': 47, 'New_York':61, 'Richmond': 81, 'Queens': 85}
    city_income = state_income_data[(state_income_data['County'].isin(nyc_counties.values()))]
    county_to_boroughID = {5:2, 47:3, 61:1, 81:5, 85:4}
    city_income['BoroughID'] = city_income['County'].map(lambda x: county_to_boroughID[x])
    city_income = city_income.drop('County', axis=1)
    city_income['Median_income'] = city_income['Median_income'].map(lambda x: x if len(str(x)) >=1 else np.NaN)
    
    return city_income
                    