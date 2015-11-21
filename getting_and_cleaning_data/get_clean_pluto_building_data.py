import pandas as pd
import re

### Read data in from downloaded csv file

def read_in_pluto_data():
    boroughs = {'bronx':'BX.csv', 'brooklyn':'BK.csv', 'Manhattan':'Mn.csv', 'Queens':'QN.csv', "Staten_island":'SI.csv'}
    frames = []
    for borough in boroughs.keys():
        df_name = borough + '_pluto'
        file_path = '../../data/nyc_pluto_15v1/' + boroughs[borough]
        df_name = pd.read_csv(file_path)
        df_name = df_name[['UnitsRes','AssessTot','YearBuilt','YearAlter1','YearAlter2','BBL', 'CT2010']]
        df_name = df_name[(df_name['UnitsRes'] != 0)]
        frames.append(df_name)
    result = pd.concat(frames, ignore_index=True)
    return result

def get_clean_pluto_data():
    #Get Data
    pluto_dat = read_in_pluto_data()
    
    #Process and clean data
    pluto_dat['CT2010'] = pluto_dat['CT2010'].map(proc_tract)
    pluto_dat['YearLastAlter'] = pluto_dat[['YearAlter1','YearAlter2']].max(axis=1)
    pluto_dat = pluto_dat.drop(['YearAlter1','YearAlter2'],axis=1)
    pluto_dat['Avg_value_per_res_unit'] = pluto_dat['AssessTot']/pluto_dat['UnitsRes']
    pluto_dat = pluto_dat[~(pluto_dat.isnull().any(axis=1))]
    pluto_dat['BuildingAge'] = 2015 - pluto_dat['YearBuilt']
    pluto_dat['YearSinceLastAlter'] = 2015 - pluto_dat['YearLastAlter']
    pluto_dat = pluto_dat.drop(['YearBuilt', 'YearLastAlter'],axis=1)
    mask = (pluto_dat['YearSinceLastAlter'] == 2015)
    pluto_dat.loc[mask,'YearSinceLastAlter'] = pluto_dat['BuildingAge']
    pluto_dat = pluto_dat[pluto_dat.BuildingAge < 500]

    return pluto_dat

##Helper functions

def proc_tract(val):
    val = str(val)
    split_val = re.split('\.',val)
    if len(split_val) == 1:
        integer = split_val[0].zfill(4)
        decimal = '00'
    elif len(split_val) == 2:
        integer = split_val[0].zfill(4)
        decimal = split_val[1].ljust(2, '0')
    new_code = integer + decimal
    return new_code