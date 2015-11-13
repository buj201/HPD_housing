import pandas as pd

### Read data in from downloaded csv file

def read_in_pluto_data():
    boroughs = {'bronx':'BX.csv', 'brooklyn':'BK.csv', 'Manhattan':'Mn.csv', 'Queens':'QN.csv', "Staten_island":'SI.csv'}
    frames = []
    for borough in boroughs.keys():
        df_name = borough + '_pluto'
        file_path = 'data/nyc_pluto_15v1/' + boroughs[borough]
        df_name = pd.read_csv(file_path)
        df_name = df_name[['UnitsRes','AssessTot','YearBuilt','YearAlter1','YearAlter2','BBL','Tract2010']]
        df_name = df_name[(df_name['UnitsRes'] != 0)]
        frames.append(df_name)
    result = pd.concat(frames, ignore_index=True)
    return result

def clean_pluto_data():
    pluto_dat = read_in_pluto_data()
    pluto_dat['YearLastAlter'] = pluto_dat[['YearAlter1','YearAlter2']].max(axis=1)
    pluto_dat = pluto_dat.drop(['YearAlter1','YearAlter2'],axis=1)
    pluto_dat['Avg_value_per_res_unit'] = pluto_dat['AssessTot']/pluto_dat['UnitsRes']
    pluto_dat = pluto_dat[~(pluto_dat.isnull().any(axis=1))]
    return pluto_dat
