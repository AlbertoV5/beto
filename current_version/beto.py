"""
Main Module with General Functions
"""
import beto_analysis as an
import beto_util as util
import beto_classes as obj

##------- READING ---------##

def GetDirectories():
    root = util.gcd()
    return root + "/input", root + "/output", root + "/plot"

def ReadMidi(path,resolution,plotting):
    return util.StoreCSV(path,resolution,plotting)

def GetSnapsInBars(midiSections,grid):
    return an.GetAllSnapsInBars(midiSections,grid)

def DefineGrid(section,repetition,bar,beat,unit,midiResolution):
    return obj.Grid(section,repetition,bar,beat,unit,midiResolution)

def DefineInstructions(a = "Ratio",b= "Pitch", c = "Highest",d = [i for i in range(16)],e = {"Attack":1,"Sustain":1}):
    return obj.Instructions(a,b,c,d,e)

##------- CALL FOR ANALYSIS FUNCTIONS ---------##
def Compare_ReferenceBar_to_AllBars(grid,referenceBar,allBars,inputSectionSelection,outputSections,info):
    outputBars, bannedBars = [],[]
    barsSelection = range(0,grid.size_inBars_section) #INCLUDE ALL
    barsSelection = info.harmonicProgression
    outputLengthInBars = range(0,(outputSections-1)*grid.size_inBars_section)

    if info.analysisTechnique == "Percentage": 
        for i in outputLengthInBars:
            newBarData = an.LookForBestBar(allBars,inputSectionSelection,barsSelection,referenceBar,bannedBars,info)
            outputBars.append(newBarData) 
            referenceBar = newBarData[1]
            bannedBars.append(newBarData[2])
            
    return outputBars

def GetMarkovChains():
    
    
    pass
    
##------- DATA ---------##

def PrintList(all_bars):
    print("\nAll Bars:")
    for i in all_bars:
        print(i[0],i[2])
        
##------- WRITING ---------##
       
def CreateNewMidi(BarList,grid,resolution,name,path,plotting):
    newMidiFile = an.ConcatenateBars(BarList,grid,resolution,"Notes On")
    if plotting[0] == True:
        util.PlotPiece(newMidiFile[0],newMidiFile[1],plotting[1]+"/",plotting[2])
    util.WriteCSV(newMidiFile,name,path)
   
        
