from flask_wtf import FlaskForm
from flask_wtf import Form
from flask_table import Table, Col,LinkCol
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, DateField, IntegerField, HiddenField, FieldList,FormField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField as Picker
from wtforms.widgets import TextArea

s={1:'Registered',2:'App made',3:'Attended',4:'Processed',5:'Written',6:'Reported'}

def DateString(d):
    datestring=str(d.day)+'/'+str(d.month)+'/'+str(d.year)
    return datestring

### diary ###
class DiaryTable(Table):   
    doa=Col('Day')
    ### left hand operator is the name from the db table
    doa_str = Col('DOA')
    op=LinkCol('Day','appointment',url_kwargs=dict(appID='id'),text_fallback=doa_str)   
    id=Col('ID')
    patID = Col('PatID')
    time=Col('Time')
    status=Col('Status')
    
###


class ConditionSelect(FlaskForm):
   footware=[('barefoot', 'barefoot'), ('L AFO', 'L AFO'), ('R AFO', 'R AFO')]
   walking_aid=[('independent','independent'),('posterior walker','posterior walker')]
   footware_select = SelectField(u'Footware', choices=footware)
   walking_aid_select = SelectField(u'Walking aid', choices=walking_aid)
   submit=SubmitField('select')
   
class StaffSelect(FlaskForm):
    role=[('holder', 'holder'), ('measurer', 'measurer'), ('observer', 'observer'),
          ('processor','processor'),('writer','writer'),('reviewer','reviewer')]
#    staff=[(1,'NF'),(2,'JN')]
    role_select = SelectField(u'Role', choices=role)
    staff_select = SelectField(u'Staff')
    submit=SubmitField('select')
    
class DiagnosisSelect(FlaskForm):
    diagnosis_select = SelectField(u'Diagnosis')
    submit=SubmitField('select')
    
class FolderSelect(FlaskForm):
    ftypelist=[('report', 'report'), ('data', 'data'), ('photo', 'photo')]
#    folder=[]
    ftype_select = SelectField(u'Role', choices=ftypelist)
    folder_select = SubmitField(u'Folder')
    path_select = SelectField(u'Path')
#    folder3_select = SelectField(u'Folder3')
#    folder4_select = SelectField(u'Folder4')
    submit=SubmitField('select')

class TrialSelect(FlaskForm):
    ttypelist=[('gait', 'gait'), ('static', 'static'), ('long movie', 'long movie')]
    ttype_select = SelectField(u'Ttype', choices=ttypelist)
    submit=SubmitField('select') 
    
class ReferrerSelect(FlaskForm):
#    ttypelist=[('gait', 'gait'), ('static', 'static'), ('long movie', 'long movie')]
    ref_select = SelectField(u'Ttype')
    submit=SubmitField('select')
   
class SingleButton(Form):
    new=SubmitField('new')

class DiaryForm(FlaskForm):
#    date_of_interest=StringField('Date of interest')
    select=SubmitField('select date')
    cd=StringField('current date')
    dt = Picker('DatePicker', format='%Y-%m-%d')
#    start_time = DateField('Start at', widget=DatePickerWidget())
#    go_back=SubmitField('<')
    
class DayForm(Form):
    open_pat_am=SubmitField('open pat')
    make_am=SubmitField('make app')
    cancel_am=SubmitField('cancel app')
    open_pat_pm=SubmitField('open pat')
    make_pm=SubmitField('make app')
    cancel_pm=SubmitField('cancel app')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PatientForm(FlaskForm):
    id=StringField('ID')
    name=StringField('Name')
    surname=StringField('Surname')
    dob_str=StringField('DOB')
    hosp_no=StringField('Hosp No')
    NHS_no=StringField('NHS No')
    submit=SubmitField('Save patient')

class AppointmentForm(FlaskForm):
    id=StringField('ID')
    status=StringField('Status')
    doa_str=StringField('DOA')
    patID=IntegerField('PatID')
    follow_up=StringField('Follow up')
    submit=SubmitField('Save appointment')    
    footware=[('barefoot', 'barefoot'), ('L AFO', 'L AFO'), ('R AFO', 'R AFO')]
    walking_aid=[('independent','independent'),('posterior walker','posterior walker')]
    footware_select = SelectField(u'Footware', choices=footware)
    walking_aid_select = SelectField(u'Walking aid', choices=walking_aid)
    
class ConditionForm(FlaskForm):
    id=StringField('ID')
    footware=StringField('Footware')
    walking_aid=StringField('Walking aid')
    
class TrialForm(FlaskForm):
    id=StringField('ID')
    c3dfile=StringField('c3dfile')


    
class NewPatientForm(FlaskForm):
    name=StringField('Name')
    surname=StringField('Surname')
    submit=SubmitField('Save patient')
    
class ReferralForm(FlaskForm):
    name=StringField('Name')
    surname=StringField('Surname')
    submit=SubmitField('Save patient')
    
class RegisterForm(FlaskForm):
    number=StringField('HospNo')
    submit=SubmitField('OK')
    name=StringField('Name')
    surname=StringField('Surname')
    when_comment=StringField('Comment')
    when=SelectField('When', choices=[('ASAP', 'ASAP'), ('Delayed', 'Delayed')])
    
class PatientTable(Table):
    id=LinkCol('open','patient',url_kwargs=dict(patID='id'))
    name = Col('Name')
    surname = Col('Surname')
    dob_str= Col('DOB')
    hosp_no= Col('hosp_no')
    NHS_no=Col('NHS_no')

class NotesTable(Table):
    doa=Col('Date')
    note=Col('Note')    
    
#class PatientItem(object):
#    def __init__(self, id, name, surname,dob_str,hosp_no):
#        
#        self.id=id
#        self.name = name
#        self.surname = surname
#        self.dob_str = dob_str
#        self.hosp_no = hosp_no

class AppointmentTable(Table):
    op=LinkCol('open','appointment',url_kwargs=dict(appID='id'))
    id=Col('ID')
    patient=Col('Patient') 
    doa_str = Col('DOA')
    time=Col('Time')
#    status=Col('Status')
    stat=Col('Status')
    when=Col('When')
    
class InProgressTable(Table):
    op=LinkCol('open','appointment',url_kwargs=dict(appID='id'))
    id=Col('ID')
    patient=Col('Patient') 
    doa_str = Col('DOA')
    time=Col('Time')
    stat=Col('Status')
    op2=LinkCol('change_status','change_status',url_kwargs=dict(id='status',appID='id'))
    
class NeedsAppTable(Table):
    op=LinkCol('open','appointment',url_kwargs=dict(appID='id'))
    id=Col('ID')
    patient=Col('Patient') 
    when=Col('When')

class MakeTable(Table):
    op=LinkCol('select','set_app_date',url_kwargs=dict(appID='id',doa='doa',time='time'))
    id=Col('ID')
    patient=Col('Patient') 
    when=Col('When')

    
#class ProgressTable(Table):
#    op=LinkCol('open','appointment',url_kwargs=dict(id='id'))
#    id=Col('ID')
#    patient=Col('Patient') 
#    doa_str = Col('DOA')
#    time=Col('Time')
#    status=Col('Status')
#    stat=Col('Status')
#    
          
    
#class AppointmentItem(object):
#    def __init__(self, op,id,patID, doa_str,time,status):
#        self.op=op
#        self.patID = patID.patient
#        self.doa_str = doa_str
#        self.time=time
#        self.status = s[status]
#        self.id=id
        
class ConditionTable(Table):
    op=LinkCol('open','condition',url_kwargs=dict(id='id'))
    id=Col('ID')
    appID = Col('AppID')
    footware = Col('Footware')
    walking_aid=Col('WalkingAid')

       
    
#class ConditionItem(object):
#    def __init__(self, op,appID,footware,walking_aid):
#        self.op=op
#        self.appID = appID.appointment
#        self.footware = footware
#        self.walking_aid=walking_aid

class TrialTable(Table):
#    op=LinkCol('open','trial',url_kwargs=dict(id='id'))
#    id=Col('ID')
#    condID = Col('CondID')
#    c3dfile = Col('c3dfile')
    op=LinkCol('open','trial',url_kwargs=dict(id='id'))
    id=Col('ID')
    condID = Col('CondID')
    ttype=Col('Type')
#    footware = Col('Footware')
#    walking_aid=Col('WalkingAid')
    c3dfile = Col('c3dfile')
    
    
class ExamDbTable(Table):
#    op=LinkCol('open','trial',url_kwargs=dict(id='id'))
    id=Col('ID')
    appID = Col('AppID')
    side=Col('Side')
#    footware = Col('Footware')
#    walking_aid=Col('WalkingAid')
    hipflex=Col('hipflex')
    hipflexdef = Col('hipflexdef')
    
    
class StaffTable(Table):
    role=Col('Role')
    stafflist=Col('staff')
    
class DiagnosisTable(Table):
    diag=Col('Diagnosis')

    
class FolderTable(Table):
    ftype=Col('type')
    folder=Col('folder')
    
class ReferrerTable(Table):
    referrer=Col('referrer')
#    RefName=Col('name')
#    RefSurname=Col('surname')
    
#class TrialItem(object):
#    def __init__(self, op,condID,c3dfile):
#        self.op=op
#        self.condID = condID.appointment
#        self.c3dfile = c3dfile

#class PatientListTable(Table):


class MakeAppTable(Table):
#    op=LinkCol('make appointment','diary',id='None')
    id=Col('ID')
    patient = Col('patient')
    status=Col('Status')       
    
class ExamTable(Table):
    
    name = Col('')
    left = Col('Left')
    right=Col('Right')
#    name=Col('Name')
#    currentleft=Col('Left')
#    currentright=Col('Right')
#    hipflex=Col('Hip flexion')
#    hipflexdef=Col('Hip flexion deformity')
#    hipabdflex=Col('Hip abduction (flexion)')
#    hipabdext=Col('Hip abduction (extension)')
#    hiprotint=Col('Internal hip rotation')
#    hiprotext=Col('External hip rotation')
#    femant=Col('Femoral anteversion')
#    kneeffd=db.Column(db.Integer)
#    kneehyp=db.Column(db.Integer)
#    kneeflexflex=db.Column(db.Integer)
#    kneeflexext=db.Column(db.Integer)
#    popliteal=db.Column(db.Integer)
#    mdfflex=db.Column(db.Integer)
#    mfdext=db.Column(db.Integer)
#    bimal=db.Column(db.Integer)
    
class ExamForm(Form):
    hipflex=IntegerField('Hip flexion')
    hipflexdef=IntegerField('Hip flexion deformity')
    hipabdflex=IntegerField('Hip abduction (flexion)')
    hipabdext=IntegerField('Hip abduction (extension)')
    hiprotint=IntegerField('Internal hip rotation')
    hiprotext=IntegerField('External hip rotation')
    femant=IntegerField('Femoral anteversion')   
    
class ExamList(Form):
    exams=FieldList(FormField(ExamForm))
    
class HistoryForm(FlaskForm):
    text=StringField('text')
    
class PhoneHistoryForm(FlaskForm):
    text=StringField('text')
    ck1=BooleanField("Confirmed date of birth of patient")
    ck2=BooleanField("Introduced yourself")
    ck3=BooleanField("Have completed GFAQ")
    ck4=BooleanField("Confirmed appointment date")
    ck5=BooleanField("Discussed who will attend appointment")
    ck6=BooleanField("Discussed travel arrangements")
    ck7=BooleanField("Discussed COVID symptoms")
    
    
    
    diff=BooleanField("None or fill in below")
    diff_box=StringField(u'diff_box', widget=TextArea())
    comm_box= StringField(u'Text', widget=TextArea())
    

    current_box= StringField(u'current_box', widget=TextArea())
    max_distance=StringField()
    units=StringField()
    condition=StringField()
    stopped_by=StringField()
    speaker=StringField('speaker')
    relationship=StringField()
    ascends=SelectField('ascends', choices=[('',''),('independently', 'independently'),
                            ('holding one handrail', 'holding one handrail'),
                            ('holding two handrails', 'holding two handrails'),
                            ('unable','unable')])
    descends=SelectField('ascends', choices=[('',''),('independently', 'independently'),
                            ('holding one handrail', 'holding one handrail'),
                            ('holding two handrails', 'holding two handrails'),
                            ('unable','unable')])
    stairfeet=SelectField('stairfeet', choices=[('',''),('both feet on each step', 'both feet on each step'),
                            ('alternating feet', 'alternating feet')])
    kerbs=SelectField('kerbs', choices=[('',''),
                            ('independently', 'independently'),
                            ('using posterior walker', 'using posterior walker'),
                            ('holding on to something', 'holding on to something'),
                            ('unable','unable')])
    wheelchair=SelectField('wheelchair', choices=[('',''),
                            ('none', 'none'),
                            ('none but would like', 'none but would like'),
                            ('has one can self propel', 'has one can self propel'),
                            ('has one pushed','has one pushed')])
    year=SelectField('year', choices=[('',''),
                            ('year', 'year'),
                            ('6 months','6 months')])
    changes=StringField(u'Text', widget=TextArea())
    limiting=StringField(u'Text', widget=TextArea())
    activities=StringField(u'Text', widget=TextArea())
    interventions=StringField(u'Text', widget=TextArea())
    physio_name=StringField()
    physio_centre=StringField()
    physio_frequency=StringField()
    physio_programme=SelectField('programme', choices=[('',''),
                            ('yes', 'yes'),
                            ('no','no')])
    AFOS=SelectField('programme', choices=[('',''),
                            ('none', 'none'),
                            ('L AFO','L AFO'),
                            ('R AFO','R AFO'),
                            ('B AFO','B AFO')])
    afo_description=StringField('afo_description')
    afo_worn=StringField()
    afo_comment=StringField()
    gestation=StringField()
    delivery=StringField()
    neonatal=StringField()
    age_sat=StringField()
    age_walked=StringField()
    age_diagnosis=StringField()
    
class ExportForm(FlaskForm):
    text=StringField('text')
    export=SubmitField('export')