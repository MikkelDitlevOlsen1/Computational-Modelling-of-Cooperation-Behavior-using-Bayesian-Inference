import pandas as pd

def data_processing_adults_func():

    path = 'Data/adults_gain.tsv'

    ug_1 = pd.read_csv(path, sep='\t')  

    ug_1 = ug_1.drop(['ExperimentName', 'SessionDate'], axis=1)

    ug_1.rename(columns = {'subjID':'Subject', 'offer':'receivor', 'accept':'choose'}, inplace = True)

    # Find all unique subjects 
    sub_unique = ug_1['Subject'].unique()

    # Find number of subjects
    number_of_subjects = len(sub_unique)

    # Define subject specific dataframes
    subjects_dataframe_gain = [[]] * number_of_subjects

    for i,subject in enumerate(sub_unique):
        subjects_dataframe_gain[i] = ug_1.loc[ug_1['Subject'] == subject]
    
    return subjects_dataframe_gain

a = data_processing_adults_func()
        
