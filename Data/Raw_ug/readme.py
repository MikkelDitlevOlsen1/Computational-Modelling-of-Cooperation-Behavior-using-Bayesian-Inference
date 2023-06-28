#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:07:17 2023

@author: laixinyu
"""
import pandas as pd
import io
import numpy as np


#%%
#some progress has been made, for example, adults and CCNP demographic data has been updated. Now the age variables are all in contineous format
#and previously, there's some paricipants doesn't have coresspoding demographic data in CCNP, and now it's updated
#for adults cohort, their subjID started with "A"
#for twins cohort, their subjID started with "T"or "NT",  pin the behavior and demographic data according to subjID and session date
#for CCNP cohort, their subjID are just natural integer

#%%pin CCNP_UG and CCNP_demographic
#read beh data
# CCNP_merge_wave1, the variable "trail" is already created
df_beh = pd.read_csv('/Users/laixinyu/Desktop/output/CCNP/input/CCNP_merge_wave1.csv')
#read demographic
df_age = pd.read_csv('/Users/laixinyu/Desktop/output/CCNP/input/delete_redundent_age_information.csv')
df_merge =pd.merge(df_beh, df_age, on='Subject', how='left')
#create "context" variable for further analysis
df_merge['context'] = np.where(df_merge['ExperimentName'].str.contains('gain'), 'gain',
                            np.where(df_merge['ExperimentName'].str.contains('loss'), 'loss', ''))
#Encode variable names according to the requirements of the hbayes package
df_merge.rename(columns = {'Subject' : 'subjID', 'receivor' : 'offer', 'choose': 'accept'}, inplace = True)
#Rename the variables, with the "offer" variable defining fairness level and the "choose" variable numerically encoded,"gender" with F or M
df_merge['offer'] = df_merge['offer'].replace({-9: 1, -8: 2,-7: 3, -6: 4, -5: 5})#df_merge['offer'] = df_merge['offer'].replace({1: "extreamly unfair", 2: "very unfair", 3: "moderately unfair", 4: "slightly unfair", 5: "equal fair"})
df_merge['accept'] = df_merge['accept'].replace({'接受': 1, '拒绝': 0})
df_merge['gender'] = df_merge['gender'].replace({'female': 'F', 'male': 'M'})
# define cohort according to the age 
df_merge['cohort'] = pd.cut(df_merge['age'], bins=[0, 10, 18, float('inf')], labels=['children', 'adolescence', 'adult'])
# Converts the 'Subject' column to integer type
df_merge['subjID'] = df_merge['subjID'].astype(int)
#Judge whether the data merge is correct
count_age = df_merge.groupby('subjID')['age'].nunique()
# Selects subjects with multiple age values
multi_age_subj = count_age[count_age.gt(1)].index.tolist()
# Calculate the number of rows per subjID that appear in both gain and loss contexts
result = df_merge.groupby(['subjID', 'context']).size().reset_index(name='count')
not_40_subjID = result.loc[result['count'] != 40, 'subjID'].unique()
# Print a subjID with a count value other than 40 （in our desigh, each context has 40 trails）
print(not_40_subjID)

#%% pin Adult_UG and adult_demographic
# read the original text
with open('/Users/laixinyu/Desktop/output/adults/input/adultmerge.txt', mode='r', encoding='UTF-16') as f:
    text = f.read()
# Encode the original text to utf-8
utf8_text = text.encode('utf-8')
# Converts the encoded text to a data frame
df_original = pd.read_csv(io.StringIO(utf8_text.decode('utf-8')), delimiter='\t')
df_beh = df_original[["ExperimentName","Subject","SessionDate","choose","receivor", "Wait2.RT","targettext"]]
#filter the variables that we want, and create "context" variable
df_age = pd.read_csv('/Users/laixinyu/Desktop/output/adults/input/adult_participant_list_toDanyuandMikkel.csv')
df_merge =pd.merge(df_beh, df_age, on='Subject', how='left')
df_merge['context'] = np.where(df_merge['ExperimentName'].str.contains('gain'), 'gain',
                            np.where(df_merge['ExperimentName'].str.contains('loss'), 'loss', ''))
#delete empty trail
df_merge = df_merge.dropna(subset=['choose'])
##Encode variable names according to the requirements of the hbayes package
df_merge.rename(columns = {'Subject' : 'subjID', 'receivor' : 'offer', 'choose': 'accept'}, inplace = True)
#Rename the variables, with the "offer" variable defining fairness level and the "choose" variable numerically encoded,"gender" with F or M
df_merge['offer'] = df_merge['offer'].replace({-9: 1, -8: 2,-7: 3, -6: 4, -5: 5})
df_merge['offer'] = df_merge['offer'].replace({1: "extreamly unfair", 2: "very unfair", 3: "moderately unfair", 4: "slightly unfair", 5: "equal fair"})
df_merge['accept'] = df_merge['accept'].replace({'接受': 1, '拒绝': 0})
df_merge['cohort'] = pd.cut(df_merge['age'], bins=[0, 10, 18, float('inf')], labels=['children', 'adolescence', 'adult'])
#rename subjID，Just add a "A" beofre subjIID
subjID_list = df_merge['subjID'].unique().tolist()
subjID_dict = {}
for i, subjID in enumerate(subjID_list):
    new_name = 'A{}'.format(i+1)
    subjID_dict[subjID] = new_name
df_merge['subjID'] = df_merge['subjID'].replace(subjID_dict)
#Since adults data are relatively clean, I did't really have any check measure for this data

#%% pin Twins_UG and twins_demographic.
# twins real subjID in the demographic table is called "indentifier", encoded with "T"or"NT" and some numbers. 
#However, due to the fact that the e-prime software (data collection software) can't read string varaible, so the "Subject" column in UG data doesn't have the "T" or "NT"
#in the following procedure, you should be aware that we pin the data on "Subject" and "SessionDate", but the real subjID should be the "identifier"
with open('/Users/laixinyu/Desktop/output/twins/input/twinsmerge.txt', mode='r', encoding='UTF-16') as f:
    text = f.read()
#  Encode the original text to utf-8
utf8_text = text.encode('utf-8')
# Converts the encoded text to a data frame
df_original = pd.read_csv(io.StringIO(utf8_text.decode('utf-8')), delimiter='\t')
print(df_original)
#filter the variables that we want
df_beh = df_original[["ExperimentName","Subject","SessionDate","choose","receivor", "Wait2.RT","targettext"]]
#read demo
df_age = pd.read_csv('/Users/laixinyu/Desktop/output/twins/input/participantlist_Twins.csv')
# convert the date column to pandas datetime object
df_age["SessionDate"] = pd.to_datetime(df_age["SessionDate"])
# format the datetime object to the desired string format
df_age["SessionDate"] = df_age["SessionDate"].dt.strftime('%m-%d-%Y')
#merge the data depending the subject ID and experimental date
df_merge =pd.merge(df_beh, df_age, on=['Subject','SessionDate'], how='left')
df_merge['context'] = np.where(df_merge['ExperimentName'].str.contains('gain'), 'gain',
                            np.where(df_merge['ExperimentName'].str.contains('loss'), 'loss', ''))
#delete empty trail
df_merge = df_merge.dropna(subset=['choose'])
##Encode variable names according to the requirements of the hbayes package
df_merge.rename(columns = {'identifier' : 'subjID','Subject' : 'backup', 'receivor' : 'offer', 'choose': 'accept'}, inplace = True)
#Rename the variables, with the "offer" variable defining fairness level and the "choose" variable numerically encoded,"gender" with F or M
df_merge['offer'] = df_merge['offer'].replace({-9: 1, -8: 2,-7: 3, -6: 4, -5: 5})
#df_merge['offer'] = df_merge['offer'].replace({1: "extreamly unfair", 2: "very unfair", 3: "moderately unfair", 4: "slightly unfair", 5: "equal fair"})
df_merge['accept'] = df_merge['accept'].replace({'接受': 1, '拒绝': 0})
df_merge['cohort'] = pd.cut(df_merge['age'], bins=[0, 10, 18, float('inf')], labels=['children', 'adolescence', 'adult'])
count_age = df_merge.groupby('subjID')['age'].nunique()
# #Judge whether the data merge is correct, saying that one subject couldn't have more than one age
multi_age_subj = count_age[count_age.gt(1)].index.tolist()
# calculate trails
result = df_merge.groupby(['subjID', 'context']).size().reset_index(name='count')
not_40_subjID = result.loc[result['count'] != 40, 'subjID'].unique()
# print abnormal subj ID
print(not_40_subjID)



