from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin

    
class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))
    surname=db.Column(db.String(64))
    dob=db.Column(db.DateTime)
    dob_str=db.Column(db.String(64))
    hosp_no= db.Column(db.String(64))
    NHS_no= db.Column(db.Integer, index=True, unique=True)
    diagnosis=db.Column(db.Integer)
    appointment = db.relationship('Appointment', back_populates='patient')
    diagnosis = db.relationship('Diagnosis', back_populates='patient')
    def __repr__(self):
        return '%s %s' % (self.name, self.surname)
    
class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patID=db.Column(db.Integer, db.ForeignKey('patient.id'))
    doa=db.Column(db.DateTime)
    doa_str=db.Column(db.String)
    time=db.Column(db.String)
    status=db.Column(db.Integer, db.ForeignKey('status.id'))
    follow_up=db.Column(db.DateTime)
    when=db.Column(db.String)
    condition=db.relationship('Condition',back_populates='appointment' )
    folder=db.relationship('Folder',back_populates='appointment' )
    staff=db.relationship('Staff',back_populates='appointment' )
    exam=db.relationship('Exam',back_populates='appointment' )
    referrer=db.relationship('Referrer',back_populates='appointment' )
    
    patient=db.relationship('Patient',back_populates='appointment')
    stat=db.relationship('Status',back_populates='appointment')
    def __repr__(self):
        return '%s %s' % (self.patient, self.doa_str)
    
class Status(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    statusname=db.Column(db.String)
    appointment = db.relationship('Appointment', back_populates='stat' )
    
    def __repr__(self):
        return '%s' % (self.statusname)
    
class Condition(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    footware=db.Column(db.String)
    walking_aid=db.Column(db.String)
    trial=db.relationship('Trial',back_populates='condition' )
    appointment=db.relationship('Appointment',back_populates='condition' )
    def __repr__(self):
        return '%s %s %s' % (self.appointment, self.footware, self.walking_aid)
    
class Trial(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    condID=db.Column(db.Integer, db.ForeignKey('condition.id'))
    ttype=db.Column(db.String)
    c3dfile=db.Column(db.String)
    # c3d_kin=db.Column(db.String)
    condition=db.relationship('Condition',back_populates='trial' )
    def __repr__(self):
        return '%s %s' % (self.condition,self.c3dfile)
    
class Exam(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    side=db.Column(db.String)
    hipflex=db.Column(db.Integer)
    hipflexdef=db.Column(db.Integer)
    hipabdflex=db.Column(db.Integer)
    hipabdext=db.Column(db.Integer)
    hiprotint=db.Column(db.Integer)
    hiprotext=db.Column(db.Integer)
    femant=db.Column(db.Integer)
    kneeffd=db.Column(db.Integer)
    kneehyp=db.Column(db.Integer)
    kneeflexflex=db.Column(db.Integer)
    kneeflexext=db.Column(db.Integer)
    popliteal=db.Column(db.Integer)
    mdfflex=db.Column(db.Integer)
    mfdext=db.Column(db.Integer)
    bimal=db.Column(db.Integer)
    appointment=db.relationship('Appointment',back_populates='exam' )
    
    
class Stafflist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String)
    name=db.Column(db.String)
    surname=db.Column(db.String)
    profession=db.Column(db.String)
    initials=db.Column(db.String)
    notes=db.relationship('Notes',back_populates='stafflist' )
    staff=db.relationship('Staff',back_populates='stafflist' )
    def __repr__(self):
        return '%s %s' % (self.name,self.surname)
    
class Folder(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    ftype=db.Column(db.String)
    folder=db.Column(db.String)
    appointment=db.relationship('Appointment',back_populates='folder' )
    
class Staff(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    role=db.Column(db.String)
    stafflistID=db.Column(db.Integer, db.ForeignKey('stafflist.id'))
    appointment=db.relationship('Appointment',back_populates='staff' )
    stafflist=db.relationship('Stafflist',back_populates='staff' )
    
    
class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    doa=db.Column(db.DateTime)
    stafflistID=db.Column(db.Integer, db.ForeignKey('stafflist.id'))
    note=db.Column(db.String)
    stafflist=db.relationship('Stafflist',back_populates='notes' )
    
class HistoryNotes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    ck1=db.Column(db.Boolean)
    ck2=db.Column(db.Boolean)
    ck3=db.Column(db.Boolean)
    ck4=db.Column(db.Boolean)
    ck5=db.Column(db.Boolean)
    ck6=db.Column(db.Boolean)
    ck7=db.Column(db.Boolean)  
      
    diff=db.Column(db.String)
    diff_box=db.Column(db.String)
    comm_box=db.Column(db.String) 
    
    current_box= db.Column(db.String)
    max_distance=db.Column(db.String)
    units=db.Column(db.String)
    condition=db.Column(db.String)
    stopped_by=db.Column(db.String)
    speaker=db.Column(db.String)
    relationship=db.Column(db.String)
    ascends=db.Column(db.String)
    descends=db.Column(db.String)
    stairfeet=db.Column(db.String)
    kerbs=db.Column(db.String)
    wheelchair=db.Column(db.String)
    year=db.Column(db.String)
    changes=db.Column(db.String)
    limiting=db.Column(db.String)
    activities=db.Column(db.String)
    interventions=db.Column(db.String)
    physio_name=db.Column(db.String)
    physio_centre=db.Column(db.String)
    physio_programme=db.Column(db.String)
    AFOS=db.Column(db.String)
    afo_description=db.Column(db.String)
    afo_worn=db.Column(db.String)
    afo_comment=db.Column(db.String)
    gestation=db.Column(db.String)
    delivery=db.Column(db.String)
    neonatal=db.Column(db.String)
    age_sat=db.Column(db.String)
    age_walked=db.Column(db.String)
    age_diagnosis=db.Column(db.String)

    
class History(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    title=db.Column(db.String)
    text=db.Column(db.String)
    
class Historytemplate(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String)
    text=db.Column(db.String)
    
class Finding(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    findinglistID=db.Column(db.Integer)
    sidelistID=db.Column(db.Integer)
    qualifier=db.Column(db.String)

class Evidence(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    findingID=db.Column(db.Integer, db.ForeignKey('finding.id'))
    evidencelistID=db.Column(db.Integer)
    sidelistID=db.Column(db.Integer)
    qualifier=db.Column(db.String)
    
class Findinglist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String)
    
class Evidencelist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String)
    source=db.Column(db.String)
    
class Sidelist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String)
  
class Diagnosis(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    diagnosisID=db.Column(db.Integer,db.ForeignKey('diagnosislist.id'))
    patID=db.Column(db.Integer,db.ForeignKey('patient.id'))
    patient=db.relationship('Patient',back_populates='diagnosis' )
    diag=db.relationship('Diagnosislist',back_populates='diagnosislists' )
    
class Diagnosislist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    diagnosis=db.Column(db.String)
    category=db.Column(db.String)
    description=db.Column(db.String)
    diagnosislists=db.relationship('Diagnosis',back_populates='diag' )
    def __repr__(self):
        return '%s' % (self.description)
    
#class CategoryList(db.Model):
#    id=db.Column(db.Integer,primary_key=True)
#    category=db.Column(db.String)

class Referrerlist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    RefTitle=db.Column(db.String)
    RefName=db.Column(db.String)
    RefSurname=db.Column(db.String)
    RefJobTitle=db.Column(db.String)
    RefAddress=db.Column(db.String)
    referrerlists=db.relationship('Referrer',back_populates='referrer' )
    def __repr__(self):
        return '%s %s %s, %s, %s' % (self.RefTitle,self.RefName,self.RefSurname,self.RefJobTitle,self.RefAddress)
    
class Referrer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appID=db.Column(db.Integer, db.ForeignKey('appointment.id'))
    refID=db.Column(db.Integer,db.ForeignKey('referrerlist.id'))
    isRef=db.Column(db.Binary)
    appointment=db.relationship('Appointment',back_populates='referrer' )
    referrer=db.relationship('Referrerlist',back_populates='referrerlists' )
    
class FileLocation(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    filename=db.Column(db.String)
    path=db.Column(db.String)
    
