import pandas as pd
import numpy as np
import re

### 

def pull_down_problem_data():
    query = ("https://data.cityofnewyork.us/api/views/a2nx-4u46/rows.csv?accessType=DOWNLOAD")
    complaint_problems = pd.read_csv(query)
    return complaint_problems
            
def get_clean_problem_data():
    '''Main function- gets data, then cleans it before returning cleaned dataset.'''
    
    ##Get data and exclude open or incomplete cases
    complaint_problems = pull_down_problem_data()
    complaint_problems = complaint_problems.drop(['UnitType', 'SpaceType', 'Type', 'MajorCategory','MinorCategory','Code','Status'],1)
    complaint_problems = complaint_problems[(complaint_problems.StatusID == 2)]
    complaint_problems = complaint_problems[~(complaint_problems.isnull().any(axis=1))]

    ##Note there is an extra whitespace in the SpaceTypeID_ column name
    complaint_problems.columns = ['ProblemID', 'ComplaintID', 'UnitTypeID', 'SpaceTypeID', 'TypeID', 'MajorCategoryID', 'MinorCategoryID', 'CodeID', 'StatusID', 'StatusDate', 'StatusDescription']
    
    ## Validate entries in the ID features
    allowed_UnitTypeID = get_allowed_codes_from_txt('UnitType')
    complaint_problems = complaint_problems[(complaint_problems['UnitTypeID'].isin(allowed_UnitTypeID))]

    allowed_TypeID = get_allowed_codes_from_txt('ProblemType')
    complaint_problems = complaint_problems[(complaint_problems['TypeID'].isin(allowed_TypeID))]
 
    allowed_SpaceTypeID = get_allowed_codes_from_txt('SpaceType')
    complaint_problems = complaint_problems[(complaint_problems['SpaceTypeID'].isin(allowed_SpaceTypeID))]

    allowed_MajorCategoryID = get_allowed_codes_from_txt('MajorCategory')
    complaint_problems = complaint_problems[(complaint_problems['MajorCategoryID'].isin(allowed_MajorCategoryID))]

    allowed_MinorCategoryID = get_allowed_codes_from_txt('MinorCategory')
    complaint_problems = complaint_problems[(complaint_problems['MinorCategoryID'].isin(allowed_MinorCategoryID))]

    allowed_CodeID = get_allowed_codes_from_txt('Code')
    complaint_problems = complaint_problems[(complaint_problems['CodeID'].isin(allowed_CodeID))]
    
    ## Code the status descriptions
    complaint_problems['StatusDescriptionID'] = complaint_problems['StatusDescription'].map(infer_complaint_status)   
    complaint_problems = complaint_problems.drop(['StatusID','StatusDescription'],axis=1)

    ## Convert the StatusDate to pd.datetime
    complaint_problems.StatusDate = pd.to_datetime(complaint_problems.StatusDate)

    return complaint_problems
    
###helper functions###
    
def get_allowed_codes_from_txt(feature_name):
    file_path = 'codebook_for_complaint_problems/' + str(feature_name) + '.txt'
    code_values = pd.read_csv(file_path, header=None)
    code_values = np.array(code_values).flatten().astype(int)
    return code_values

def infer_complaint_status(input_string):
    try:
        input_string = str(input_string)
    except:
        print input_string
    if bool(re.search(r'not\sable\sto\sgain\saccess', input_string)):
        code = 1 
    elif bool(re.search(r'unable\sto\saccess', input_string)):
        code = 1
    elif bool(re.search(r'inspected\sthe\sfollowing\sconditions\.\sNo\sviolations\swere\sissued', input_string)):
        code = 2
    elif bool(re.search(r'Heat\swas\snot\srequired\sat\sthe\stime\sof\sthe\sinspection\.\sNo\sviolations\swere\sissued', input_string)):
        code = 2
    elif bool(re.search(r'\.\sViolations\swere\sissued', input_string)):
        code = 3
    elif bool(re.search(r'\.\sViolations\swere\spreviously\sissued', input_string)):
        code = 4
    elif bool(re.search(r'conditions\swere\scorrected', input_string)):
        code = 5 
    elif bool(re.search(r'advised\sby\sa\stenant', input_string)):
        code = 5
    elif bool(re.search(r'conditions\sare\sstill\sopen', input_string)):
        code = 6
    elif bool(re.search(r'inspection\sto\stest\sthe\spaint\sfor\slead', input_string)):
        code = 7
    elif bool(re.search(r'\.\sA\sSection\s8\sFailure\swas\sissued\.', input_string)):
        code = 8
    else:
        code = 0
    return code