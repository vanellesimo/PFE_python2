# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:43:57 2022

@author: LSM5
"""

import pickle
import pandas as pd
import matplotlib as plt
from collections import namedtuple
from preprocess_tools import preprocess_text
from sklearn.preprocessing import MultiLabelBinarizer


####Import datas (unpickling process)

Dataset = namedtuple('Dataset', ['uri', 'themeLabels', 'titles', 'descriptions', 'keywords', 'distributions'])

file = open("final_dataset_.pkl", "rb")

Datas = pickle.load(file)

# =============================================================================
# ##### Some tests on titles only
# 
# theme_tiles = Datas[["themes","titles"]]
# theme_tiles.dropna(subset = ["titles"], inplace=True)
# theme_tiles.reset_index(drop=True, inplace=True)
# 
# 
# # creating instance of multilabel binarizer
# mlb = MultiLabelBinarizer()
# a = mlb.fit_transform(theme_tiles.themes)
# pd.DataFrame(a, columns=mlb.classes_)
# 
# ### create the binarize dataframe
# used_df = pd.concat([theme_tiles,pd.DataFrame(a, columns=mlb.classes_)],axis=1)
# used_df_labels = used_df[mlb.classes_]
# 
# # Plotting population for each class
# fig_size = plt.rcParams["figure.figsize"]
# fig_size[0] = 10
# fig_size[1] = 8
# plt.rcParams["figure.figsize"] = fig_size
# 
# used_df_labels.sum(axis=0).plot.bar()
# 
# 
# #### Buiding our inputs and targets arrays
# 
# 
# titles = list(theme_tiles.titles)
# 
# X = preprocess_text(titles)
# 
# =============================================================================


##### Implement the main function

def preprocessings_on_target(target):
    
    theme_target = Datas[["themes",target]]
    theme_target.dropna(subset = [target], inplace=True)
    theme_target.reset_index(drop=True, inplace=True)
    
    
    # creating instance of multilabel binarizer
    mlb = MultiLabelBinarizer()
    a = mlb.fit_transform(theme_target.themes)
    pd.DataFrame(a, columns=mlb.classes_)
    
    ### create the binarize dataframe
    used_df = pd.concat([theme_target,pd.DataFrame(a, columns=mlb.classes_)],axis=1)
    used_df_labels = used_df[mlb.classes_]
    
    # Plotting population for each class
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size
    
    used_df_labels.sum(axis=0).plot.bar()
    
    
    #### Buiding our inputs and targets arrays
    
    
    target_list = list(theme_target[target])
    
    X = preprocess_text(target_list)
    Y = used_df_labels
    
    return (X,Y)













