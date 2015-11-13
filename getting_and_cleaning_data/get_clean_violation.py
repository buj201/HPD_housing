import pandas as pd
import numpy as np
import re

### 

def pull_down_violation_data():
    query = ("https://data.cityofnewyork.us/api/views/wvxf-dwi5/rows.csv?accessType=DOWNLOAD")
    violations = pd.read_csv(query)
    return violations
            
def get_clean_violation_data():
    '''Main function for getting and cleaning violation data'''
    ##Get data
    violations = pull_down_violation_data()
    
    ##Clean and filter data
    violations = violations[['BoroID', 'Block', 'Lot', 'Class', 'ApprovedDate']]
    violations = violations[~(violations.isnull().any(axis=1))]
    violations = violations[violations.BoroID.isin(range(1,6))]
    violations = violations[violations.Class.isin(['A','B','C'])]
    
    violations.ApprovedDate = pd.to_datetime(violations.ApprovedDate)
    start = pd.datetime(2010,4,1)
    end = pd.datetime(2015,3,31)
    allowed_date_range_violation_approval = pd.date_range(start, end, freq='D')
    violations = violations[(violations['ApprovedDate'].isin(allowed_date_range_violation_approval))]
    violations['BBL'] = map(make_BBL, violations['BoroID'], violations['Block'], violations['Lot'])
    violations = violations.drop(['BoroID','Block','Lot'],axis=1)

    ## Group by BBL and class to construct final dataframe with index=BBL and total number of violations, by class, from 04/01/2010 to 03/31/2015 as features.
    
    grouped_by_BBL = violations.groupby(['BBL','Class']).size().reset_index() 
    grouped_by_BBL.columns = ['BBL','Class','Count']
    grouped_by_BBL = grouped_by_BBL.pivot('BBL','Class','Count')
    grouped_by_BBL = grouped_by_BBL.fillna(0)
    grouped_by_BBL['BBL'] = grouped_by_BBL.index
    grouped_by_BBL = grouped_by_BBL.reset_index(drop=True)
    grouped_by_BBL.columns = ['Tot_A_violations','Tot_B_violations','Tot_C_violations','BBL']
    
    return grouped_by_BBL
    
###Helper functions

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
