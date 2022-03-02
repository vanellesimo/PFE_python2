# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:39:24 2022

@author: LSM5
"""


import time
import math
import fasttext
import pandas as pd
from langdetect import detect, DetectorFactory


DetectorFactory.seed = 0

def filterOnEnglish(dataframe):
    
    i=0
    k=0
    xn = u'\n'
    xa = u'\xa0'
    xt = u'\t'
    drops = []
    liste = []
    dfX = dataframe
   
    model = fasttext.load_model('lid.176.ftz')
        
    for target in list(dfX[dfX.columns[1]]):
        
        if xn in target: target = target.replace('\n',' ')
        if xa in target: target = target.replace(u'\xa0', u' ')
        if xt in target: target = target.replace(u'\t', u' ')
        
        
        k=0
        
        for t in target:
            if t.isdigit():
                k+=1
        if k>= 2*len(target)/3:
            pass
    
        else:        
            try:
                if (detect(target)!= 'en') and (model.predict(target, k=1)[0][0] != '__label__en'):
                    print("====================================================================\n" )
                    print(target)
                    if target not in liste: liste.append(target) 
                    print("\n Msg_dif:   Found at position" +str(i)+ "  ...\n" )
                    drops.append(i)
                    #time.sleep(1)
            except TypeError:
                print ('An error occured on this target value " '+target+' "')
                time.sleep(1.2)
                print ('\nWarning!!! We consider this value but Further verification is mandatory')
            except Exception:
                print("====================================================================\n" )
                print ("LangDetect brings up a warning but continue ...")
# =============================================================================
#                 print('Do you want this  ? (y/n) : ', target)
#                 decision = input()
#                 
#                 if decision == 'y':
#                     pass
#                 else:
# =============================================================================
                print("====================================================================\n" )
                print(target)
                if target not in liste: liste.append(target) 
                print("\n Msg_dif:   Found at position" +str(i)+ "  ...\n" )
                drops.append(i)
            
            
        i+=1    
    
    return (drops,liste)


def load_filter_Attribute_df(name,pathvalue=0):
    
    
    if pathvalue == 0: #Titles
        path = 'list_of_attributes/Titles/Titlelist__'
        path_en = "en_Titles_ds"
    else:
        path = 'list_of_attributes/Descriptions/Descriptionlist__'
        path_en = "en_Descriptions_ds"
        
    for r in range(10,22):  
        dataframe = pd.DataFrame()
        drops = []
        liste = []
        print(r)
        print("********************************************************************" )
        print("\n Msg_dif:   Local loading"+name+" ...\n" )
        
        df = pd.read_csv(path+str((r-1)*40000)+'_to_'+str(r*40000)+'.csv')
        del df['Unnamed: 0']
        df.dropna(subset = [df.columns[1]], inplace = True)
        
        dataframe = df
        print(" Msg:   Success!!! \n")
        print("Processing on ...."+str(len(dataframe))+" datas")
        time.sleep(1.2)
        
        ########## filter step #########
        
        drops,liste = filterOnEnglish(dataframe)
        en_dataframe = dataframe.reset_index(drop = True)
        en_dataframe = en_dataframe.drop(index=drops)
        en_dataframe.to_csv('en/'+path_en+str(r-10)+'.csv') 
        
    return dataframe

###### Load stored dataframes

# =============================================================================
# Titles_ls = pd.read_csv('list_of_attributes/Titles/Titlelist__360000.csv')
# Descriptions_ls = pd.read_csv('list_of_attributes/Descriptions/Descriptionlist__360000.csv')
# Keywords_ls = pd.read_csv('list_of_attributes/Keywords/Keywordlist__360000.csv')
# 
# del Titles_ls ['Unnamed: 0']
# del Descriptions_ls['Unnamed: 0']
# del Keywords_ls['Unnamed: 0']
# =============================================================================


# =============================================================================
# Titles_ls = load_Attribute_df(name = 'Titles', dataframe = Titles_ls, path= 'list_of_attributes/Titles/Titlelist__')        
# Descriptions_ls = load_Attribute_df(name = 'Descriptions', dataframe = Descriptions_ls, path= 'list_of_attributes/Descriptions/Descriptionlist__')        
#  
# Descriptions_ls.dropna(subset = ["descriptions"], inplace=True)
# 
#        
# =============================================================================

# Suppress non english attributes
# We first retrive all the indexes non english attributes




#2 9, 3 10, 4 11, 5 12, 6 13







