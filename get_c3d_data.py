# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:35:38 2021

@author: snbar
"""
import ezc3d
# import functools
import numpy as np
# import operator

no_kin_points=51

#def rsetattr(obj, attr, val):
#    pre, _, post = attr.rpartition('.')
#    print(pre,post)
#    return setattr(rgetattr(obj, pre) if pre else obj, post, val)
#
#def rgetattr(obj, attr, *args):
#    def _getattr(obj, attr):
#        return getattr(obj, attr, *args)
#    return functools.reduce(_getattr, [obj] + attr.split('.'))

kin_list=['PelvisAngles','HipAngles','KneeAngles','AnkleAngles','FootProgressAngles',
          'HipMoment','KneeMoment','KneeMoment','AnkleMoment',
          'HipPower','KneePower', 'AnklePower']

mkr_list=['ASI','PSI','THI','KNE','TIB','ANK','HEE','TOE']


class dim_data(object):
    def __init__(self):
        self.x=[]
        self.y=[]
        self.z=[]
        
class kin_c3d(object):
    def __init__(self): 
        for r in range(len(kin_list)):
            for s in ['L','R']:
                setattr(self, s+kin_list[r],[])
                
class mkr_c3d(object):
    def __init__(self): 
        for r in range(len(mkr_list)):
            for s in ['L','R']:
                setattr(self, s+mkr_list[r],[])
                
                
class info_c3d(object):
    def __init__(self):
        self.bodyweight=[]
        self.L_stride=[]
        self.R_stride=[]
        
class setup_c3d(object):
    def __init__(self):
        self.kin=[]
        self.mkr=[]
        
        
                
xyz=dim_data()

def main(filename,attr_list):
    c = ezc3d.c3d(filename)
    info = get_stride_info(c)
    f=setup_c3d()
    if 'kin' in attr_list:
        f.kin = get_kin_data(c, info)
    if 'mkr' in attr_list:
        f.mkr = get_mkr_data(c, info)

    return f

def get_stride_info(c):
    info=info_c3d()
    Bodymass=c['parameters']['PROCESSING']['Bodymass']['value'][0]
    info.bodyweight=Bodymass*100
#    norm_factor={'none':1, 'Bodyweight':Bodyweight,'10':10}
           
    frame_rate=c['header']['points']['frame_rate']
    first_frame=c['header']['points']['first_frame']
    last_frame=c['header']['points']['last_frame']
    
    no_events =c['parameters']['EVENT']['USED']['value'][0]
    event_frames=(np.round(c['parameters']['EVENT']['TIMES']['value'][1]*120)).astype(int)-first_frame
    event_labels =c['parameters']['EVENT']['LABELS']['value']
    event_contexts = c['parameters']['EVENT']['CONTEXTS']['value']
    
#    R_stride=[]
#    L_stride=[]
    for n in range(no_events):
        if event_contexts[n]=='Right' and event_labels[n]=='Foot Strike':
            info.R_stride.append(event_frames[n])
        if event_contexts[n]=='Left' and event_labels[n]=='Foot Strike':
            info.L_stride.append(event_frames[n])
    return info
#b=numpy.interp(np.arange(0, len(a), len(a)/101), np.arange(0, len(a)), a)
def get_kin_data(c,info):
    print('create holder for kin data')
    
    t=kin_c3d()
    norm=[]
    for n in range(c['parameters']['POINT']['USED']['value'][0]):
        if c['parameters']['POINT']['LABELS']['value'][n] in dir(t):
            xyz=dim_data()
            if 'Moment' in c['parameters']['POINT']['LABELS']['value'][n]:
                norm=info.bodyweight
            elif 'Power' in c['parameters']['POINT']['LABELS']['value'][n]:
                norm=10
            else:
                norm=1
            if c['parameters']['POINT']['LABELS']['value'][n][0]== 'L': 
                a=c['data']['points'][0][n][min(info.L_stride):max(info.L_stride)]/norm
                xyz.x=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][1][n][min(info.L_stride):max(info.L_stride)]/norm
                xyz.y=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][2][n][min(info.L_stride):max(info.L_stride)]/norm
                xyz.z=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                setattr(t,c['parameters']['POINT']['LABELS']['value'][n],xyz)
            else:
                a=c['data']['points'][0][n][min(info.R_stride):max(info.R_stride)]/norm
                xyz.x=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][1][n][min(info.R_stride):max(info.R_stride)]/norm
                xyz.y=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][2][n][min(info.R_stride):max(info.R_stride)]/norm
                xyz.z=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                setattr(t,c['parameters']['POINT']['LABELS']['value'][n],xyz)
          
    return t

def get_mkr_data(c,info):
    print('create holder for mkr data')
    
    t=mkr_c3d()
    norm=[]
    for n in range(c['parameters']['POINT']['USED']['value'][0]):
        if c['parameters']['POINT']['LABELS']['value'][n] in dir(t):
            xyz=dim_data()
            if c['parameters']['POINT']['LABELS']['value'][n][0]== 'L': 
                a=c['data']['points'][0][n][min(info.L_stride):max(info.L_stride)]
                xyz.x=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][1][n][min(info.L_stride):max(info.L_stride)]
                xyz.y=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][2][n][min(info.L_stride):max(info.L_stride)]
                xyz.z=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                setattr(t,c['parameters']['POINT']['LABELS']['value'][n],xyz)
            else:
                a=c['data']['points'][0][n][min(info.R_stride):max(info.R_stride)]
                xyz.x=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][1][n][min(info.R_stride):max(info.R_stride)]
                xyz.y=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                a=c['data']['points'][2][n][min(info.R_stride):max(info.R_stride)]
                xyz.z=np.interp(np.arange(0, len(a), len(a)/no_kin_points), np.arange(0, len(a)), a)
                setattr(t,c['parameters']['POINT']['LABELS']['value'][n],xyz)
    
    return t