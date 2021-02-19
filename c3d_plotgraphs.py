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

import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))



def plot_kinematics(required_data):
    ##### plot kinematics #######
    kinematic_plot=[['PelvisAngles.y','PelvisAngles.x','PelvisAngles.z'],
                   ['HipAngles.y','HipAngles.x','HipAngles.z'],
                   ['KneeAngles.y','KneeAngles.x','FootProgressAngles.z'],
                   [None,'AnkleAngles.x','AnkleAngles.z']]
    kinematic_plot_title=[['Pelvic Obliquity','Pelvic Tilt',  'Pelvic Rotation'],
                          ['Hip Ab/Adduction','Hip Flex/Ext','Hip Rotation'],
                          ['Knee Varus/Valgus','Knee Flex/Ext','Foot Progression'],
                          [None,'Ankle Pf/Df','Ankle Rotation']]
    kinematic_plot_range=[[[-30,30],[-30,30],[-30,30]],     
                            [[-30,30],[-20,60],[-30,30]],
                            [[-30, 30],[-10,80],[-30,30]],
                            [None,[-30,30],[-30,30]]]
    
    fig = plt.figure(figsize=(8,9)) #### plot kinematics graph
    for r in range(4):
        for c in range(3):
            if kinematic_plot[r][c] is not None:
                ax = fig.add_subplot(4,3,r*3+c+1)
                ax.plot(rgetattr(required_data,'L'+kinematic_plot[r][c]),color='red')
                ax.plot(rgetattr(required_data,'R'+kinematic_plot[r][c]),color='green')
                ax.xaxis.set_major_locator(ticker.NullLocator()) 
                ax.set_ylim([kinematic_plot_range[r][c][0],kinematic_plot_range[r][c][1]])
                ax.title.set_text(kinematic_plot_title[r][c])
                ax.axhline(0,color='black')
                ax.text(-30,20,'up',rotation=90)
                ax.text(-30,-20,'down',rotation=90)
                
                
    ##### plot kinematics #######            
    kinetic_plot=[['HipAngles.y','HipMoment.y',None],
                   ['HipAngles.x','HipMoment.x','HipPower.z'],
                   ['KneeAngles.x','KneeMoment.x','KneePower.z'],
                   ['AnkleAngles.x','AnkleMoment.x','AnklePower.z']]
    kinetic_plot_title=[['Hip Ab/Adduction','Hip abductor moment',  None],
                          ['Hip Flex/Ext','Hip Extensor moment','Hip Power'],
                          ['Knee Flex/Ext','Knee Extendor moment','Knee power'],
                          ['Ankle Pf/Df','Ankle pfx moment','Ankle Power']]
    kinetic_plot_range=[[[-30,30],[-1,2],[-2,3]],     
                            [[-20,60],[-1,2],[-2,3]],
                            [[-10,80],[-1,2],[-2,3]],
                            [[-30,30],[-1,2],[-2,3]]]
    
    fig = plt.figure(figsize=(8,9))
    for r in range(4):
        for c in range(3):
            if kinetic_plot[r][c] is not None:
#                print(r,c)
                ax = fig.add_subplot(4,3,r*3+c+1)
                ax.plot(rgetattr(required_data,'L'+kinetic_plot[r][c]),color='red')
                ax.plot(rgetattr(required_data,'R'+kinetic_plot[r][c]),color='green')
                ax.xaxis.set_major_locator(ticker.NullLocator()) 
                ax.set_ylim([kinetic_plot_range[r][c][0],kinetic_plot_range[r][c][1]])
                ax.title.set_text(kinetic_plot_title[r][c])
                ax.axhline(0,color='black')
                ax.text(-30,20,'up',rotation=90)
                ax.text(-30,-20,'down',rotation=90)          
                
                
