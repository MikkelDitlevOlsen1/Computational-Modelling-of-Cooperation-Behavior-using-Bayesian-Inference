import pandas as pd
import numpy as np


## load answers
path = 'Data/Raw_ug/raw/CCNP_raw/data/CCNP_merge_wave1.csv'

ug_1 = pd.read_csv(path)  
print(ug_1)
ug_1 = ug_1.dropna()
ug_1 = ug_1.drop(['sub', 'wave','trail','ExperimentName','SessionDate'], axis=1)


# Convert choose to 1 = accepted and 0 = rejected
ug_1['choose'][ug_1.choose != '拒绝'] = 1
ug_1['choose'][ug_1.choose == '拒绝'] = 0



sub_unique = ug_1['Subject'].unique()
print(len(sub_unique))
#Find number of subjects
number_of_subjects = len(sub_unique)
print(sub_unique)
ug_1 = ug_1.groupby('Subject').agg({'choose': list, 'receivor': list , 'Wait2.RT' :list , 'targettext': list})

# Reset the index to make 'subject' a column
ug_1 = ug_1.reset_index()


## load demografiks
path = 'Data/Raw_ug/raw/CCNP_raw/demographic/delete_redundent_age_information.csv'

demo_1 = pd.read_csv(path) 


demo_1 = demo_1.drop(['birth_date', 'scan_date','wave','rural/urban','ethnicity'], axis=1)

print(demo_1)
#merge
merge_df = pd.merge(ug_1, demo_1, on='Subject')


#load svo
path= 'Data/svo/SVO_As.csv'
svo_1 = pd.read_csv(path) 


merge_df = pd.merge(merge_df, svo_1, on='Subject')


merge_df.to_csv('Data/all_combined.csv', index = False)