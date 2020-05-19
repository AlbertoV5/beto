import os
import pandas as pd
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.patches import Rectangle

def GetDirectories(sub):
    root = os.getcwd()
    return root + sub + "/input", root + sub + "/output", root + sub + "/plot"

class Grid():
    def __init__(self,repetitions, bars, beats,units, resolution):
        self.sectionSize = repetitions*bars*beats*units #256
        self.repetitionSize = bars*beats*units #64
        self.barSize = beats*units #16
        self.beatSize = units #4
        
        self.beat = resolution
        self.unitSize = 1/units #0.25
        self.measure = beats*resolution
        
        self.bar = resolution*bars
        self.unit = resolution/units
        self.section = self.unit*self.sectionSize
        self.repetition = self.unit*self.repetitionSize

        self.size_inBars_section = repetitions*bars #barsInSect
        
        self.total_units = int(repetitions*bars*beats/self.unitSize)#256
        self.total_beats = repetitions*bars*beats #64
        self.total_bars = bars*repetitions #16
        self.total_repetitions = repetitions #4
                
        
class Collection():
    def __init__(self,path):
        files = [path+"/"+i for i in os.listdir(path) if ".csv" in i]
        files = sorted(files)
        print("Found: " + str(len(files)) + " .csv files.")
        self.collection = []
        self.sections = [[] for i in range(len(files))]
        
        for file in range(len(files)):
            csv = pd.read_csv(files[file])
            pitch = np.array([float(i) for i in csv["Pitch"]])
            position = np.array([float(i) for i in csv["Position"]])
            length = np.array([float(i) for i in csv["Length"]])
            velocity = np.array([int(i) for i in csv["Velocity"]])
            
            for i in range(pitch.size):
                self.collection.append([position[i], rnd(length[i]), pitch[i], velocity[i]])
                self.sections[file].append([position[i], rnd(length[i]), pitch[i], velocity[i]])
            
    def GetBarsInSection(self, section, grid):
        bar, bars, counter = [], [], 1
        for i in section:
            if grid.measure*counter <= i[0]:
                bars.append(bar)
                bar = [i]
                counter += 1
            else:
                bar.append(i)
        bars.append(bar) #for last
        return bars
    
    
    def GetNormalizedBars(self, section, grid):
        bar, bars, counter = [], [], 1
        for i in section:
            if i[0] >= grid.measure*counter:
                bars.append(bar)
                bar = []
                bar.append([norm(i[0],grid.measure*(counter)),i[1],i[2],i[3]])
                counter += 1
            else:
                bar.append([norm(i[0],grid.measure*(counter-1)),i[1],i[2],i[3]])
                
        bars.append(bar) #for last
        return bars
    
class Vector():
    def Mono(n1,n2):
        dy = rnd(n2[2]-n1[2])
        dx = abs(rnd(n2[0]-n1[0]))
        dl = rnd(n2[1]-n1[1])
        dv = rnd(n2[3]-n1[3])
        return [dx,dl,dy,dv]
        
    def Poly(n1,n2):          
        y1 = [i[2] for i in n1]
        y2 = [i[2] for i in n2]
        vectors = []
        for i in range(len(y2)):
            c = np.array(y1)[np.abs(np.array(y1) - y2[i]).argmin()]
            n = y1.index(c)
            a = n1[n]
            b = n2[i]
            if b[0] > a[0]:
                vectors.append(Vector.Mono(a,b)) 
            else:
                vectors.append(Vector.Mono(b,a))
        return vectors
        
    def Snap(notes1,notes2):
        if len(notes1) == 0 and len(notes2) == 0:
            return []
        elif len(notes1) == 1 and len(notes2) == 1:
            return [Vector.Mono(notes1[0],notes2[0])]
        elif len(notes1) > len(notes2):
            return Vector.Poly(notes1,notes2)
        elif len(notes2) > len(notes1):
            return Vector.Poly(notes2,notes1)
        
    def Sequence(data):
        sequence = []
        for i in range(len(data)):
            print(data[i])
            try:
                v = Vector.Snap(data[i],data[i+1])                    
                sequence.append(v)
            except:
                pass
        return sequence
    

def norm(original, limit):
    if original >= limit:
        return original - limit
    else:
        return original
        
class Plot():
    def MidiBar(title, path, b, color, grid):
        bar = [[j[0] for j in b], [j[1] for j in b], [j[2] for j in b], [j[3] for j in b]]
        fig,ax = plt.subplots(subplot_kw=dict())
        ax.figure.set_size_inches(25, 10)
        ax.grid(alpha = 1)
        cmap = matplotlib.cm.get_cmap(color)
        norm = matplotlib.colors.Normalize(vmin=0, vmax=127)
        ax.set_xlim(left = 0, right=grid.bar)
        
        ax.grid(which = 'major', color='k', linestyle='-', linewidth=1, alpha = 1)
        ax.grid(which = 'minor', color='k', linestyle='-',linewidth=1, alpha = 0.3)
        ax.xaxis.set_major_locator(MultipleLocator(grid.beat))
        ax.xaxis.set_minor_locator(AutoMinorLocator(grid.beatSize))
        a = (bar[0], bar[2], bar[1], bar[3])
        height = 1
        a_zipped = zip(*a)
        for a_x, a_y, a_z, a_c in a_zipped:
            _color = cmap(norm(a_c))
            ax.add_patch(Rectangle(xy=(a_x, a_y-height/2) ,
                                   width=a_z, height=height, linewidth=1, color=_color, fill=True))
        ax.scatter(bar[0],bar[2], s = 0)
        fig.savefig(path + title+".png", transparent=False)
    


def WriteCSV(newMidi,name,path): 
    d = {'Pitch': newMidi[1],'Position': newMidi[0],'Velocity': newMidi[2],"Length": newMidi[3]}
    df = pd.DataFrame(data = (d))
    df.to_csv(path_or_buf = path + "/"+ name +".csv", index=False)  
    print("Done writing to path.")


def rnd(num):
    num = num * 1000
    return (math.ceil(num))/1000