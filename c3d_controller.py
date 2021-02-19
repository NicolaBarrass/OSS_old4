# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:56:52 2021

@author: snbar
"""

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG 
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 

import io


def make_graph(data,title,ran):
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(data)
    
    ax.xaxis.set_major_locator(ticker.NullLocator()) 
    ax.set_ylim(ran)
    ax.set_title(title,size = 42)
    ax.axhline(0,color='black')
    ax.text(-30,20,'up',rotation=90)
    ax.text(-30,-20,'down',rotation=90)
    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output

# import c3dreader
# import ezc3d
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker 
# import numpy as np
# import operator

import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))



def plot_kinematics(rep_data):
    ##### plot kinematics #######
    print('in plot kinematics')
    # print(dir(rep_data.apps))
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
    
    # print('in plot kineamtics')     
    # for a in rep_data.apps:
    #     for c in a.condition:
    #         for t in c.trial:
    #             required_data=t.c3d.kin
                
    
    
    fig = plt.figure(figsize=(8,9)) #### plot kinematics graph
    for r in range(4):
        for cl in range(3):
            if kinematic_plot[r][cl] is not None:
                ax = fig.add_subplot(4,3,r*3+cl+1)
                for a in rep_data.apps:
                    for c in a.condition:
                        for t in c.trial:
                            required_data=t.c3d.kin
                            ax.plot(rgetattr(required_data,'L'+kinematic_plot[r][cl]),color='red')
                            ax.plot(rgetattr(required_data,'R'+kinematic_plot[r][cl]),color='green')
                ax.xaxis.set_major_locator(ticker.NullLocator()) 
                ax.set_ylim([kinematic_plot_range[r][cl][0],kinematic_plot_range[r][cl][1]])
                ax.title.set_text(kinematic_plot_title[r][cl])
                ax.axhline(0,color='black')
                ax.text(-30,20,'up',rotation=90)
                ax.text(-30,-20,'down',rotation=90)
                
    print('about to save fig')
    plt.savefig('C:/Users/snbar/Anaconda3/envs/OSS/app/static/images/kinematic_plot.png')
    print('fig saved')
    
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return output
                
def plot_kinetics(rep_data):               
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
        for cl in range(3):
            if kinetic_plot[r][cl] is not None:
#                print(r,c)
                ax = fig.add_subplot(4,3,r*3+cl+1)
                for a in rep_data.apps:
                    for c in a.condition:
                        for t in c.trial:
                            required_data=t.c3d.kin
                            ax.plot(rgetattr(required_data,'L'+kinetic_plot[r][cl]),color='red')
                            ax.plot(rgetattr(required_data,'R'+kinetic_plot[r][cl]),color='green')
                ax.xaxis.set_major_locator(ticker.NullLocator()) 
                ax.set_ylim([kinetic_plot_range[r][cl][0],kinetic_plot_range[r][cl][1]])
                ax.title.set_text(kinetic_plot_title[r][cl])
                ax.axhline(0,color='black')
                ax.text(-30,20,'up',rotation=90)
                ax.text(-30,-20,'down',rotation=90)
                
    plt.savefig('C:/Users/snbar/Anaconda3/envs/OSS/app/static/images/kinetic_plot.png')            
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return output             
    
    
def plot_bokeh(rep_data):
    print('in graph')
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
    from bokeh.io import curdoc
    from bokeh.resources import INLINE
    from bokeh.embed import components
    from bokeh.layouts import column, row
    from bokeh.models import Select
    from bokeh.palettes import Spectral5
    from bokeh.models.callbacks import CustomJS
    # from bokeh.plotting import curdoc, 
    # from bokeh.plotting import figure, output_file, show
    
    print('in plot bokeh')     
    for a in rep_data.apps:
        print(a.doa_str)
        for c in a.condition:
            print(c.footware)
            for t in c.trial:
                print(t.c3dfile)
    
    # def update(attr, old, new):
    #     print('UPDATING')
    #     source.data=dict(
    #         y=getattr(required_data, new)
    #     )

    source = ColumnDataSource()
    
    fig = figure(plot_height=600, plot_width=720, tooltips=[("Title", "@title"), ("Released", "@released")])
    fig.line(x="x",y="y", source=source, color="#FF9900")
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
    
    tm=[]
    for i in range(51):
        tm.append(i/50)
        
        
    for a in rep_data.apps:
        for c in a.condition:
            for t in c.trial:
                print (t.c3dfile)
                required_data=t.c3d.kin
    
    # print('###########################')
    # print (required_data.__dict__)
    #             # try:
    #             #     required_data=t.c3d.kin
    #             # except:
    #             #     print('not able to use')
        
    source.data=dict(
        x=tm,
        y=required_data.LKneeAngles.x,
        r=required_data.LHipAngles.x,
        
        
        )
    
    print(required_data.LKneeAngles.x)
    
    columns=dir(required_data)
    for word in columns[:]:
        if word.startswith('_'):
            columns.remove(word)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var x = data['x'];
        var y = data['r'];
        console.log(y);

        source.change.emit();
    """)
    
    
    x = Select(title='X-Axis', value='mpg', options=columns)
    x.js_on_change('value', callback)
    
    # y = Select(title='Y-Axis', value='hp', options=columns)
    # y.on_change('value', update)
        
    controls = column(x, width=200)
    layout = row(controls, fig)
    
    curdoc().add_root(layout)
    curdoc().title = "Crossfilter"
    
    return layout