import pandas as pd
import numpy as np

def data_processing_func():

    path = 'Data/step3_format_csv/UG_wave1.csv'

    ug_1 = pd.read_csv(path)  

    # Delete all rows containin
    # g NaN
    ug_1 = ug_1.dropna()

    # Delete unnecessary columns
    ug_1 = ug_1.drop(['SessionDate', 'SessionTime', 'type'], axis=1)

    # Convert choose to 1 = accepted and 0 = rejected
    ug_1['choose'][ug_1.choose != '�ܾ�'] = 1
    ug_1['choose'][ug_1.choose == '�ܾ�'] = 0

    # Find all unique subjects 
    sub_unique = ug_1['Subject'].unique()

    # Find number of subjects
    number_of_subjects = len(sub_unique)

    # Creat a dictionary with subjectID and index
    #subjectID = {}
    #for idx, person in enumerate(sub_unique):
    #    subjectID[idx] = person
    #
    #array = np.array(list(subjectID.items()))
    #np.save('Data/subjectID_index.npy', array)


    # Define subject specific dataframes
    subjects_dataframe = [[]] * number_of_subjects
    subjects_dataframe_gain = [[]] * number_of_subjects
    subjects_dataframe_loss = [[]] * number_of_subjects


    for i,subject in enumerate(sub_unique):
        subjects_dataframe[i] = ug_1.loc[ug_1['Subject'] == subject]
        subjects_dataframe_gain[i] = subjects_dataframe[i][subjects_dataframe[i].Context == 'gain']
        subjects_dataframe_loss[i] = subjects_dataframe[i][subjects_dataframe[i].Context == 'lose']

    return subjects_dataframe, subjects_dataframe_gain, subjects_dataframe_loss


a,b,c=data_processing_func()

