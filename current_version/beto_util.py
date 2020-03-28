"""
Module for Storage and Math functions
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import math

##------- MATH FUNCTIONS ---------##

def Round(v,typ,dec):
    if typ == "floor":
        return math.floor((10**dec)*(v))/(10**dec)
    elif typ == "ceil":
        return math.ceil((10**dec)*(v))/(10**dec)

def Normalize(num,unitsInBar,barsInSection,result=0): #
    r = [i*unitsInBar for i in range(barsInSection)]
    for i in range(barsInSection):
        if num >= r[i] and num < r[i]+unitsInBar:
            result = num - r[i]
            break
        else:
            result = num
    return result
  
##------- DATA MANAGEMENT FUNCTIONS ---------##

def gcd():
    return os.getcwd()
  
def GetFiles(directory):
    files_list = os.listdir(directory)
    files = [directory+i for i in files_list if ".csv" in i]
    print("Found: " + str(len(files)) + " .csv files.")
    return sorted(files)

def WriteCSV(newMidi,name,path): 
    d = {'Pitch': newMidi[1],'Velocity': newMidi[2],'Position': newMidi[0],"Length": newMidi[3]}
    df = pd.DataFrame(data = (d))
    df.to_csv(path_or_buf = path + "/"+ name +".csv", index=False)  
    print("Done writing to path.")
    
    
def StoreCSV(path,resolution,plotOptions):
    files = GetFiles(path+"/")
    allMidiFiles,xax,yax = [[] for i in files],[],[]
    
    for k in range(len(files)):
        v = pd.read_csv(files[k])
        allMidiFiles[k] = [
                [float(i) for i in v["Pitch"]],
                [float(i/resolution) for i in v["Position"]],
                [(math.ceil(1000*(float(i/resolution))))/1000 for i in v["Length"]],
                [int(i) for i in v["Velocity"]]
                ]
        if plotOptions[0] == True:
            for i in allMidiFiles[k][0]:
                xax.append(i)
            for i in allMidiFiles[k][1]:
                yax.append((i*resolution)+plotOptions[3]*k)
    #PLOTS CONCATENATED DATA IN THE SAME LIST, THEN PLOT ALL THE READ FILES (ENTIRE PIECE)
    if plotOptions[0] == True:
        PlotPiece(yax,xax,plotOptions[1]+"/",plotOptions[2])
            
    return allMidiFiles

##------- DATA VISUALIZATION FUNCTIONS ---------##

def PlotPiece(yax,xax,path,name): 
    figi,axi = plt.subplots(figsize=(20,10))
    axi.plot(yax,xax)
    axi.grid(alpha = 1.0)
    figi.savefig(path+name)
    figi.show()
    

def PlotScatterSnaps(xDF,yDF,name,color,path):   
    fig, ax = plt.subplots(figsize = (6,10))
    ax.set_xticks([i for i in range(0)])
    ax.set_yticks([(i*4 + 24) for i in range(18)])
    ax.set_ylim(36, 96)
    ax.grid(which = 'major', color='k', linestyle='-', linewidth=1, alpha = 0.2)
    ax.scatter(xDF,yDF,marker = "s", s = 1000, c = color)
    fig.savefig(path+"/output"+"/snaps/"+name,transparent = True)
    fig.show()
    
def PlotSnapsInBar(bar,path):
    #print("\nGRAPHS:\n")
    for i in range(len(bar)):
        x1,y1,x2,y2 = [],[],[],[]
        snap = bar[i][0]
        start = snap.get("Start Notes")
        pedal = snap.get("Pedal Notes")
        for j in start:
            y1.append(j[0])
            x1.append(0)
        if len(x1) == 0:
            x1,y1 = [0],[0]
        PlotScatterSnaps(x1,y1,"Snap"+str(i),"r")
        for j in pedal:
            y2.append(j[0])
            x2.append(0)
        if len(x2) == 0:
            x2,y2 = [0],[0]
        #print(x1,y1,x2,y2)
        PlotScatterSnaps(x2,y2,"Snap"+str(i)+"pedal","b",path)
        
