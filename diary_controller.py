# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:03:41 2020

@author: snbar
"""

import datetime
from datetime import datetime as my_datetime

from app.admin_controller import prep_in_progress
from app.admin_controller import prep_needs_app

from app.database.database import list_appointments_doa_str
from app.database.database import make_new
from app.database.database import db_edit

from app.forms import DiaryForm
from app.forms import MakeTable


def DateString(d):
    datestring=str(d.day).zfill(2)+'/'+str(d.month).zfill(2)+'/'+str(d.year)
    return datestring

#def String_to_date(d):
#    current_date=my_datetime(int(d[6:10]),int(d[3:5]),int(d[0:2]))
#    return current_date

def Convert_to_date(d):
    current_date=my_datetime(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    return current_date

#def get_date_list(current_date):
#    week_date=[]
#    for n in range(5):
#        week_date.append(DateString(current_date-datetime.timedelta(current_date.weekday()-n)))
#    return week_date


def diary_prep1(date):
    print('date',date)
    form=DiaryForm()
    if date=='None':
        print('in none')
        current_date=datetime.datetime.now()
    else:
        print('has date')
        current_date=Convert_to_date(date)
        
    week_date, d, day, time, m_c, appID, details, doa_str, date = ([] for i in range(9))
    day_list=['Monday','Tuesday','Wednesday','Thursday','Friday']
    
    for n in range(5):
        week_date.append(DateString(current_date-datetime.timedelta(current_date.weekday()-n)))
        d.append(current_date-datetime.timedelta(current_date.weekday()-n))

    for n in range(5):
        a=list_appointments_doa_str(week_date[n],'am')
        doa_str.append(week_date[n])
        date.append(d[n])
        time.append('am')
        day.append(day_list[n])
        if a!=None:
            appID.append(a.id)
            m_c.append('cancel')
            details.append(a.patient)
        else:
            appID.append(0)
            m_c.append('make')
            details.append('')
            
        a=list_appointments_doa_str(week_date[n],'pm')
        doa_str.append('')
        date.append(d[n])
        time.append('pm')
        day.append('')
        if a!=None:
            appID.append(a.id)
            m_c.append('cancel')
            details.append(a.patient)
        else:
            m_c.append('make')
            appID.append(0)
            details.append('')
    
    col_values=zip(day,doa_str,time,m_c,appID,details,date)        
#    col_values=diary_prep(current_date)
    
    return form, current_date, col_values

def diary_go_back(form):
    current_date=form.cd.data
    current_date=Convert_to_date(current_date)-datetime.timedelta(7)
    return current_date

def diary_go_forward(form):
    current_date=form.cd.data
    current_date=Convert_to_date(current_date)+datetime.timedelta(7)
    return current_date
    
def diary_select(form):
    current_date=form.dt.data.strftime('%Y-%m-%d')
    current_date=Convert_to_date(current_date) 
    return current_date

def prep_make(date,time):
    current_date=Convert_to_date(date)
    table,a=prep_in_progress([1])

    for app in a:
        print (app.stat)
        app.doa=current_date
        app.time=time

    table = MakeTable(a)
    
    col_values=prep_needs_app()
    
    return col_values,table,current_date

def prep_set_app_date(appID,doa,time):
    my_doa_str=DateString(doa)
    my_list=['doa','doa_str','status','time']
    my_val=[doa,my_doa_str,2,time]
    db_edit('Appointment',appID,my_list,my_val)
    timestamp=datetime.datetime.now()
    my_note='appointment made date: '+ my_doa_str +' time: '+time
    make_new('Notes',{'appID':appID,'note':my_note,'doa':timestamp})

def cancel_appointment(appID):
    my_list=['doa','doa_str','status','time']
    my_val=[None,None,1,None]
    db_edit('Appointment',appID,my_list,my_val)