# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:53:10 2021

Programme to select all kinematic and kinetic data from a trial, read it in from
for single cycle on each side, normalise to gait cycle, plot kinematic and kinetic
graph

@author: snbar
"""
import c3dreader
import ezc3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import numpy as np
import operator
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation

class marker_data(object):
    def __init__(self):
        self.c3dname=[]
        self.DimensionName=[]
        
class marker_c3d(object):
    def __init__(self): 
        for r in range(len(mk_list)):
            for c in range(3):
#                for s in ['L','R']:
                setattr(self, required_data.DimensionName[r][c],[])
                
class file_def(object):
        def __init__(self):
            for index,at in enumerate(attr_list):
                setattr(self,at,val_list[index])
                
attr_list=['mkr_attr']               

mk_list=['LASI','LPSI','LTHI','LKNE','LTIB','LANK','LHEE','LTOE',
         'RASI','RPSI','RTHI','RKNE','RTIB','RANK','RHEE','RTOE']                    
required_data=marker_data()    
for n in range(len(mk_list)):              
    required_data.c3dname.append(mk_list[n])
    l=[]
    for i in range(3):
        l.append(mk_list[n]+'_'+str(i+1))
    required_data.DimensionName.append(l)

      
t=marker_c3d()   
filename = 'C:\\Users\\snbar\\projects\\Data\\Pats20\\Misc\\APatient\\Helen_NF_N\\Helen_NF_N07.c3d'
#filename='C:\\Users\\snbar\\projects\\nj80102.c3d'
[required_data]=c3dreader.read_data(required_data,t,filename)

val_list=[t]
p=file_def() 
########### now make 3D graph
#get_ipython().run_line_magic('matplotlib', 'qt')
#####

fig = plt.figure(figsize=(9,9))  # figure 1 3D plot of frame i
ax = fig.add_subplot(111, projection='3d')

ax.xaxis.set_major_locator(ticker.NullLocator()) 
ax.yaxis.set_major_locator(ticker.NullLocator()) 
ax.zaxis.set_major_locator(ticker.NullLocator()) 
#ax.set_aspect("equal")
i=50
ax.plot3D([t.LASI_1[i], t.RASI_1[i], t.RPSI_1[i], t.LPSI_1[i], t.LASI_1[i]],
          [t.LASI_2[i], t.RASI_2[i], t.RPSI_2[i], t.LPSI_2[i],t.LASI_2[i]], 
          [t.LASI_3[i], t.RASI_3[i], t.RPSI_3[i], t.LPSI_3[i],t.LASI_3[i]], color='black')

# left leg
ax.plot3D([t.LASI_1[i], t.LTHI_1[i], t.LKNE_1[i], t.LTIB_1[i], t.LANK_1[i]],\
          [t.LASI_2[i], t.LTHI_2[i], t.LKNE_2[i], t.LTIB_2[i], t.LANK_2[i]],\
          [t.LASI_3[i], t.LTHI_3[i], t.LKNE_3[i], t.LTIB_3[i], t.LANK_3[i]], color='red')

# right leg
ax.plot3D([t.RASI_1[i], t.RTHI_1[i], t.RKNE_1[i], t.RTIB_1[i], t.RANK_1[i]],\
          [t.RASI_2[i], t.RTHI_2[i], t.RKNE_2[i], t.RTIB_2[i], t.RANK_2[i]],\
          [t.RASI_3[i], t.RTHI_3[i], t.RKNE_3[i], t.RTIB_3[i], t.RANK_3[i]], color='green')

# left foot
ax.plot3D([t.LANK_1[i], t.LHEE_1[i], t.LTOE_1[i], t.LANK_1[i]],\
          [t.LANK_2[i], t.LHEE_2[i], t.LTOE_2[i], t.LANK_2[i]],\
          [t.LANK_3[i], t.LHEE_3[i], t.LTOE_3[i], t.LANK_3[i]], color='red')

# right foot
ax.plot3D([t.RANK_1[i], t.RHEE_1[i], t.RTOE_1[i], t.RANK_1[i]],\
          [t.RANK_2[i], t.RHEE_2[i], t.RTOE_2[i], t.RANK_2[i]],\
          [t.RANK_3[i], t.RHEE_3[i], t.RTOE_3[i], t.RANK_3[i]], color='green')


ax.set_ylim([-1000, 1000])
ax.set_xlim([0, 2000])
ax.set_zlim([0, 2000])
ax.grid(False)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')


fig = plt.figure(figsize=(9,9))  # figure 1 3D plot of frame i
ax = fig.add_subplot(111, projection='3d')
#fig, ax = plt.subplots()
xdata, ydata, zdata = [], [], []
ln, = ax.plot3D([], [],[], 'ro')

def init():
    ax.set_ylim([-1000, 1000])
    ax.set_xlim([0, 2000])
    ax.set_zlim([0, 2000])
    return ln,

def update(frame):
    xdata.append(t.LASI_1[frame])
    ydata.append(t.LASI_2[frame])
    zdata.append(t.LASI_3[frame])
    ln.set_data(xdata, ydata, zdata)
    return ln,

ani = FuncAnimation(fig, update, frames=range(10),
                    init_func=init, blit=True)
plt.show()

#max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
#mid_x = (X.max()+X.min()) * 0.5
#mid_y = (Y.max()+Y.min()) * 0.5
#mid_z = (Z.max()+Z.min()) * 0.5
#ax.set_xlim(mid_x - max_range, mid_x + max_range)
#ax.set_ylim(mid_y - max_range, mid_y + max_range)
#ax.set_zlim(mid_z - max_range, mid_z + max_range)
#plt.show()