# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:50:14 2020

@author: snbar
"""
import datetime
from datetime import datetime as my_datetime

def DateString(d):
    datestring=str(d.day).zfill(2)+'/'+str(d.month).zfill(2)+'/'+str(d.year)
    return datestring

def Convert_to_date(d):
    current_date=my_datetime(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    return current_date

def String_to_date(d):
    current_date=my_datetime(int(d[6:10]),int(d[3:5]),int(d[0:2]))
    return current_date

def get_date_list(current_date):
    week_date=[]
    for n in range(5):
        week_date.append(DateString(current_date-datetime.timedelta(current_date.weekday()-n)))
    return week_date

class Tablelist(object):
    def __init__(self):
        self.condition=[]
        self.staff=[]
        self.folder=[]
        self.referrer=[]

class Report_var(object):
    def __init__(self):
        self.name=[]
        self.dob_str=[]
        self.hosp_no=[]
        self.NHS_no=[]
        self.doa_str=[]
        self.referrer=[]
        self.collector=[]
        self.processor=[]
        self.writer=[]
        self.reviewer=['Martin Gough']
        self.age=''
        self.items=[]
        self.combined=[]
        self.combined2=[]
        self.years=[]
        self.LexamID=[]
        self.RexamID=[]
        self.apps=[]
        self.history=[]
        self.historynotes=[]
        self.c3d=[]

class app_list(object):
    def __init__(self):
        self.id=[]
        self.doa_str=[]
        self.doa=[]
        self.cond_list=[]
        
        
class Item(object):
    def __init__(self, name, left, right):
        self.name = name
        self.nameL = name+'L'
        self.nameR = name+'R'
        self.left = left
        self.right = right
        
class Item2(object):
    def __init__(self, name, kwargs):
        self.name = name
        self.nameL = name+'L'
        self.nameR = name+'R'
        if len(kwargs)>=1:
            self.D1 = kwargs[0]
        if len(kwargs)>=2:    
            self.D2 = kwargs[1]
        if len(kwargs)>=3:    
            self.D3 = kwargs[2]
        if len(kwargs)>=4:    
            self.D4 = kwargs[3]
            
class Item3(object):
    def __init__(self, name, l_list,r_list):
        self.name = name
        self.nameL = name+'L'
        self.nameR = name+'R'
        self.dataL=l_list
        self.dataR=r_list
        
class c3d(object):
    def __init__(self):
        self.filename = []
        self.markers=[]
        self.kinematics=[]
        self.events=[]
        self.kinetics=[]
        self.emg=[]
        
class markers(object):
    def __init__(self): 
        self.LTOE=[]
        self.RTOE=[]        
