# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 17:00:02 2021

@author: snbar
"""

class Report_var(object):
    def __init__(self):
        self.name=[]
        self.dob_str=[]
        self.hosp_no=[]
        self.app1=[]
        self.app2=[]
#        for a in doa:
#            setattr(self, 'app' + a,[])
        
class Apps(object):
    def __init__(self):
        self.referrer=[]  
        self.staff=[] 
        self.doa=[]
        

report_var=Report_var()
        
a=Apps()
a.referrer.append("Gough")
a.staff.append("NF")
a.doa.append("06sep2021")

report_var.app1=a
a=Apps()
a.referrer.append("Brown")
a.staff.append("JJ")
a.doa.append("06jan2022")  
report_var.app2=a

for v in dir(report_var):
    if v[0:3] == 'app':
        print(v)

b='app1'
c='doa'

print(getattr(getattr(report_var,b),c))
#report_var=Report_var(a.doa)
#
#report_var.dob_str="02/03/1999"
#report_var.name='Fred Blogga'
#report_var.hosp_no='2344x'
#
#apps=a.doa
#conds=['barefoot','shoes']
#
#report_var.apps=apps
##setattr(report_var.apps[0],'conds',conds)
#
#t1=['T1','T2','T3','T4']
#t2=['T5','T6']
#t3=['T7','T8']
#
#c1=[]
#c1.t=t1
#c2=[]
#c2.t=t2
#c3=[]
#c3.t=t3
#
#a1=[]
#a1.c=[c1,c2]
#a2=[]
#a2.c=c3
#
