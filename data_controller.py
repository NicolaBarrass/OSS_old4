# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:50:34 2020

@author: snbar
"""
from flask import render_template, flash, redirect, url_for, request, Response, send_file
from collections import defaultdict

from app.database.database import db_list_orderby
from app.database.database import make_new
from app.database.database import db_edit

from app.database.database import append_conditions
from app.database.database import append_trials
from app.database.database import db_get_id
from app.database.database import db_get_exam

from app.classess import DateString, Convert_to_date, String_to_date
from app.classess import Item, Item2, Item3

from matplotlib.backends.backend_agg import FigureCanvasAgg

from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig
import random

import datetime
from datetime import datetime as my_datetime




exam_meas=['hipflex','hipflexdef','hipabdflex','hipabdext','hiprotint','hiprotext','femant',
           'kneeffd','kneehyp','popliteal','kneeflexflex','kneeflexext',
           'mdfflex','mfdext','bimal']



#class app_list(object):
#    def __init__(self):
#        self.id=[]
#        self.doa_str=[]
#        self.doa=[]
#        self.cond_list=[]
#    
#class cond_list(object):
#    def __init__(self):
#        self.id=[]
#        self.footware=[]
#        self.walking_aid=[]
#        self.trial_list=[]
#        
#class tri_list(object):
#    def __init__(self):
#        self.id=[]
#        self.c3dfile=[]
#        
#class DateList(object):
#    def __init__(self):
#        self.id=[]
#        self.doa_str=[]
#        self.time=[]
#        self.m_c=[]
#        self.appID=[]
#        self.details=[]
#        self.day=[]
#
#class Tree(object):
#    def __init__(self):
#        self.id=[]
#        self.name=[]
#        self.type=[]

#def get_everything_patient(appID):
#    this_a=db_get_id('Appointment',{'id':appID})#id',appID)
#    print('date:',(this_a.doa))
#    print('date:',type(this_a.doa))
#    p=db_get_id('Patient',{'id':this_a.patID})
#    a=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
##    a.sort()
##    c=blank_condition()
#    a_list=app_list()
#    c_list=cond_list()
#    t_list=tri_list()
#    i_c=0
#    i_t=0
#    tree_list=Tree()
#    count=0
#
#    for my_a in a:
#        a_list.id.append(my_a.id)
#        a_list.doa_str.append(my_a.doa_str)
#        a_list.doa.append(my_a.doa)
#        c=append_conditions([my_a.id])
##        c=db_inlist('Condition','Condition.appID',[my_a.id])
#        condition_list=[]
#        tree_list.id.append(count)
#        tree_list.name.append(my_a.doa_str)
#        tree_list.type.append('app')
#        count=count+1
#        for my_c in c:
#            print(my_c.id)
#            c_list.id.append(my_c.id)
#            c_list.footware.append(my_c.footware)
#            c_list.walking_aid.append(my_c.walking_aid)
#            condition_list.append(i_c)
#            i_c=i_c+1
#            t=append_trials([my_c.id])
#            trial_list=[]
#            tree_list.id.append(count)
#            tree_list.name.append('   '+my_c.footware+' '+my_c.walking_aid)
#            tree_list.type.append('cond')
#            count=count+1
#            for my_t in t:
#                t_list.id.append(my_t.id)
#                t_list.c3dfile.append(my_t.c3dfile)
#                trial_list.append(i_t)
#                i_t=i_t+1
#                tree_list.id.append(count)
#                tree_list.name.append('      '+my_t.c3dfile)
#                tree_list.type.append('trial')
#                count=count+1
#            c_list.trial_list.append(trial_list)               
#        a_list.cond_list.append(condition_list)
#        
#    name_values=tree_list.name
#    type_values=tree_list.type   
#    col_values=zip(name_values,type_values)
#
#    return p,a_list,c_list,t_list,tree_list,col_values
    
#def prep_kinematics():  
#    fig = Figure()
#    axis = fig.add_subplot(1, 1, 1)
#    xs = range(100)
#    ys = [random.randint(1, 50) for x in xs]
#    axis.plot(xs, ys)
#    return fig,axis
    
def get_exam(appID,s):
    e=db_get_exam(appID,s)
    try:
        print(e.id)
    except:
#    print("result len", len(e.all()))
#    if len(e)==0:
#        print('need to make an exam instance')
        make_new('Exam',{'appID':appID,'side':'L'})
        make_new('Exam',{'appID':appID,'side':'R'})
        e=db_get_exam(appID,s)
#    print('after making exam instance length of results is: ',len(e.all()))
    return e

def save_exam(form,appID,LexamID, RexamID):
    my_list_L=[]
    my_list_R=[]
    for nm in exam_meas:
        my_list_L.append(request.form[nm+'L'])
        my_list_R.append(request.form[nm+'R'])
       
    db_edit('Exam',LexamID[0],exam_meas,my_list_L)
    db_edit('Exam',RexamID[0],exam_meas,my_list_R)

    



def prep_exam(appID):
    LexamID=[]
    RexamID=[]  
    appIDs=[]
    dates=[]
    date_list=[]
    years=[]
    items=[]
    combined=[]
    combined2=[]
    left_exam=[]
    right_exam=[]
    lists=defaultdict(list)
    
    this_a=db_get_id('Appointment',{'id':appID})#id',appID)
    p=db_get_id('Patient',{'id':this_a.patID})
    a=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
    for my_a in a:
        appIDs.append(my_a.id)
        dates.append(my_a.doa_str)
        date_list.append(my_a.doa)

    for date in dates:
        years.append(date[6:10])
#    
    for ID in appIDs:
        print('appID: ',appIDs)
        exam=get_exam(ID,'L')
        
        
#    for exam in left_exam:
#        print('left exam:',exam.id,exam.appID,exam.hipflex)
        LexamID.append(exam.id)
        for nm in exam_meas:
            lists['L'+nm].append(getattr(exam,nm))
            
        exam=get_exam(ID,'R')   
#    for exam in right_exam:
        RexamID.append(exam.id)
        for nm in exam_meas:
            lists['R'+nm].append(getattr(exam,nm))
           
    for nm in exam_meas:
        items.append(Item(nm, lists['L'+nm][0], lists['R'+nm][0]))
           
    for nm in exam_meas:
        combined.append(Item2(nm, lists['L'+nm] + lists['R'+nm]))
        
    for nm in exam_meas:
        combined2.append(Item3(nm, lists['L'+nm] , lists['R'+nm]))
    
    return p, items, LexamID, RexamID, combined, years,combined2
    