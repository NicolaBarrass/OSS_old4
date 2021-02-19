# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:15:51 2021

@author: snbar
"""

##### next need to resample data to get 51 or 101 points
##### need to read kinetics as well and display this
##### create methods for averaging and plotting data bands
##### set limits on graphs and draw zero line on, change graph colours


##### read in markers and draw stick man in 3D - allow user to scroll through

import ezc3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import numpy as np
import operator
import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


class kin_plot(object):
    def __init__(self):
        self.c3dname=[]
        self.DimensionName=[]
        self.GraphNo=[]
        self.KineticsNo=[]
        self.DefaultRange=[]
        self.NormFactor=[]
                            
class event(object):
    def __init__(self):
        self.label=[]
        self.frame=[]  
        
def read_data(required_data,filename):
    c = ezc3d.c3d(filename)
    
    Bodymass=c['parameters']['PROCESSING']['Bodymass']['value'][0]
    Bodyweight=Bodymass*100
    norm_factor={'none':1, 'Bodyweight':Bodyweight,'10':10}
           
    frame_rate=c['header']['points']['frame_rate']
    first_frame=c['header']['points']['first_frame']
    last_frame=c['header']['points']['last_frame']
    
    no_events =c['parameters']['EVENT']['USED']['value'][0]
    event_frames=(np.round(c['parameters']['EVENT']['TIMES']['value'][1]*120)).astype(int)-first_frame
    event_labels =c['parameters']['EVENT']['LABELS']['value']
    event_contexts = c['parameters']['EVENT']['CONTEXTS']['value']
    
    R_stride=[]
    L_stride=[]
    for n in range(no_events):
        if event_contexts[n]=='Right' and event_labels[n]=='Foot Strike':
            R_stride.append(event_frames[n])
        if event_contexts[n]=='Left' and event_labels[n]=='Foot Strike':
            L_stride.append(event_frames[n])
    
    
    print(required_data)
    # get index value for each parameter in angle_list
#    try:
#        required_data
#        print('exists')
    angle_indexL=[]
#    angle_indexR=[None]*len(required_data.kin)
    print(dir(required_data))
    for n in range(c['parameters']['POINT']['USED']['value'][0]):
        if c['parameters']['POINT']['LABELS']['value'][n] in dir(required_data):
            print(n,c['parameters']['POINT']['LABELS']['value'][n])
            rsetattr(required_data,c['parameters']['POINT']['LABELS']['value'][n]+'.x',c['data']['points'][0][n][min(L_stride):max(L_stride)])
            rsetattr(required_data,c['parameters']['POINT']['LABELS']['value'][n]+'.y',c['data']['points'][1][n][min(L_stride):max(L_stride)])
            rsetattr(required_data,c['parameters']['POINT']['LABELS']['value'][n]+'.z',c['data']['points'][2][n][min(L_stride):max(L_stride)])
##                if c['parameters']['POINT']['LABELS']['value'][n][0]=='L':
#            angle_indexL[required_data.index(c['parameters']['POINT']['LABELS']['value'][n])].append(n)
##                if c['parameters']['POINT']['LABELS']['value'][n][0]=='R':
##                    angle_indexR[required_data.c3dname.index(c['parameters']['POINT']['LABELS']['value'][n][1::])]=n
##    except:
##        print('does not exist')
##        angle_index=[None]*len(required_data.c3dname)
##        for n in range(c['parameters']['POINT']['USED']['value'][0]):
##            if c['parameters']['POINT']['LABELS']['value'][n] in required_data.c3dname:
##                angle_index[required_data.c3dname.index(c['parameters']['POINT']['LABELS']['value'][n])]=n
##    # for each parameter in angle_list read data into correct attribute
#    if hasattr(required_data, 'NormFactor'):
#        for a in range(len(required_data.c3dname)):
##            for d in range(3):
#            if required_data.DimensionName[a][d] is not None:
#                setattr(required_data.x,'L'+required_data.DimensionName[a][d],c['data']['points'][d][angle_indexL[a]][min(L_stride):max(L_stride)]/norm_factor[required_data.NormFactor[a]])
#                setattr(required_data.x,'R'+required_data.DimensionName[a][d],c['data']['points'][d][angle_indexR[a]][min(R_stride):max(R_stride)]/norm_factor[required_data.NormFactor[a]])
#    else:
#        for a in range(len(required_data.c3dname)):
#            if required_data.c3dname[a] is not None:
#                for d in range(3):
#                    setattr(t,required_data.DimensionName[a][d],c['data']['points'][d][angle_index[a]][min(L_stride):max(L_stride)])
##                    setattr(t,'R'+required_data.DimensionName[a][d],c['data']['points'][d][angle_indexR[a]][min(R_stride):max(R_stride)])
     
    return required_data
