"""
Main Module with General Functions
"""
import beto_analysis as an
import beto_util as util
import beto_classes as obj
import beto_snaps as snap

##------- READING ---------##

def GetDirectories():
    root = util.gcd()
    return root + "/input", root + "/output", root + "/plot"

def ReadMidi(path,resolution,plotting):
    return util.StoreCSV(path,resolution,plotting)

def GetSnapsInBars(midiSections,grid):
    return snap.GetAllSnapsInBars(midiSections,grid)

def DefineGrid(section,repetition,bar,beat,unit,midiResolution):
    return obj.Grid(section,repetition,bar,beat,unit,midiResolution)

def DefineInstructions():
    return obj.Instructions()

##------- CALL FOR ANALYSIS FUNCTIONS ---------##
def Sequencial_ReferenceBar_to_AllBars(grid,referenceBar,allBars,inputSectionSelection,outputSections,info):
    outputBars, bannedBars = [],[]
    outputLengthInBars = range(0,(outputSections-1)*grid.size_inBars_section)
    
    if info.saveLogs == True:
        util.ClearLogs(info.pathOutput)

    for i in outputLengthInBars:
        newBarData = an.LookForBestBar(allBars,inputSectionSelection,info.harmonicProgression,referenceBar,bannedBars,info,i)
        outputBars.append(newBarData) 
        referenceBar = newBarData[1]
        bannedBars.append(newBarData[2])
            
    return outputBars

def GetMarkovChains():
    
    
    pass
    
##------- DATA ---------##

def PrintList(all_bars,path):
    print("\nAll Bars:")
    for i in all_bars:
        print(i[0],i[2])
               
##------- WRITING ---------##
       
def CreateNewMidi(BarList,grid,resolution,name,path,plotting,info):
    newMidiFile = an.ConcatenateBars(BarList,grid,resolution,"Notes On")
    if plotting[0] == True:
        util.PlotPiece(newMidiFile[0],newMidiFile[1],plotting[1]+"/",plotting[2])
    util.WriteCSV(newMidiFile,name,path)
    if info.saveLogs == True:
        util.SaveOutputData(BarList,path,"_allBars")
   
    