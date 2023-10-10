#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 14:30:20 2022

@author: lost
"""

import json
import os
from my_project_dao import MyProjectDao
from my_project_result import *
from scipy.stats import mannwhitneyu, pearsonr

from numpy import mean, std # version >= 1.7.1 && <= 1.9.1
from math import sqrt

import math

import seaborn as sns

def cmp_mannwhitneyu(data1, data2):
    # compare samples
    stat, p = mannwhitneyu(data1, data2)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distribution (fail to reject H0)')
    else:
        print('Different distribution (reject H0)')


def cohen_d(x,y):
        return (mean(x) - mean(y)) / sqrt((std(x, ddof=1) ** 2 + std(y, ddof=1) ** 2) / 2.0)
    
    
def print_cmp_mannwhitneyu_cohen_d(data, y_name, key):
    todos = data[data["Languages"] == key]
    todosSim = todos[todos["Co-evolution"] == "High"]
    todosNao = todos[todos["Co-evolution"] == "Low"]
    
    print(y_name, key)
    #print(todosNao[[y_name]])
    #die;
    cmp_mannwhitneyu(todosSim[[y_name]], todosNao[[y_name]])
    print("cohen_d", cohen_d(todosSim[[y_name]], todosNao[[y_name]]))
    print("---")

def get_key_language(project_result):
    
    if project_result.project_language == 'javascript':
       return 0
            
    if project_result.project_language == 'java':
       return 1
        
    if project_result.project_language == 'python':
       return 2
        
    if project_result.project_language == 'php':
       return 3
   
    if project_result.project_language == 'c#':
       return 4

def check_coevolution(serie1, serie2):
    return pearsonr(serie1, serie2)[0]

def get_box_plot_data(labels, bp):
    rows_list = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i*2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i*2)+1].get_ydata()[1]
        rows_list.append(dict1)

    return rows_list

def save_json_log(dir, repositorie_id, data):
    #print(dir, repositorie_id, data)
    file_path = dir+repositorie_id+".json"       
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)
        
def save_csv_log(dir, project_result_id, conteudo):
        f = open(os.path.join(dir,project_result_id+".csv"),"w+", encoding="utf-8")
        f.write("{}\r\n".format(conteudo))
        f.close()

def get_JSON(dir):
    if os.path.exists(dir) == True:
        with open(dir) as json_file:
            return json.load(json_file)
    return False

def clean_create_dir(dir):
    if os.path.exists(dir) == True:
        os.system("rm -rf {my_directory}".format(my_directory= dir))
     
    os.mkdir(dir)
    
def prepare_get_name_with_virg(list, len_prev, indice_start, pos_start):
    stop = (pos_start+(len(list)-len_prev))
    #print(indice_start, stop)
    return ','.join(list[indice_start:stop])

def get_valid_ids():
    my_project_dao = MyProjectDao()
            
    return my_project_dao.get_valid_ids()
    