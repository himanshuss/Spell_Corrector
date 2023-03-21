import pandas as pd
import numpy as np
from Levenshtein import ratio
import traceback
import math

# import only system from os
from os import system, name
 
# import sleep to show output for some time period
from time import sleep
############################################################################### 
# define our clear function
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
###############################################################################
## function to clean the files (remove null rows)
def clean_it(frame):
    frame=frame[frame.isna().all(axis=1)==False] ##removing blank rows
    frame=frame.drop_duplicates()
    return frame
###############################################################################
## function to get the column name from user for mapping
def name_it(frame):
    a=frame.columns.to_list()
    count=1
    for i in a:
        print(count," ",i)
        count=count+1
    col_index=0
    
    try:
        col_index=int(input("Please give in range input for column name: "))
        feild_name=a[col_index-1]
    except Exception:
        traceback.print_exc()
    
    return feild_name

# first trying for sure match
# lower case (done)
# short form match
# n-grams match (considering first word only)
# no space all-in-one
###############################################################################
def n_grams(list_name):
    name_len=len(list_name)
    new_list=list()
    st=list_name[0]
    for i in range(name_len):
        new_list.append(st)
        if i<name_len-1:
            st=st+" "+list_name[i+1]
    return new_list
###############################################################################
def exact_match_check(comp,comp_lis):
    #lower and upper case match
    #comp=slave name
    #comp_lis= master list
    #comp_lis=list(df[ms_feild].unique())
    comp=comp.title()
    for i in comp_lis:
        i=str(i)
        i=i.title()
        
        #first case
        if i==comp:
            return i
        
        #n-grams word match word exact match
        spl=i.split(" ")
        n_gram_list=n_grams(spl)
        comp_split_name=comp.split(" ") #first word matching

        if ((comp in n_gram_list)):
            return i
        if (len(comp_split_name[0])>3 and (comp_split_name[0] in n_gram_list)):
            return i
        
        if (len(comp_split_name[0])==1):
            z=comp_split_name[0]+" "+comp_split_name[1]
            if (z in n_gram_list):
                return i

    return comp
        
###############################################################################
def calculate_score(comp,comp_lis,option):
    comp=comp.title()
    score_list=list()
    score_old=0
    for i in comp_lis:
        i=str(i)
        i=i.title()
        
        score=ratio(comp,i)
        score=round(score,2)
        score_list.append(score)
        
        if (math.isclose(score_old, score) or (score_old < score)):
            suggest=i
            score_old=score
        
    score_list.sort(reverse=True)
    
    
    if(score_list[0]!=1):
        entry = {'slave': comp, 'suggestion': suggest, 'score': score_list[0]}
        print(entry)
        return entry
###############################################################################

def mapping(comp,dc):
    if comp in (dc.keys()):
        return dc.get(comp)
    else:
        return comp

## function to mapp feild names from master to slave
def mapp_it(ms,sl):
    try:
        #get the feild name from files
        ms_feild=name_it(ms)
        sl_feild=name_it(sl)

        #list of unique entries from master file
        master_lis=list(ms[ms_feild].unique())
        sl[sl_feild] = sl[sl_feild].apply(exact_match_check,comp_lis=master_lis) ## exact match done

        #score based mapping
        choice=0
        a_list=list()
        a_list.append(sl[sl_feild].apply(calculate_score,comp_lis=master_lis,option=choice))
        for data in a_list:
            data = list(filter(lambda item: item is not None, data))
        result=pd.DataFrame(data)
        result.drop_duplicates(inplace=True)
        result.to_excel("/Users/himanshusahrawat/Library/CloudStorage/OneDrive-O.P.JindalGlobalUniversity/Nestle/results/result.xlsx")
        print("Done !! Please crosscheck the files and Do the required changes in file (result.xlsx). If OK . Press Enter!!")
        input()
        result=pd.read_excel("/Users/himanshusahrawat/Library/CloudStorage/OneDrive-O.P.JindalGlobalUniversity/Nestle/results/result.xlsx")
        #replacing Slave data frame on the basis of threshold
        #get the thresshold value

        threshold=float(input("Provide the threshold to match (e.g. 0.9 for 90%): "))

        #remove rest of the values from dataframe
        result=result[result["score"]>=threshold]

        #replace rest of the values if found any in slave file
        mydict = dict(zip(result['slave'], result['suggestion']))
        sl[sl_feild]=sl[sl_feild].apply(mapping,dc=mydict)

        sl.replace()
        print("Reflecting the changes and creating new SLAVE file")

        return sl
    except Exception:
        traceback.print_exc()


