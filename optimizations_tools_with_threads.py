# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:44:13 2022

@author: LSM5
"""


import os
import time
import pandas as pd
import threading
import pickle
from collections import namedtuple

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, fileId, df_list, folder, step,div):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.fileId = fileId
      self.df_list = df_list
      self.folder = folder
      self.step = step
      self.div = div
      
   def run(self):
      print ("Starting " + self.name)
      seperate_Themes(self.name, self.fileId, self.df_list, self.folder, self.step, self.div)
      print ("Exiting " + self.name)
      
      
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

def seperate_Themes(threadName, fileId, df_lists, folder, step,div) :
    
    URI_str =[]
    #Retrieve the list of URIs in each themes
    with open('ByThemes/data_URI_by_themes_'+str(fileId)+'.txt') as f:
        print(".........................................................................")
        print("\nLoading URIs for theme .... 0"+str(fileId)+"  ",folder)
        contents = f.readlines()
        print("\n  Success!!")
    

    for uri in contents[1:]:  
        
        uri = uri.replace("\n", "")
        URI_str.append(uri)



    o=0
    
    partition =int(len(URI_str)/div)
    step_start = step*partition
    step_end = (step+1)*partition
    
    dropList1 = []
    dropList2 = []
    dropList3 = []
    dropList4 = []
   
    DatasetList_Obj = []
    
    if step == div-1:
        step_end = len(URI_str)
                
    for uri in URI_str[step_start:step_end]:
        print(".........................................................................")
        print("\nStart buiding a new dataset")
        o+=1
        start = time.time()
       
        datasetObj = Dataset(uri,[folder],[],[],[],[])
        datasetObj,dropList1 = through_list(uri, df_lists[0], dropList1, datasetObj, titles=True)
        datasetObj,dropList2 = through_list(uri, df_lists[1], dropList2, datasetObj, descriptions=True)
        datasetObj,dropList3 = through_list(uri, df_lists[2], dropList3, datasetObj, keywords=True)
        datasetObj,dropList4 = through_list(uri, df_lists[3], dropList4, datasetObj, distributions=True)
        
        DatasetList_Obj.append(datasetObj)
        print("\n........................................................................." )
        print("\n Msg_dif: 0"+str(o)+" / "+str(len(URI_str[step_start:step_end]))+"  New object added for Label  " +folder+ " %s ...\n" %threadName)
        executionTime = (time.time() - start)
        print(' Msg:   Execution time: ' + str(round(executionTime,2)) + " sec\n")        
     
        
    print('*** *** *** *** *** *** Saving ...'+str(step)+' *** *** *** *** *** *** \n')
    
    with open('Datastets_uni/'+folder+'/Datasets__'+str(step)+'__'+str(o)+'.pkl', 'ab') as outp:
         
            pickle.dump(DatasetList_Obj, outp)
 
    DatasetList_Obj = []    




# main

if __name__ == '__main__':
    

    Titles_ls = load_Attribute_df(name = 'Titles',  path= 'en/Titles')        
    Descriptions_ls = load_Attribute_df(name = 'Descriptions',  path= 'en/Descriptions')        
    Keywords_ls = load_Attribute_df(name = 'Keywords', path= 'en/Keywords')        
    Distributions_ls = load_Attribute_df(name = 'Distributions',  path= 'list_of_attributes/Distributions')        
            
    df_lists = [Titles_ls,Descriptions_ls,Keywords_ls,Distributions_ls]
    
    ###### Create a new datatype to store Dataset elements
    
    Dataset = namedtuple('Dataset', ['uri', 'themeLabels','titles','descriptions','keywords','distributions'])        
    
    
    #define the number of threads and start execution
    print("How many threads do you want to use ?  ")
    div = int(input())
    print('On which folder? Choose between : "inter","energy","health","education","regions","transports","society","economy","government","science","environment","justice","agriculture"')
    folder = input()
    print('Id of the file please ? ')
    fileId = int(input())
    print('you want to start from ? ')
    start = input()
    
    for j in range(start,div):
        Dynamic_variable = "".join(("thread",str(j)))
        vars()[Dynamic_variable] = myThread(j, Dynamic_variable , fileId, df_lists, folder, j, div)
        vars()[Dynamic_variable].start()
        
















