# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:22:18 2021

@author: snbar
"""

import c3dreader
#import ezc3d
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker 
#import numpy as np
#import operator
#from mpl_toolkits.mplot3d import axes3d
#from matplotlib.animation import FuncAnimation
import PIG_defs

def read_c3d(filename,attr_list):  
       
    val_list=[]
    val_list2=[]
                 
    class file_def(object):
            def __init__(self):
                for index,at in enumerate(attr_list):
                    setattr(self,at,val_list[index])
#                    setattr(self,at,val_list2[index])
    class dim_data(object):
        def __init__(self):
            self.x=[]
            self.y=[]
            self.z=[]
                    
############# information relating to markers ############################    
    if 'mkr' in attr_list: 
        
        t = PIG_defs.mkr()
        t=c3dreader.read_data(t,filename)    
        val_list.append(t)
#        val_list2.append(required_data)

        
    if 'kin' in attr_list:     
        t = PIG_defs.kin()
        t=c3dreader.read_data(t,filename)     
#        val_list.append(t)
        val_list.append(t)
#        
    p=file_def() 
    return p