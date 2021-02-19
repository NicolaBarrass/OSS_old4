# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:22:16 2021

@author: snbar
"""


# import read_c3d
import get_c3d_data
import c3d_plotgraphs
# import matplotlib.pyplot as plt
#import numpy as np

#import c3d_markers
                
attr_list=['kin','mkr']                 
filename = 'C:\\Users\\snbar\\projects\\Data\\Pats20\\Misc\\APatient\\Helen_NF_N\\Helen_NF_N07.c3d'
#f=read_c3d.read_c3d(filename,attr_list)

f=get_c3d_data.main(filename,attr_list)

if 'kin' in attr_list:
    c3d_plotgraphs.plot_graphs(f.kin)

#if 'mkr' in attr_list:
#    c3d_plotgraphs.Nexus(f.mkr)   

class make_class(object):
    def __init__(self,att_list): 
        for r in att_list:
            setattr(self, r,[])