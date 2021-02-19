# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:37:15 2019

@author: Nicky
"""
from app import db
from app.models import Patient, Appointment, Condition, Trial, Notes, Finding,Status,Staff,Folder
from app.models import Evidence, Findinglist, Evidencelist, History, Sidelist, Exam, Stafflist
from app.models import Referrer, Referrerlist, Diagnosis, Diagnosislist, History, Historytemplate, HistoryNotes
from sqlalchemy import and_

### get all data from given table
def db_all_table(table_name):
    constructor = globals()[table_name]
    a=constructor.query.all()
    return a

### diary    
def list_appointments_doa_str(d,t):
    appointments=Appointment.query.filter((Appointment.doa_str==d) & (Appointment.time==t)).first()
    return appointments
  
def db_appointment_status(l):
    appointments=Appointment.query.filter(Appointment.status.in_ (l))
    return appointments

### to edit existing row in table with given id
### my_list is list of attributes to change and my_val is list of values 
### to assign to attributes    
def db_edit(table_name,ID,my_list,my_val):
    constructor = globals()[table_name]
    a=constructor.query.filter_by(id=ID).first()    
    for n in range(len(my_list)):
        setattr(a,my_list[n],my_val[n])   
    db.session.commit() 
    
### get data from table where id is my_id    (single data row)
def db_get_id(table_name,kwargs):
    constructor = globals()[table_name]
    p=constructor.query.filter_by(**kwargs).first()
    return p

### lists all rows from database where conditions are true
def db_list(table_name,kwargs):
    constructor = globals()[table_name]
    p=constructor.query.filter_by(**kwargs)
    return p

def db_list_orderby(table_name,date,kwargs):
    constructor = globals()[table_name]
    p=constructor.query.filter_by(**kwargs).filter(constructor.doa<=date).order_by(constructor.doa.desc())
    return p
  
### make new row in table and set initial variables
def make_new(table_name,kwargs):
    constructor = globals()[table_name]
    t = constructor(**kwargs)
    db.session.add(t)
    db.session.commit()

## this does not work yet - it will replace append_conditions and append_trials    
def db_inlist(table_name,att,my_list):
    constructor = globals()[table_name]
#    this_att=globals()[att]
    c=[constructor.query.filter_by(appID=id) for id in my_list]
#    [Shoe.query.filter_by(id=id).one() for id in my_list_of_ids]
    return c

def append_conditions(my_list):
    constructor = globals()['Condition']
    print(dir(constructor))
    conditions=Condition.query.filter(Condition.appID.in_(my_list))
    print('in append conditions')
    for c in conditions:
        print (c.id)
    return conditions

def append_trials(my_list):
    trials=Trial.query.filter(Trial.condID.in_(my_list))
    print('in append trials')
    for t in trials:
        print (t.id)
    return trials

def db_get_exam(ID,s):
    e=Exam.query.filter(and_(Exam.appID==ID, Exam.side==s)).first()
    return e

def db_get_history(ID):
    e=History.query.filter(History.appID==ID)
    return e

def db_count_history(ID):
    e=History.query.filter(History.appID==ID).count()
    return e

def db_count_historynotes(ID):
    e=HistoryNotes.query.filter(HistoryNotes.appID==ID).count()
    return e

def db_make_exam(thisappID):
    print('in database making exam instance')
    e=Exam(appID=int(thisappID),side='L')
    db.session.add(e)
    db.session.commit()
    e=Exam(appID=int(thisappID),side='R')
    db.session.add(e)
    db.session.commit()
    