# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 19:58:49 2020

@author: snbar


"""
from flask import render_template, flash, redirect, url_for, request, Response, send_file
from collections import defaultdict

from app.forms import PatientTable, AppointmentTable, ConditionTable, TrialTable
from app.forms import ExamDbTable, StaffTable
from app.forms import FolderTable, ReferrerTable, DiagnosisTable

from app.forms import PatientForm,AppointmentForm,ConditionForm,TrialForm 
from app.forms import FolderSelect,TrialSelect,ReferrerSelect 
from app.forms import StaffSelect,DiagnosisSelect,ConditionSelect

from app.files.files import pdf_list
from app.files.files import folder_file_list

from app.classes import Report_var, Tablelist
from app.classes import Item, Item2, Item3

from app.database.database import make_new
from app.database.database import db_edit
from app.database.database import db_get_id
from app.database.database import db_list_orderby
from app.database.database import db_get_exam
from app.database.database import db_get_history
from app.database.database import db_count_history
from app.database.database import db_count_historynotes
from app.database.database import db_all_table
from app.database.database import db_list

import app.get_c3d_data as get_c3d_data

from app.c3d_controller import make_graph
from app.c3d_controller import plot_kinematics
from app.c3d_controller import plot_kinetics
from app.c3d_controller import plot_bokeh

DATA_FOLDER="C:\\Users\\snbar\\projects\\"
exam_meas=['hipflex','hipflexdef','hipabdflex','hipabdext',
           'hiprotint','hiprotext','femant',
           'kneeffd','kneehyp','popliteal','kneeflexflex','kneeflexext',
           'mdfflex','mfdext','bimal']


class make_class(object):
    def __init__(self,att_list): 
        for r in att_list:
            setattr(self, r,[])
            
## database_controller###################################################        
######### patient, appointment, condition, trial ########################
def prep_patient(patID):
    p=db_get_id('Patient',{'id':patID})
    table = AppointmentTable(p.appointment)
    form = PatientForm()   
    return table,p,form

def save_patient_details(form,my_id):
    dob_str=form.dob_str.data
    dob=String_to_date(dob_str)
    
    my_list=['name','surname','dob','dob_str','NHS_no']
    my_val=[form.name.data,form.surname.data,dob,dob_str,form.NHS_no.data]
    db_edit('Patient',my_id,my_list,my_val)
    
def prep_appointment(appID):       
    form = AppointmentForm()
    tables=Tablelist()
    a=db_get_id('Appointment',{'id':appID})
    tables=[ConditionTable(a.condition),StaffTable(a.staff),
            FolderTable(a.folder),ReferrerTable(a.referrer)]    
    return tables,form,a

def respond_appointment(form,appID,a):
    sub=request.form['submitButton']
    if sub=="Open report":
        return redirect(url_for('report', appID=appID))
    if sub=="Open notes":
        return redirect(url_for('notes', appID=appID))
    if sub=="Add staff":
        return redirect(url_for('add_staff', appID=appID))
    if sub=="Select folders":
        return redirect(url_for('add_folder', appID=appID,path='Data',ftype='photo'))
    if sub=="Select referrer":
        return redirect(url_for('add_referrer', appID=appID))
    if sub=="Make new condition":
        return redirect(url_for('add_condition', appID=appID))
    if sub=="Go back to patient":
        new_id=a.patID
        return redirect(url_for('patient', patID = new_id))



def prep_condition(condID):
    form = ConditionForm()
    c=db_get_id('Condition',{'id':condID})
    table = TrialTable(c.trial)    
    return form,table,c

def prep_trial(trialID):
    form = TrialForm()
    c=db_get_id('Trial',{'id':trialID})  
    return form,c

######## add folder, referrer, staff, diagnosis, trial, condition
def prep_add_folder(appID,path): 
    full_path=DATA_FOLDER+path
    f=db_list('Folder',{'appID':appID})
    folder_table=FolderTable(f)
    form=FolderSelect()
    my_list=folder_file_list(full_path)
    f2_list=[['','']]
    for mf in my_list:
        f2_list.append([mf,mf])
    form.path_select.choices=f2_list    
    return form,folder_table

def prep_add_referrer(appID): 
    f=db_list('Referrer',{'appID':appID})
    referrer_table=ReferrerTable(f)
    form=ReferrerSelect()
    my_list=db_all_table('Referrerlist')
    f2_list=[['','']]
    for mf in my_list:
        f2_list.append([mf.id,mf.RefSurname])
    form.ref_select.choices=f2_list    
    return form,referrer_table

def prep_add_staff(appID): 
    f=db_list('Staff',{'appID':appID})
    staff_table=StaffTable(f)
    form=StaffSelect()
    my_list=db_all_table('Stafflist')
    f2_list=[['','']]
    for mf in my_list:
        f2_list.append([mf.id,mf.name+' '+mf.surname])
    form.staff_select.choices=f2_list    
    return form,staff_table

def prep_add_diagnosis(patID): 
    f=db_list('Diagnosis',{'patID':patID})
    diagnosis_table=DiagnosisTable(f)
    form=DiagnosisSelect()
    my_list=db_all_table('Diagnosislist')
    f2_list=[['','']]
    for mf in my_list:
        f2_list.append([mf.id,mf.diagnosis+' '+mf.category+' '+mf.description])
    form.diagnosis_select.choices=f2_list    
    return form,diagnosis_table

def prep_add_trial(condID,appID):
    t=db_list('Trial',{'condID':condID})
    trial_table=TrialTable(t)
    form=TrialSelect()    
    # get appID info, get folder where ftype is data
    a=db_get_id('Folder',{'appID':appID,'ftype':'data'})
    try:
        my_list=pdf_list('C:\\Users\\snbar\\projects\\'+a.folder,'.c3d')
    except:
        my_list=[]
    try:
        data_folder=a.folder
    except:
        data_folder='None'
        
    return form,trial_table,data_folder,my_list

def prep_add_condition(appID):
    t=db_list('Condition',{'appID':appID})
    condition_table=ConditionTable(t)
    form=ConditionSelect()            
    return form,condition_table

######### report getting date ######################################
def get_basics(appID,rep_data):
#    report_var=Report_var()
    this_a=db_get_id('Appointment',{'id':appID})    
        
    all_apps=db_list('Appointment',{'patID':this_a.patID})
    # all_apps=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
    # report_var.apps=a
    att_list=[]
    for i_a,a in enumerate(all_apps):
        att_list.append('apps')
    rep_data=make_class(att_list)
    rep_data.apps=all_apps
    
    for a in all_apps:
        # print(a.doa_str)
        for c in a.condition:
            # print(c.footware)
            for t in c.trial:
                # print(t.c3dfile)
                setattr(t,'c3d',get_c3ddata2(t.c3dfile))
    # print('in get basics')     
    # for a in rep_data.apps:
    #     print(a.doa_str)
    #     for c in a.condition:
    #         print(c.footware)
    #         for t in c.trial:
    #             # print(t.c3dfile)
    #             # print(dir(t.kin))
    #             print(t.c3d.kin.LPelvisAngles.x)
                
    #### create kinematic and kinetic graphs ###
    plot_kinematics(rep_data)
    plot_kinetics(rep_data)
    layout = plot_bokeh(rep_data)
    
    # for i_a,a in enumerate(all_apps):
    #     all_conds=db_list('Condition',{'appID':a.id})
    #     att_list=[]
    #     for i_c,c in enumerate(all_conds):
    #         att_list.append('cond'+str(i_c))
    #     c_class=make_class(att_list)
    #     for i_c,c in enumerate(all_conds):
    #         setattr(a,'cond'+str(i_c),c)
    #         all_trials=db_list('Trial',{'condID':a.id})
    #         for i_t,t in enumerate(all_trials):
    #             setattr(c,'trial'+str(i_t),t)
    #             t=get_c3ddata2(t) # reads c3d data
    #         # add calculate cond averages and STs
    #         setattr(c_class,'cond'+str(i_c),c)
    #     # add read clinical exam data
    #     # add read all other data - photos, US
    #     setattr(rep_data,'app'+str(i_a),a) 
            
            
    # print(rep_data.app0.cond0.footware)
    # print(rep_data.app0.cond0.trial0.c3dfile)
    # print(rep_data.app0.doa)
    # print(rep_data.app0.patient.name)
    # print(rep_data.app0.cond0.trial0.c3d.kin.LPelvisAngles.x)
    # print('#######')

    att_list=['name','dob_str','hosp_no','NHS_no','doa_str']
    val_list=[this_a.patient,this_a.patient.dob_str,this_a.patient.hosp_no,
              this_a.patient.NHS_no,this_a.doa_str]
    for n in range(len(att_list)):
        try:
            setattr(rep_data,att_list[n],val_list[n])
            # print('setting ',att_list[n])
        except:
            setattr(rep_data,att_list[n],'') 
    # print('name: ',report_var.name)
    # return report_var,this_a, rep_data
    return rep_data, layout

def get_c3ddata2(t):
    attr_list=['kin','mkr']  
# C:\Users\snbar\projects\Data\Pats20\CP\APatient\APatient20-feb-20               
    filename = 'C:\\Users\\snbar\\projects\\Data\\Pats20\\CP\\APatient\\APatient20-feb-20\\' + t 
    v=get_c3d_data.main(filename,attr_list)
    # setattr(t,'c3d',v)
    return v

# def get_c3ddata(rep_data):
#     attr_list=['kin','mkr']                 
#     filename = 'C:\\Users\\snbar\\projects\\Data\\Pats20\\Misc\\APatient\\Helen_NF_N\\Helen_NF_N07.c3d'   
#     setattr(rep_data,'c3d',get_c3d_data.main(filename,attr_list))
#     print(rep_data.c3d.kin.LPelvisAngles.x)
#     return rep_data


def prep_video(appID):
    report_var,this_a,rep_data=get_basics(appID,report_var)    
    return report_var

def prep_report(appID,rep_data):
    print('preparing report')
    rep_data, layout =get_basics(appID,rep_data)
    # print(rep_data.app0.cond0.footware)
    # rep_data = get_c3ddata(rep_data)
    print('in prep report')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
    return rep_data, layout

def prep_export(appID,report_var):   
    ### gets appointment info
    # report_var,this_a, rep_data=get_basics(appID,report_var)
    # report_var=get_c3ddata(report_var,this_a)
    # report_var,a=get_prep_exam(report_var,appID,this_a)
    # a=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
    # report_var.apps=a  
    
    print('name: ',report_var.name)
    print(report_var.c3d.kin.LPelvisAngles.x)
    ### saves app info (name etc, referrer, staff) into report_var
    try:
        setattr(report_var,'referrer',this_a.referrer[0].referrer)
    except:
        setattr(report_var,'referrer','')    

    for n in range(len(this_a.staff)):
        if this_a.staff[n].role in ['holder','measurer']:
            report_var.collector.append(this_a.staff[n].stafflist)
        if this_a.staff[n].role in ['processor']:
            report_var.processor.append(this_a.staff[n].stafflist)
        if this_a.staff[n].role in ['writer']:
            report_var.writer.append(this_a.staff[n].stafflist)
        if this_a.staff[n].role in ['reviewer']:
            report_var.reviewer.append(this_a.staff[n].stafflist)
    ### get exam data into report_var
    print('name: ',report_var.name)
    report_var,a=get_prep_exam(report_var,appID,this_a)
    print('name',report_var.name)
    print(this_a.condition)
    print(report_var.apps)
    print(report_var.c3d.kin.LPelvisAngles.x)
    return report_var,this_a

def get_exam(appID,s):
    e=db_get_exam(appID,s)
    try:
        print(e.id)
    except:
        make_new('Exam',{'appID':appID,'side':'L'})
        make_new('Exam',{'appID':appID,'side':'R'})
        e=db_get_exam(appID,s)
    return e

def save_exam(form,appID,LexamID, RexamID):
    my_list_L=[]
    my_list_R=[]
    for nm in exam_meas:
        my_list_L.append(request.form[nm+'L'])
        my_list_R.append(request.form[nm+'R'])       
    db_edit('Exam',LexamID[0],exam_meas,my_list_L)
    db_edit('Exam',RexamID[0],exam_meas,my_list_R)

    
def prep_exam(appID,report_var):
    report_var,this_a, rep_data=get_basics(appID,report_var)
    report_var,a=get_prep_exam(report_var,appID,this_a)
    return report_var,a

def get_prep_exam(report_var,appID,this_a):
    lists=defaultdict(list)

    a=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
    for my_a in a:
        report_var.years.append(my_a.doa_str[6:10])
        exam=get_exam(my_a.id,'L')
        report_var.LexamID.append(exam.id)
        for nm in exam_meas:
            lists['L'+nm].append(getattr(exam,nm))           
        exam=get_exam(my_a.id,'R')   
        report_var.RexamID.append(exam.id)
        for nm in exam_meas:
            lists['R'+nm].append(getattr(exam,nm))
           
    for nm in exam_meas:
        report_var.items.append(Item(nm, lists['L'+nm][0], lists['R'+nm][0]))
        report_var.combined.append(Item2(nm, lists['L'+nm] + lists['R'+nm]))
        report_var.combined2.append(Item3(nm, lists['L'+nm] , lists['R'+nm]))     
    return report_var,a

def prep_kinematics(appID,report_var):
    report_var,this_a, rep_data=get_basics(appID,report_var) 
    report_var=get_c3ddata(report_var,this_a)
    a=db_list_orderby('Appointment',(this_a.doa),{'patID':this_a.patID})
    report_var.apps=a     
    return report_var

def get_history(appID):
    c=db_count_history(appID)
    if c >0:
        e=db_get_history(appID)
    else:
        h=db_all_table('Historytemplate')
        for hist in h:
            make_new('History',{'appID':appID,'text':hist.text,
                                'title':hist.title})
        e=db_get_history(appID)
    return e

def prep_history(appID):
    print('prep history')
    report_var,this_a, rep_data=get_basics(appID,report_var) 
    ### check if history already exists
    report_var.history=get_history(appID)
    
          
    return report_var,this_a

def prep_phonehistory(appID):
    print('prep phonehistory')
    report_var,this_a, rep_data=get_basics(appID,report_var) 
    ### check if history already exists
    report_var.history=get_history(appID)
    ### check if history_notes already exist for this app
    c=db_count_historynotes(appID)
    print(c)
    if c >0:
        h=db_get_id('HistoryNotes',{'appID':appID})
    else:
        make_new('HistoryNotes',{'appID':appID})
        h=db_get_id('HistoryNotes',{'appID':appID})
#    for j in h:
    report_var.historynotes=h
      
    return report_var,this_a

def save_history_notes(form,report_var,this_a):
    print('history notes id:', report_var.historynotes.id)
    print(form.speaker.data)
    print(form.ascends.data)
    print(form.current_box.data)
    print(form.ck1.data)
    print(form.ck2.data)
    print(form.ck3.data)
    my_id=report_var.historynotes.id
    my_list=['speaker','relationship','diff_box',
             'ascends','descends','stairfeet','kerbs','wheelchair',
             'max_distance','condition','stopped_by','current_box',
             'year','changes','limiting','activities','interventions',
             'physio_name','physio_centre','physio_frequency','physio_programme',
             'AFOS','afo_description','afo_worn','afo_comment']
    my_val=[form.speaker.data,form.relationship.data, form.diff_box.data,
            form.ascends.data,form.descends.data,form.stairfeet.data,form.kerbs.data,form.wheelchair.data,
            form.max_distance.data,form.condition.data,form.stopped_by.data,form.current_box.data,
            form.year.data,form.changes.data,form.limiting.data,form.activities.data,form.interventions.data,
            form.physio_name.data,form.physio_centre.data,form.physio_frequency.data,form.physio_programme.data,
            form.AFOS.data,form.afo_description.data,form.afo_worn.data,form.afo_comment.data]
    db_edit('HistoryNotes',my_id,my_list,my_val)

def prep_any_database(page):
    title=page+' Database'
    p=db_all_table(page)
    if page=='Patient':
        table = PatientTable(p)
    if page=='Appointment':
        table = AppointmentTable(p)
    if page=='Condition':
        table = ConditionTable(p)
    if page=='Exam':
        table = ExamDbTable(p)
    if page=='Trial':
        table = TrialTable(p)
    return title,table

