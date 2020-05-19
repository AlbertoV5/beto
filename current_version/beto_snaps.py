"""
Snapshot Module
"""
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.patches import Rectangle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import math
 
class Get():   
    def Snapshot(midi,delta):
        note_on,note_len,note_sus_ind = [],[],[]
        
        for i in range(len(midi)):
            if midi[i][0] >= delta[0] and midi[i][0] < delta[1]:
                note_on.append(midi[i])
            elif midi[i][0] < delta[1] and midi[i][0] + midi[i][1] >= delta[1]:
                note_sus_ind.append(i)
                note_len.append(midi[i][1] + midi[i][0] - delta[0])
        return note_on,note_sus_ind,note_len
    
    def __init__(self, grid, midi, limit):
        self.snaps = []
        unit = grid.unit
        units = np.array([i*unit for i in range(limit)])
        for j in range(limit):
            delta = [units[j], units[j] + unit]
            note_on, index, note_len = Get.Snapshot(midi,delta)
            note_sus = [[midi[index[i]][0],note_len[i],midi[index[i]][2],midi[index[i]][3]] for i in range(len(index))]
            self.snaps.append([delta, note_on, note_sus])  
    

class Compare():
    def __init__(self, target, criteria, selection, weights):
        self.target = target #Position, length, pitch, velocity, etc
        self.criteria = criteria #Ratio, Percentage
        self.selection = selection #Highest, Lowest, Farthest, etc
        self.w1 = weights[0]
        self.w2 = weights[1]

    def Sequence(self, reference, bars, grid):
        sequence = []
        for i in range(len(bars)):
            for j in range(len(bars[i])):
                target = bars[i][j]
                score = Compare.SnapsAverages(self,reference,target)
                sequence.append(score)  
                #print(i,j,score)
        return sequence
    
    def SnapsAverages(self,snaps1,snaps2):
        if len(snaps1) != len(snaps2):
            return print("Not the same amount of snaps in both lists")
        
        scores = [[],[],[],[]]
        for i in range(len(snaps1)):
            position,length,pitch,velocity = CompareNotesAverage(snaps1[i][1],snaps2[i][1],self.w1,self.criteria)
            position2,length2,pitch2,velocity2 = CompareNotesAverage(snaps1[i][2],snaps2[i][2],self.w2,self.criteria)
            
            scores[0].append(position + position2)
            scores[1].append(length + length2)
            scores[2].append(pitch + pitch2)
            scores[3].append(velocity + velocity2)
        
        avgPos = Round(Average(scores[0]),"ceil",4)
        avgLength = Round(Average(scores[1]),"ceil",4)
        avgPitch = Round(Average(scores[2]),"ceil",4)
        avgVel = Round(Average(scores[3]),"ceil",4)
            
        scores = GetTargetMidiData_Scores(self.target,avgPitch,avgPos,avgVel,avgLength)
        finalScoreAverage = Round(Average(scores),"ceil",4)
        return finalScoreAverage
   
class Vector():
    def Mono(n1,n2):
        dy = Round(n2[2]-n1[2],"ceil",3)
        dx = abs(Round(n2[0]-n1[0],"ceil",3))
        dl = Round(n2[1]-n1[1],"ceil",3)
        dv = Round(n2[3]-n1[3],"ceil",3)
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
        
    def Sequence(snaps):
        snaps = [i for i in snaps if len(i[1])>0]
        control = snaps[0][1]
        sequence = [control]
        for i in range(len(snaps)):
            try:
                v = Vector.Snap(snaps[i][1],snaps[i+1][1])                    
                sequence.append(v)
            except:
                pass
        return sequence
    
class Plot():
    class ByBar():
        def Snaps(title, path, snaps, grid): 
            g = [i[0][0] for i in snaps]
            g.append(snaps[-1][0][1]) #last
            x,y,l,v = [],[],[],[]
                    
            for snap in snaps:
                for j in snap[1]:
                    x.append(j[0])
                    l.append(j[1])
                    y.append(j[2])
                    v.append(j[3])
                        
            fig,ax = plt.subplots(subplot_kw=dict())
            ax.figure.set_size_inches(28, 8)
            ax.grid(alpha = 1)
            ax.set_xlim(left = 0, right=g[len(g)-1])
            ax.set_ylim(bottom = min(y), top = max(y)+1)
            
            ax.grid(which = 'major', color='k', linestyle='-', linewidth=1, alpha = 1)
            ax.grid(which = 'minor', color='k', linestyle='-',linewidth=1, alpha = 0.3)
            ax.xaxis.set_major_locator(MultipleLocator(grid.beat))
            ax.xaxis.set_minor_locator(AutoMinorLocator(grid.beatSize))
            
            cmap = cm.get_cmap("cool")
            norm = matplotlib.colors.Normalize(vmin=0, vmax=127)
            a = (x, y, l, v)
            height = 1
            a_zipped = zip(*a)
            for a_x, a_y, a_z, a_c in a_zipped:
                _color = cmap(norm(a_c))
                ax.add_patch(Rectangle(xy=(a_x, a_y) ,
                                       width=grid.unit, height=height, linewidth=1, color=_color, fill=True))
            
            ax.scatter(x,y)
            fig.savefig(path + title+".png", transparent=False)
    
    class Score():
            
        def Step(x,y,path,title,grid):
            fig, ax = plt.subplots(figsize = (20, 8))
            ax.grid(which = 'major', color='k', linestyle='-', linewidth=1, alpha = 0.6)
            ax.grid(which = 'minor', color='k', linestyle='dotted',linewidth=1, alpha = 0.3)
            ax.xaxis.set_major_locator(MultipleLocator(grid.repetition))
            ax.xaxis.set_minor_locator(AutoMinorLocator(grid.bar))
            ax.set_xlim(left = 0, right = x[-2])
            ax.set_xticklabels = (range(len(x)))
            
            ax.set_title(label = "Rate of Change")
            ax.step(x,y, color = "m")
            ax.scatter(x,y, color = "m")
            fig.savefig(path + title + ".png", transparent=False)
            
        class ByBar():
                
            def RateOfChange(title, path, sequence, grid):
                y = [(1-i)*100 for i in sequence]
                x = [i*grid.bar for i in range(len(sequence)+1)]
                y.insert(0,0)
                Plot.Score.Step(x,y,path,title,grid)
                
            def InvRateOfChange(title, path, sequence, grid):
                y = [(i)*100 for i in sequence]
                x = [i*grid.bar for i in range(len(sequence)+1)]
                y.insert(0,0)
                Plot.Score.Step(x,y,path,title,grid)
                
     
    
##------- COMPARISON FUNCTIONS ---------##

def Round(v,typ,dec):
    if typ == "floor":
        return math.floor((10**dec)*(v))/(10**dec)
    elif typ == "ceil":
        return math.ceil((10**dec)*(v))/(10**dec)

def Average(data):
    return float(sum(data))/float(len(data))

def GetScoreAverages(avgSnap1,avgSnap2,criteria): #Percentage returns a 0 to 1 value and Ratio can go > 1
    if criteria == "Percentage":
        return Round(min([avgSnap1,avgSnap2])/max([avgSnap1,avgSnap2]),"ceil",4)
    if criteria == "Ratio":
        return Round(avgSnap1/avgSnap2,"ceil",4)

def CompareAmountOfNotes(pos1,pos2,criteria):
    if criteria == "Percentage":
        return Round(min([pos1,pos2])/max([pos1,pos2]),"floor",4)
    if criteria == "Ratio":
        return Round(pos1/pos2,"floor",4)
    
def CompareAverageNoteData(notes1,notes2,index,criteria): #Returns a single digit score of the average values in both snaps
    list1,list2 = [],[]
    for i in notes1:
        list1.append(i[index]) 
    for i in notes2:
        list2.append(i[index])     
    avgSnap1 = Average(list1)
    avgSnap2 = Average(list2)
    score = GetScoreAverages(avgSnap1,avgSnap2,criteria)
    return score

def CompareNotesAverage(notes1,notes2,ratio,criteria):
    len1,len2 = float(len(notes1)),float(len(notes2))
    if len1 > 0 and len2 > 0:
        pos = CompareAmountOfNotes(len1,len2,criteria)
        length = CompareAverageNoteData(notes1,notes2,1,criteria)
        pitch = CompareAverageNoteData(notes1,notes2,2,criteria)
        vel = CompareAverageNoteData(notes1,notes2,3,criteria)
    elif len1 > 0 and len2 == 0:
        pos,vel,pitch,length = 0,0,0,0
    elif len2 > 0 and len1 == 0:
        pos,vel,pitch,length = 0,0,0,0
    elif len1 == 0 and len2 == 0:
        pos,vel,pitch,length = 1.0,1.0,1.0,1.0
    return pos*ratio,length*ratio,pitch*ratio,vel*ratio


def GetTargetMidiData_Scores(target,pitch,pos,vel,length):
    if target == "Position":
        return [pos,pos]
    elif target == "Velocity":
        return [vel,vel]
    elif target == "Pitch":
        return [pitch,pitch]
    elif target == "Length":
        return [length,length]
    elif target == "No Pitch":
        return [pos,vel,length]
    elif target == "No Position":
        return [pitch,vel,length]
    elif target == "No Velocity":
        return [pitch,pos,length]
    elif target == "No Length":
        return [pitch,pos,length]
    elif target == "PosLen":
        return [pos,length]
    elif target == "PosPitch":
        return [pos,pitch]
    elif target == "PosVel":
        return [pos,vel]
    elif target == "PitchVel":
        return [pitch,vel]
    elif target == "PitchLen":
        return [pitch,length]
    elif target == "VelLen":
        return [vel,length]
    else:
        return [pos,vel,pitch,length]


    