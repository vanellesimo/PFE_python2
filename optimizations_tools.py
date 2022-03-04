# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:33:04 2022

@author: LSM5
"""
from collections import namedtuple 
import pandas as pd
import time
import pickle
import os

def load_Attribute_df(name,path):
    
    dataframe = pd.DataFrame()
    
    for pd_path in os.listdir(path):
        print(pd_path)
        print("********************************************************************" )
        print("\n Msg_dif:   Local loading"+name+" ...\n" )
        df = pd.read_csv("/".join((path,pd_path)))
        del df['Unnamed: 0']
        dataframe = dataframe.append(df, ignore_index=True)
        print(" Msg:   Success!!! \n")
        
    return dataframe




def through_list(uri,df_list,drops,datasetObj,
                 titles=False,descriptions=False,
                 keywords=False,distributions=False):
   
    count = 0 
    
    dfused_list = df_list.drop(index=drops)
    datasetList = list(dfused_list[dfused_list.columns[0]])
    targetList = list(dfused_list[dfused_list.columns[1]])
    
    for data, target, i  in zip(datasetList,targetList,list(dfused_list.index)):
        if(uri == data):
            drops.append(i)
            if titles : datasetObj.titles.append(target)
            elif descriptions : datasetObj.descriptions.append(target)
            elif keywords : datasetObj.keywords.append(target)
            elif distributions : datasetObj.distributions.append(target)
            else : 
                print("set one param to true please !")
                break
            count += 1
            
            if count == 1:
                
                print("at least one: ___ "+dfused_list.columns[1]+" ___ found")
        
        i+=1
        
    return (datasetObj, drops)



###### Load stored dataframes


Titles_ls = load_Attribute_df(name = 'Titles',  path= 'en/Titles')        
Descriptions_ls = load_Attribute_df(name = 'Descriptions',  path= 'en/Descriptions')        
Keywords_ls = load_Attribute_df(name = 'Keywords', path= 'en/Keywords')        
Distributions_ls = load_Attribute_df(name = 'Distributions',  path= 'list_of_attributes/Distributions')        
        

###### Create a new datatype to store Dataset elements

Dataset = namedtuple('Dataset', ['uri', 'themeLabels','titles','descriptions','keywords','distributions'])        

###### Retrieve URI strings by Themes

#Themes = ["INTR","ENER","HEAL","EDUC","REGI","TRAN","SOCI","ECON","GOVE","TECH","ENVI","JUST","AGRI"]

themefolder = ["inter","energy","health","education","regions","transports","society","economy","government","science","environment","justice","agriculture"]

for i,folder in zip(range(13),themefolder):
    
    URI_str = []
    #Retrieve the list of URIs in each themes
    with open('ByThemes/data_URI_by_themes_'+str(i)+'.txt') as f:
        print(".........................................................................")
        print("\nLoading URIs for theme .... 0"+str(i)+"  ",folder)
        contents = f.readlines()
        print("\n  Success!!")
    

    for uri in contents[1:]:  
        
        uri = uri.replace("\n", "")
        URI_str.append(uri)

    o=0
    j=0
    dropList0 = []  
    dropList1 = []
    dropList2 = []
    dropList3 = []
    dropList4 = []
    DatasetList_Obj = []
                
    for uri in URI_str:
        print(".........................................................................")
        print("\nStart buiding a new dataset")
        o+=1
        start = time.time()
        datasetObj = Dataset(uri,[folder],[],[],[],[])
        datasetObj,dropList1 = through_list(uri, Titles_ls, dropList1, datasetObj, titles=True)
        datasetObj,dropList2 = through_list(uri, Descriptions_ls, dropList2, datasetObj, descriptions=True)
        datasetObj,dropList3 = through_list(uri, Keywords_ls, dropList3, datasetObj, keywords=True)
        datasetObj,dropList4 = through_list(uri, Distributions_ls, dropList4, datasetObj, distributions=True)
        
        DatasetList_Obj.append(datasetObj)
        print("\n........................................................................." )
        print("\n Msg_dif: 0"+str(o)+" / "+str(len(URI_str))+"  New object added for Label  " +folder+ "  ...\n" )
        executionTime = (time.time() - start)
        print(' Msg:   Execution time: ' + str(round(executionTime,2)) + " sec\n")        
        
        if o % 250 == 0:
            i+=1
            print('*** *** *** *** *** *** Saving ... *** *** *** *** *** *** \n')
            
            with open('Dataset_uni/'+folder+'/Datasets__'+str(j*250)+'.pkl', 'ab') as outp:
                 
                    pickle.dump(DatasetList_Obj, outp)
     
            DatasetList_Obj = []    
        
        
    
    
