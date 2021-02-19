from flask import render_template, flash, redirect, url_for, request, Response, send_file,session
import io
#import btk
import pickle
import numpy as np
import sys
import os
import ezc3d
import app.get_c3d_data as get_c3d_data

# from app.classes import rep_data

from app import app

from app.forms import ExamForm
from app.forms import HistoryForm
from app.forms import PhoneHistoryForm
#from app.forms import PhoneCheckboxForm
from app.forms import ExportForm

### diary ###
from app.diary_controller import cancel_appointment
from app.diary_controller import diary_prep1
from app.diary_controller import diary_go_back
from app.diary_controller import diary_go_forward
from app.diary_controller import diary_select
from app.diary_controller import prep_make
from app.diary_controller import prep_set_app_date

### admin ###
from app.admin_controller import prep_in_progress
from app.admin_controller import prep_referral
from app.admin_controller import prep_register
from app.admin_controller import prep_register_OK1
from app.admin_controller import prep_register_OK2
from app.admin_controller import open_letter
from app.admin_controller import all_table
from app.admin_controller import new_condition
from app.admin_controller import new_folder
from app.admin_controller import save_patient_details
from app.admin_controller import save_appointment_details
from app.admin_controller import new_staff
from app.admin_controller import save_trials
from app.admin_controller import prep_change_status
from app.admin_controller import new_referrer
from app.admin_controller import new_diagnosis
from app.admin_controller import prep_notes

### database ###
from app.database_controller import prep_patient
from app.database_controller import prep_appointment
from app.database_controller import respond_appointment
from app.database_controller import prep_condition
from app.database_controller import prep_trial
from app.database_controller import prep_add_folder
from app.database_controller import prep_add_trial
from app.database_controller import prep_add_referrer
from app.database_controller import prep_add_staff
from app.database_controller import prep_add_diagnosis
from app.database_controller import prep_add_condition
from app.database_controller import prep_report
from app.database_controller import prep_export
from app.database_controller import save_exam
from app.database_controller import prep_exam
from app.database_controller import prep_video
from app.database_controller import prep_kinematics
from app.database_controller import prep_history
from app.database_controller import prep_phonehistory
from app.database_controller import prep_any_database
from app.database_controller import save_history_notes
#from app.database_controller import prep_open_report

from app.c3d_controller import make_graph
from app.c3d_controller import plot_kinematics
from app.c3d_controller import plot_kinetics
from app.c3d_controller import plot_bokeh


### data ###

### word ###
from app.word_controller import final_report

from app.classes import DateString, Convert_to_date, Report_var

import datetime
from datetime import datetime as my_datetime


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG 
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import random
import io

DATA_FOLDER="C:\\Users\\snbar\\projects\\"
day_list=['Monday','Tuesday','Wednesday','Thursday','Friday']
rep_data=Report_var()

##############################################################################
### diary ###
@app.route('/diary/<string:date>', methods=['GET', 'POST'])
def diary(date):
    form,current_date,col_values=diary_prep1(date)
       
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Select":
            current_date=diary_select(form)       
            return redirect(url_for('diary', date = current_date))
        if sub=="Go back a week":
            current_date=diary_go_back(form)
            return redirect(url_for('diary', date = current_date))
        if sub=="Go forward a week":
            current_date=diary_go_forward(form)      
            return redirect(url_for('diary', date = current_date))
        
    return render_template('diary.html',tabs1='management',title='Diary',
                           col_values=col_values,form=form,
                           current_date=current_date)
    
@app.route('/make/<string:date>/<string:time>', methods=['GET', 'POST'])   
def make(date,time):
    col_values,table,current_date=prep_make(date,time)
          
    if request.method=='POST':
        appID=request.form['submitButton']
        prep_set_app_date(appID,current_date,time)
        return redirect(url_for('diary', date = date))

    return render_template('make.html', 
                           col_values=col_values,
                           current_date=DateString(current_date),
                           day=day_list[current_date.weekday()],
                           time=time,
                           table=table,
                           date=date)
    
@app.route('/set_app_date/<int:appID>/<string:doa>/<string:time>', 
           methods=['GET', 'POST'])   
def set_app_date(appID,doa,time):
    prep_set_app_date(appID,Convert_to_date(doa),time)
    return redirect(url_for('diary', date = doa))


@app.route('/cancel<string:date>/<string:time>/<int:appID>/<string:details>', 
           methods=['GET', 'POST'])   
def cancel(date,time,appID,details):
    current_date=Convert_to_date(date)
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=='Cancel this appointment':
            cancel_appointment(appID)
        return redirect(url_for('diary', date = date))
    
    return render_template('cancel.html',
                           details=details,
                           current_date=DateString(current_date),
                           day=day_list[current_date.weekday()],time=time,
                           date=date) 
        
################################################################################
### admin ###   
@app.route('/referral', methods=['GET', 'POST'])
def referral():
    my_list=prep_referral()
    if request.method=='POST':
        sub=request.form['submitButton']
        open_letter(sub)        
    return render_template('referral.html', title='Referrals',tabs1='management',
                           tabs2='admin',my_list=my_list)
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    form=prep_register()
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="OK1":
            hosp_no,p,new,message=prep_register_OK1(form)
            return render_template('register.html',tabs1='none',
                        reg_level='two',title='Register referral',
                        form=form,p=p,new=new, message=message,hosp_no=hosp_no)
        if sub=="OK2":
            prep_register_OK2(form)            
            return render_template('register.html',tabs1='management',tabs2='admin',
                        reg_level='one',title='Register referral',form=form)
    return render_template('register.html',tabs1='management',tabs2='admin',
                        reg_level='one',title='Register referral',form=form)

@app.route('/needs_app', methods=['GET', 'POST'])
def needs_app():
    table,a=prep_in_progress([1])
    
    return render_template('needs_app.html', tabs1='management',tabs2='admin',
                        title='Patients who need an appointment',
                           table=table)
    
@app.route('/app_made')
def app_made():
    table=prep_in_progress([2])
    
    return render_template('app_made.html', tabs1='management',tabs2='admin',
                        title='Patients who have an appointment',
                        table=table)

@app.route('/change_status/<int:id>/<int:appID>')
def change_status(id,appID):
    url=prep_change_status(id,appID)
    return redirect(url_for(url))
    

@app.route('/')
@app.route('/in_progress')
def in_progress():
    attended,processed,written=prep_in_progress([3])

    return render_template('in_progress.html', tabs1='management',tabs2='admin',
                           attended=attended,
                           processed=processed,
                           written=written)

################################################################################
### database ###
@app.route('/any_database/<string:page>', methods=['GET', 'POST'])
def any_database(page):
    form = ExamForm()
    title,table=prep_any_database(page)
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Graph":
            print('graph')
            return redirect(url_for('show_graph'))
    
    return render_template('any_database.html',title=title,
                           tabs1='management', tabs2='database',
                           table=table, form=form)

@app.route('/show_graph/')
def show_graph():
    print('in graph')
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
    from bokeh.io import curdoc
    from bokeh.resources import INLINE
    from bokeh.embed import components
    # from bokeh.plotting import figure, output_file, show

    source = ColumnDataSource()
    
    fig = figure(plot_height=600, plot_width=720, tooltips=[("Title", "@title"), ("Released", "@released")])
    fig.line(x="x", y="y", source=source, color="#FF9900")
    fig.xaxis.axis_label = "IMDB Rating"
    fig.yaxis.axis_label = "Rotten Tomatoes Rating"
    
    currMovies = [
        {'imdbid': 'tt0099878', 'title': 'Jetsons: The Movie', 'genre': 'Animation, Comedy, Family', 'released': '07/06/1990', 'imdbrating': 5.4, 'imdbvotes': 2731, 'country': 'USA', 'numericrating': 4.3, 'usermeter': 46},
        {'imdbid': 'tt0099892', 'title': 'Joe Versus the Volcano', 'genre': 'Comedy, Romance', 'released': '03/09/1990', 'imdbrating': 5.6, 'imdbvotes': 23680, 'country': 'USA', 'numericrating': 5.2, 'usermeter': 54},
        {'imdbid': 'tt0099938', 'title': 'Kindergarten Cop', 'genre': 'Action, Comedy, Crime', 'released': '12/21/1990', 'imdbrating': 5.9, 'imdbvotes': 83461, 'country': 'USA', 'numericrating': 5.1, 'usermeter': 51},
        {'imdbid': 'tt0099939', 'title': 'King of New York', 'genre': 'Crime, Thriller', 'released': '09/28/1990', 'imdbrating': 7, 'imdbvotes': 19031, 'country': 'Italy, USA, UK', 'numericrating': 6.1, 'usermeter': 79},
        {'imdbid': 'tt0099951', 'title': 'The Krays', 'genre': 'Biography, Crime, Drama', 'released': '11/09/1990', 'imdbrating': 6.7, 'imdbvotes': 4247, 'country': 'UK', 'numericrating': 6.4, 'usermeter': 82}
    ]
    
    source.data = dict(
        x = [d['imdbrating'] for d in currMovies],
        y = [d['numericrating'] for d in currMovies],
        color = ["#FF9900" for d in currMovies],
        title = [d['title'] for d in currMovies],
        released = [d['released'] for d in currMovies],
        imdbvotes = [d['imdbvotes'] for d in currMovies],
        genre = [d['genre'] for d in currMovies]
    )
    
    print(source.data['x'])
    
    script, div = components(fig)
    
    return render_template('graph.html',
                plot_script=script,
                plot_div=div,
                js_resources=INLINE.render_js(),
                css_resources=INLINE.render_css(),
            ).encode(encoding='UTF-8')
    
@app.route('/patient/<int:patID>', methods=['GET', 'POST'])
def patient(patID):
    table,p,form=prep_patient(patID)
    other_form,diagnosis_table=prep_add_diagnosis(patID)

    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Save patient details":
            save_patient_details(form,patID)
        if sub=="Select diagnosis":
            return redirect(url_for('add_diagnosis', patID=patID))
        
    return render_template('patient.html', title='Patient Details',form=form,
                           table=table,p=p,
                           tabs1='management', tabs2='database',
                           diagnosis_table=diagnosis_table)

@app.route('/appointment/<int:appID>', methods=['GET', 'POST'])
def appointment(appID):
    tables,form,a=prep_appointment(appID)
       
    if request.method=='POST':
        return respond_appointment(form,appID,a)

    return render_template('appointment.html', title='Appointment Details',
                           tables=tables,form=form,a=a,
                           tabs1='management', tabs2='database')
    
@app.route('/condition/<int:id>', methods=['GET', 'POST'])
def condition(id):
    form,table,c=prep_condition(id)
    
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Save condition details":
            print('sAVING CONDIRION')
        if sub=="Add trials":
            return redirect(url_for('add_trial', condID = id,appID=c.appID))            
        if sub=="Go back to appointment":
            new_id=c.appID
            return redirect(url_for('appointment', appID = new_id))
        
    return render_template('condition.html', title='Condition Details',
                           table=table,form=form,c=c,
                           tabs1='management', tabs2='database')
    
@app.route('/trial/<int:id>', methods=['GET', 'POST'])
def trial(id):
    form,c=prep_trial(id)
    
    if request.method=='POST':
        sub=request.form['submitButton']         
        if sub=="Go back to condition":
            new_id=c.condID
            return redirect(url_for('condition', id = new_id))       
        if sub=="Return to trial database":
            return redirect(url_for('trial_database')) 
            
    return render_template('trial.html', title='Trial Details',
                           form=form,c=c,
                           tabs1='management', tabs2='database')
    
### notes ###
@app.route('/notes/<int:appID>')
def notes(appID):
    table=prep_notes(appID)
    return render_template('notes.html',tabs1='management',title='Notes',table=table)

@app.route('/add_diagnosis/<int:patID>', methods=['GET', 'POST'])
def add_diagnosis(patID):
    form,diagnosis_table=prep_add_diagnosis(patID)
    
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Add diagnosis":
            new_diagnosis(patID,form.diagnosis_select.data)
            return redirect(url_for('add_diagnosis', patID = patID))       
        if sub=="Exit":
            return redirect(url_for('patient', patID = patID))
    return render_template('add_diagnosis.html',tabs1='management',title='Diagnosis',
                           form=form,table=diagnosis_table)

@app.route('/add_staff/<int:appID>', methods=['GET', 'POST'])
def add_staff(appID):
    form,staff_table=prep_add_staff(appID)
    
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Add to staff list":
            new_staff(appID,form.role_select.data,form.staff_select.data)
            return redirect(url_for('add_staff', appID = appID))       
        if sub=="Exit":
            return redirect(url_for('appointment', appID = appID))
    return render_template('add_staff.html',tabs1='management',title='Staff',
                           form=form,table=staff_table)
    
@app.route('/add_folder/<int:appID>/<string:path>/<string:ftype>', methods=['GET', 'POST'])
def add_folder(appID,path,ftype):
    form,folder_table=prep_add_folder(appID,path)
    
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Open Folder":
            path=path+'\\'+form.path_select.data
            ftype=form.ftype_select.data
            return redirect(url_for('add_folder', appID = appID,path=path,ftype=ftype))
        if sub=="Select Path":
            new_folder(appID,form.ftype_select.data,path)
            return redirect(url_for('add_folder', appID = appID,path='Data',ftype=ftype))        
        if sub=="Exit":
            print('exiting with ',form.path_select.data,form.ftype_select.data)
            return redirect(url_for('appointment', appID = appID))
        
    return render_template('add_folder.html',tabs1='management',title='Folder',
                           path=path,form=form,table=folder_table)
    
@app.route('/add_referrer/<int:appID>', methods=['GET', 'POST'])
def add_referrer(appID):
    form,referrer_table=prep_add_referrer(appID)
    
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Select referrer":
            new_referrer(appID,form.ref_select.data)
            return redirect(url_for('add_referrer', appID = appID))        
        if sub=="Exit":
            return redirect(url_for('appointment', appID = appID))
        
    return render_template('add_referrer.html',tabs1='management',title='Folder',
                           form=form,table=referrer_table)

@app.route('/add_trial/<int:condID>/<int:appID>', methods=['GET', 'POST'])
def add_trial(condID,appID):
    form,trial_table,data_folder,my_list=prep_add_trial(condID,appID)

    if request.method=='POST':
        sub=request.form['submitButton']
        if sub == 'Select trials':
            my_list=request.form.getlist('trial')
            ttype=form.ttype_select.data        
            save_trials(my_list,ttype,condID)
            return redirect(url_for('add_trial', condID = condID,appID=appID))
        else:
            return redirect(url_for('condition', condID = condID))
        
    return render_template('add_trial.html',tabs1='management',title='Trials',
                           appID=appID,condID=condID,form=form,
                           table=trial_table,data_folder=data_folder,my_list=my_list)
    
    
### general ###
@app.route('/add_condition/<int:appID>', methods=['GET', 'POST'])
def add_condition(appID):
    form,condition_table=prep_add_condition(appID)
    if request.method=='POST':
        sub=request.form['submitButton']
        if sub=="Select condition":
            new_condition(appID,form.footware_select.data,form.walking_aid_select.data)
            return redirect(url_for('add_condition', appID=appID))
        if sub=="Exit":
            return redirect(url_for('appointment', appID = appID))
    return render_template('add_condition.html',title='Please select condition',
                           form=form,table=condition_table)
    
### report ###################################################################
##############################################################################

#@app.route('/report/<int:appID>', methods=['GET', 'POST'])
#def report(appID):
#    rep_data,this_a=prep_export(appID)
#       
##    name_values=tree_list.name
##    type_values=tree_list.type   
##    col_values=zip(name_values,type_values)
#    
#    return render_template('report.html',tabs1='report',
##                           col_values=col_values,
#                           rep_data=rep_data,appID=appID)
    
### text pages ####
@app.route('/report/<int:appID>')
def report(appID):
    global rep_data
    rep_data=Report_var()
    global ff
    ff=117
    
    rep_data,layout =prep_report(appID,rep_data)
    print(rep_data.name)
    print('in report')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
                # required_data=t.c3d.kin
    # global rep_data  ### set up class variable to hold all data for patient
    # rep_data= rep_data()
    # rep_data,this_a=prep_export(appID,rep_data)
#    rep_data,this_a=prep_export(appID)
    form=ExportForm()
    # print('Opening report for appointment', dir(this_a))
    # print('Opening report for appointment', dir(this_a.patient))
    # print('Opening report for appointment', dir(this_a.condition))
    # print(dir(rep_data))
    
    # print('in graph')
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
    from bokeh.io import curdoc
    from bokeh.resources import INLINE
    from bokeh.embed import components
    from bokeh.layouts import column, row
    from bokeh.models import Select
    from bokeh.palettes import Spectral5
    # from bokeh.plotting import curdoc, 
    # from bokeh.plotting import figure, output_file, show
    
    # def update(attr, old, new):
    #     print('UPDATING')

    # source = ColumnDataSource()
    
    # fig = figure(plot_height=600, plot_width=720, tooltips=[("Title", "@title"), ("Released", "@released")])
    # fig.line(x="x", y="y", source=source, color="#FF9900")
    # fig.xaxis.axis_label = "IMDB Rating"
    # fig.yaxis.axis_label = "Rotten Tomatoes Rating"
    
    # currMovies = [
    #     {'imdbid': 'tt0099878', 'title': 'Jetsons: The Movie', 'genre': 'Animation, Comedy, Family', 'released': '07/06/1990', 'imdbrating': 5.4, 'imdbvotes': 2731, 'country': 'USA', 'numericrating': 4.3, 'usermeter': 46},
    #     {'imdbid': 'tt0099892', 'title': 'Joe Versus the Volcano', 'genre': 'Comedy, Romance', 'released': '03/09/1990', 'imdbrating': 5.6, 'imdbvotes': 23680, 'country': 'USA', 'numericrating': 5.2, 'usermeter': 54},
    #     {'imdbid': 'tt0099938', 'title': 'Kindergarten Cop', 'genre': 'Action, Comedy, Crime', 'released': '12/21/1990', 'imdbrating': 5.9, 'imdbvotes': 83461, 'country': 'USA', 'numericrating': 5.1, 'usermeter': 51},
    #     {'imdbid': 'tt0099939', 'title': 'King of New York', 'genre': 'Crime, Thriller', 'released': '09/28/1990', 'imdbrating': 7, 'imdbvotes': 19031, 'country': 'Italy, USA, UK', 'numericrating': 6.1, 'usermeter': 79},
    #     {'imdbid': 'tt0099951', 'title': 'The Krays', 'genre': 'Biography, Crime, Drama', 'released': '11/09/1990', 'imdbrating': 6.7, 'imdbvotes': 4247, 'country': 'UK', 'numericrating': 6.4, 'usermeter': 82}
    # ]
    
    # source.data = dict(
    #     x = [d['imdbrating'] for d in currMovies],
    #     y = [d['numericrating'] for d in currMovies],
    #     color = ["#FF9900" for d in currMovies],
    #     title = [d['title'] for d in currMovies],
    #     released = [d['released'] for d in currMovies],
    #     imdbvotes = [d['imdbvotes'] for d in currMovies],
    #     genre = [d['genre'] for d in currMovies]
    # )
    
    # columns=['one','two','three']
    
    # x = Select(title='X-Axis', value='mpg', options=columns)
    # x.on_change('value', update)
    
    # y = Select(title='Y-Axis', value='hp', options=columns)
    # y.on_change('value', update)
        
    # controls = column(x, y, width=200)
    # layout = row(controls, fig)
    
    # curdoc().add_root(layout)
    # curdoc().title = "Crossfilter"
    
    # layout=plot_bokeh(rep_data)
    
    script, div = components(layout)
    
    # return render_template('graph.html',
    #             plot_script=script,
    #             plot_div=div,
    #             js_resources=INLINE.render_js(),
    #             css_resources=INLINE.render_css(),
    #         ).encode(encoding='UTF-8')
    
    
    
    return render_template('report.html',tabs1='report',tabs2='text',
                           # appID=appID,
                           rep_data=rep_data,
                           url_kinematics='/static/images/kinematic_plot.png',
                           url_kinetics='/static/images/kinetic_plot.png',
                           form=form,
                           plot_script=script,
                            plot_div=div,
                            js_resources=INLINE.render_js(),
                            css_resources=INLINE.render_css(),
                        ).encode(encoding='UTF-8')


@app.route('/header/')
def header():
#     global rep_data
#     global rep_data  ### set up class variable to hold all data for patient
#     rep_data= rep_data()
#     rep_data,this_a=prep_export(appID,rep_data)
# #    rep_data,this_a=prep_export(appID)
#     form=ExportForm()
    # print('Opening report for appointment', dir(this_a))
    # print('Opening report for appointment', dir(this_a.patient))
    # print('Opening report for appointment', dir(this_a.condition))
    # print(dir(rep_data))
    return render_template('header.html',tabs1='report',tabs2='text',
#                           a=this_a,
                           appID=appID,
                           rep_data=rep_data,
                           my_ref=rep_data.referrer,form=form)

@app.route('/history/', methods=['GET', 'POST'])
def history():
#    rep_data,this_a=prep_history(appID)
    print('ff: ',ff)
    print(rep_data.name)
    print('in history')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
    form=HistoryForm()
    
#     if request.method=='POST':
#         sub=request.form['submitButton']
#         print('SUB',sub)
#         if sub=="Import text":
#             print('saving')
#             return redirect(url_for('history',appID=appID))
#         if sub=="Save history":
#             print('saving')
#             for n in rep_data.history:
#                 print(n.id)
#             print(request.GET['test'])
# #            sub=request.form['text_box']
# ##            print(sub)
# #            save_to_text_file(sub)
#             return redirect(url_for('history',appID=appID))

    
    return render_template('history.html',tabs1='report',tabs2='text',
                           form=form,
                           # appID=appID,
                           rep_data=rep_data)
    
@app.route('/phonehistory/', methods=['GET', 'POST'])
def phonehistory():
#    rep_data,this_a=prep_phonehistory(appID)
    print('current_box',rep_data.historynotes.current_box)
    form=PhoneHistoryForm(ascends=rep_data.historynotes.ascends, 
                          stairfeet=rep_data.historynotes.stairfeet,
                          current_box=rep_data.historynotes.current_box,
                          diff_box=rep_data.historynotes.diff_box,
                          changes=rep_data.historynotes.changes)
    
#    form.current_box.data=rep_data.historynotes.current_box
    
#    form.ascends.default=rep_data.historynotes.ascends

#    form1=PhoneCheckboxForm()
    
    if request.method=='POST':
        sub=request.form['submitButton']
        print('SUB',sub)
        if sub=="Import text":
            print('saving')
            return redirect(url_for('phonehistory',appID=appID))
        if sub=="Save history":
            print('saving')
            save_history_notes(form,rep_data,this_a)
            rep_data,this_a=prep_phonehistory(appID)
            return redirect(url_for('phonehistory',appID=appID))

    
    return render_template('phonehistory.html',tabs1='report',tabs2='text',
                           form=form,appID=appID,this_a=this_a,
                           rep_data=rep_data)
    
@app.route('/findings/')
def findings():
#    rep_data=prep_video(appID)
    f=all_table('Findinglist')
    for finding in f:
        print(finding.text)
    return render_template('findings.html',tabs1='report',tabs2='text',
                           rep_data=rep_data,appID=appID,f=f) 
@app.route('/create_finding/<int:appID>/<string:t>')
def create_finding(appID,t):
#    rep_data=prep_video(appID)
    for finding in f:
        print(finding.text)
    return render_template('findings.html',tabs1='report',tabs2='text',
                           rep_data=rep_data,appID=appID,f=f) 

@app.route('/recommendations/')
def recommendations():
#    rep_data=prep_video(appID)
    return render_template('recommendations.html',tabs1='report',tabs2='text',
                           rep_data=rep_data,appID=appID) 
### data pages ###
@app.route('/video/')
def video():
#    rep_data=prep_video(appID,rep_data)
    return render_template('video.html',tabs1='report',tabs2='data',
                           appID=appID,
                           rep_data=rep_data)

#class Item(object):
#    def __init__(self, name, left, right):
#        self.name = name
#        self.nameL = name+'L'
#        self.nameR = name+'R'
#        self.left = left
#        self.right = right
        

@app.route('/exam/', methods=['GET', 'POST'])
def exam():
    print(rep_data.name)
    # rep_data,a=prep_exam(appID,rep_data)
    form=ExamForm()

    if request.method=='POST':
        sub=request.form['submitButton']
        save_exam(form,appID,rep_data.LexamID,rep_data.RexamID)
        
        return redirect(url_for('exam', appID = appID))
       
    return render_template('exam.html',tabs1='report',tabs2='data',
                           rep_data=rep_data,
#                           a=a,
                           form=form,
                           items=rep_data.items,
                           combined=rep_data.combined,
                           years=rep_data.years)
    
@app.route('/photos/')
def photos():
#    rep_data=prep_video(appID)
    
#    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'jpeg.jpg')
#    print(full_filename)
#    return render_template("index.html", user_image = full_filename)
    return render_template('photos.html',tabs1='report',tabs2='data',
                           appID=appID,
                           rep_data=rep_data)
#                           ,
#                           user_image=full_filename)

@app.route('/ST/')
def ST():
    print('ff: ',ff)
    print(rep_data.name)
    print('in ST')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
#    rep_data=prep_video(appID)
    return render_template('ST.html',tabs1='report',tabs2='data',
                           rep_data=rep_data)

@app.route('/kinematics/')
def kinematics():
    global ff
    ff=117
    print('ff: ',ff)
    print(rep_data.name)
    print('in kinematics')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)

    return render_template('kinematics.html',tabs1='report',tabs2='data',
                           rep_data=rep_data)


# @app.route('/jpg/', methods=['GET', 'POST'])
# def jpg():
#     from PIL import Image
#     im=Image.open('C:\\Users\\snbar\\projects\\myName.png')
# #    im.show()
# #    image_file='C:\\Users\\snbar\\projects\\myName.png'
# #    file = request.files['file']
# #    file.save(image_file)
# #    output = io.BytesIO()
# #    file.print_png(output)
#     return Response(Image, mimetype='image/png')

@app.route("/matplot_kinematics/", methods=['GET', 'POST'])
def matplot_kinematics():
    print('in matplot kinematics')    
    print('ff: ',ff)
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
                print(t.c3d.kin.LPelvisAngles.x)
    output = plot_kinematics(rep_data)
    
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/matplot_kinetics/', methods=['GET', 'POST'])
def matplot_kinetics():
#    rep_data=prep_kinematics(appID)
    output = plot_kinetics(rep_data.c3d.kin)
    
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/kinetics/')
def kinetics():
#    rep_data=prep_kinematics(appID)
    plot_bokeh()
    
    return render_template('kinetics.html',tabs1='report',tabs2='data',
                           rep_data=rep_data)
   
### export report ###
@app.route('/export/', methods=['GET', 'POST'])
def export():
    # global rep_data  ### set up class variable to hold all data for patient
    # rep_data= rep_data()
    # rep_data,this_a=prep_export(appID,rep_data)
    print('back in export')
    print(rep_data.c3d.kin.LPelvisAngles.x)
    print(rep_data.apps)
    form=ExportForm()
    
    if request.method=='POST':
        sub=request.form['submitButton']
        final_report(rep_data)
        return redirect(url_for('export'))

    return render_template('export.html',tabs1='report',a=this_a,
                           rep_data=rep_data,
                           my_ref=rep_data.referrer,form=form)
