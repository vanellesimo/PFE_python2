# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 09:30:23 2022

@author: LSM5
"""
"""
This script aim to optimize the reconstruction of datasets object through pandas utils only or as much as possible

"""
import os
import time
import fasttext
import pandas as pd
import threading
import pickle
from collections import namedtuple



def load_Attribute_df(name, path):

    dataframe = pd.DataFrame()

    for pd_path in os.listdir(path):
        print(pd_path)
        print("********************************************************************")
        print("\n Msg_dif:   Local loading"+name+" ...\n")
        df = pd.read_csv("/".join((path, pd_path)))
        del df['Unnamed: 0']
        dataframe = dataframe.append(df, ignore_index=True)
        print(" Msg:   Success!!! \n")

    return dataframe

def find_unique(series):
    model = fasttext.load_model('lid.176.ftz')
    chosed = float('NaN')
    xn = u'\n'
    for target in series:
        if xn in target: target = target.replace('\n',' ')
        if  model.predict(target, k=1)[0][0] == '__label__en':
            chosed = target
    return chosed   

def listOfSeries(series):
    return(list(series.values))
   

def createLabeldataFrame():
    datas = []
    ThemeList = ["inter","energy","health","education","regions","transports","society","economy","government","science","environment","justice","agriculture","notheme"]
    
    for fileId,theme in zip(range(14),ThemeList):
        
        # Retrieve the list of URIs in each themes
        with open('ByThemes/data_URI_by_themes_'+str(fileId)+'.txt') as f:
            print(".........................................................................")
            print("\nLoading URIs for theme .... 0"+str(fileId)+"  ", theme)
            contents = f.readlines()
            print("\n  Success!!")
        
        for uri in contents[1:]:
        
            uri = uri.replace("\n", "")
            datas.append((uri,theme))
    
    Labeldf = pd.DataFrame(datas,columns= ('uris','themes'))   
    
    return Labeldf

def filterOnUris(dataframe,func):
    
    #aggregate dataframe to have one line
    df = dataframe.groupby(dataframe[0]).agg({dataframe[1]:[func]})
    
    #create a new dataframe with a known structure"
    new_df = pd.DataFrame({'uris': list(df[df.columns[0][0]][df.columns[0][1]].index), 
                        dataframe[1]: list(df[df.columns[0][0]][df.columns[0][1]].values)})
    return new_df

def mergedataframes(listOfDataframes, target):
    
    #merge on target
    df_final = listOfDataframes[0]
    for i in range(1,len(listOfDataframes)):
        df_final = df_final.merge(listOfDataframes[i],how= 'outer', on='uris')

    return df_final


# main
if __name__ == '__main__':

    #### Load dataframes
    Titles_ls = load_Attribute_df(name='Titles',  path='en/Titles')
    Descriptions_ls = load_Attribute_df(name='Descriptions',  path='en/Descriptions')
    Keywords_ls = load_Attribute_df(name='Keywords', path='en/Keywords')
    Distributions_ls = load_Attribute_df(name='Distributions',  path='list_of_attributes/Distributions')
    
    #### Create Label dataframe
    Labels_ls = createLabeldataFrame()
    
    ## Apply groupby on dtaframes
    Labelsdf = filterOnUris(Labels_ls, listOfSeries)
    Titlesdf = filterOnUris(Titles_ls, find_unique)
    Descriptionsdf = filterOnUris(Descriptions_ls, find_unique)
    Keywordsdf = filterOnUris(Keywords_ls, listOfSeries)
    Distributionsdf = filterOnUris(Distributions_ls, listOfSeries)
    
    listOfDataframes = [Labelsdf, Titlesdf, Descriptionsdf, Keywordsdf, Distributionsdf]
    
    finalData = mergedataframes(listOfDataframes, 'uris')



















