import pandas as pd
import numpy as np
import re

### 

def pull_down_complaint_data():
    query = ("https://data.cityofnewyork.us/api/views/uwyv-629c/rows.csv?accessType=DOWNLOAD")
    complaints = pd.read_csv(query)
    return complaints
   
def get_clean_complaint_data():
    '''Main function- gets complaints, then process raw data'''
    ##Get data
    complaints = pull_down_complaint_data()
    
    ##Filter data
    complaints = complaints.drop(['BuildingID','Borough','HouseNumber','StreetName','Zip','Apartment','CommunityBoard','StatusID','Status','StatusDate'],axis=1)
    complaints.ReceivedDate = pd.to_datetime(complaints.ReceivedDate)
    complaints = complaints[complaints.BoroughID.isin(range(1,6))]

    start = pd.datetime(2014,11,1)
    end = pd.datetime.now()
    allowed_date_range = pd.date_range(start, end, freq='D')
    complaints = complaints[(complaints['ReceivedDate'].isin(allowed_date_range))]
    complaints['BBL'] = map(make_BBL, complaints['BoroughID'], complaints['Block'], complaints['Lot'])
    complaints = complaints.drop(['Block','Lot'], axis=1)
    return complaints

##Helper functions:

def make_BBL(borough, block, lot): 
    '''
    The borough code is one numeric digit. 
    The tax block is one to five numeric digits, preceded with leading zeroswhen the block is less than five digits.
    The tax lot is one to four digits and is preceded with leading zeros when the lot is less than four digits.
    
    >>> make_BBL(1,16,100)
    1000160100
    >>> make_BBL(3,15828,7501)
    3158287501
    '''
    return int(str(borough) + str(block).zfill(5) + str(lot).zfill(4))
 