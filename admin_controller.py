# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:18:30 2019

@author: Nicky
"""
from app.files.files import pdf_list
from app.files.files import open_pdf

from app.database.database import db_all_table
from app.database.database import make_new
from app.database.database import db_edit
from app.database.database import db_appointment_status
from app.database.database import db_get_id

from app.forms import NeedsAppTable
from app.forms import InProgressTable
from app.forms import RegisterForm

from app.classes import String_to_date




import datetime
from datetime import datetime as my_datetime


from matplotlib.backends.backend_agg import FigureCanvasAgg

from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig
import random
import io
from flask import Flask, Response, request




REFERRER_FOLDER="C:\\Users\\snbar\\projects\\Referrals"
DATA_FOLDER="C:\\Users\\snbar\\projects\\Data"
s={1:'Registered',2:'App made',3:'Attended',4:'Processed',5:'Written',6:'Reported'}

        




































### admin ###
def prep_in_progress(lst):
    if lst==[3]:
        a=db_appointment_status([3])
        attended=InProgressTable(a)
        a=db_appointment_status([4])
        processed=InProgressTable(a)
        a=db_appointment_status([5]) 
        written=InProgressTable(a)
        return attended,processed,written
    if lst==[1]:
        a=db_appointment_status([1])
        table = NeedsAppTable(a)
        return table,a
    if lst==[2]:
        a=db_appointment_status([2])
        table = InProgressTable(a)
        return table
###
def set_status(appID,status):
    db_edit('Appointment',appID,['status'],[status])

def prep_referral():
    my_list=pdf_list(REFERRER_FOLDER,'.pdf')
    return my_list

def prep_register():
    form=RegisterForm()
    return form
    
def prep_register_OK1(form):
    hosp_no=form.number.data
    p=db_get_id('Patient',{'hosp_no':hosp_no})
    try: # check if patient was found - if not it will go to except
        p.id
        message="Patient "+hosp_no+ " already exists. Please check details below"
        new="no"
    except:
        message="Patient "+hosp_no+ " does not exist, please enter details below."
        new="yes"
    return hosp_no,p,new,message

def prep_register_OK2(form):
    w=form.when.data
    status=1
    if w=='Delayed':
        when_comment= form.when_comment.data
    if w=='ASAP':
        when_comment="ASAP"+form.when_comment.data
    
    hosp_no=form.number.data
    name=form.name.data
    surname=form.surname.data
    p=db_get_id('Patient',{'hosp_no':hosp_no})
    if p==None:
        make_new('Patient',{'name':name,'surname':surname,'hosp_no':hosp_no})
        p=db_get_id('Patient',{'hosp_no':hosp_no})
    make_new('Appointment',{'status':status,'patient':p,'when':when_comment})

def open_letter(letter):
    open_pdf(REFERRER_FOLDER,letter)

def all_table(table_name):
    a=db_all_table(table_name)
    return a
    
def save_patient_details(form,my_id):
    print('testing finding form data: ',form.dob_str.data)
    dob_str=form.dob_str.data
    dob=String_to_date(dob_str)
    
    my_list=['name','surname','dob','dob_str','NHS_no']
    my_val=[form.name.data,form.surname.data,dob,dob_str,form.NHS_no.data]
    db_edit('Patient',my_id,my_list,my_val)

def save_appointment_details(form,my_id):
    print('testing finding form data: ',form.status.data)

def prep_needs_app():
    a=db_appointment_status([1])
    details,status,appID=([] for i in range(3))
    for app in a:
        details.append(app.patient)
        status.append(s[app.status])
        appID.append(app.id)
    col_values=zip(details,status,appID)
    return col_values

def prep_kinematics():  
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

def save_trials(trial_list,ttype,condID):
    for trial in trial_list:
        make_new('Trial',{'condID':condID,'c3dfile':trial,'ttype':ttype})  
        
def prep_change_status(id,appID):
    if id==2:
        url='app_made'
    if id in [3,4,5]:
        url='in_progress'
    set_status(appID,id+1)
    return url  

def prep_notes(appID):
    n=notes_list(appID)
    table=NotesTable(n)      

############ new #############################################################
def new_condition(appID,footware,walking_aid):
    make_new('Condition',{'appID':appID,'footware':footware,'walking_aid':walking_aid})   

def new_staff(appID,role,staffID):
    make_new('Staff',{'appID':appID,'role':role, 'stafflistID':int(staffID)})

def new_folder(appID,ftype,folder):
    make_new('Folder',{'appID':int(appID),'ftype':ftype,'folder':folder})  
    
def new_referrer(appID,refID):
    make_new('Referrer',{'appID':int(appID),'refID':refID}) 
    
def new_diagnosis(patID,diagnosisID):
    make_new('Diagnosis',{'patID':int(patID),'diagnosisID':diagnosisID})
       


