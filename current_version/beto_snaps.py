"""
Snapshot Calculation Module
"""
import beto_util as util
import beto_classes as obj

##------- FIRST DATA MANAGEMENT FUNCTIONS ---------##
      
def CalculateSnapshot(midi,snapUnit):
    note_on,sus_index,note_sus = [],[],[]
    for k in range(len(midi.pitch)):
        if midi.position[k] == snapUnit:
            note_on.append(k)
        elif midi.position[k] < snapUnit and midi.position[k] + midi.length[k] > snapUnit:
            sus_index.append(k)
            note_sus.append(midi.length[k] + midi.position[k] - snapUnit)
    return note_on,sus_index,note_sus

def GetSnaps(grid,midi):
    notes = []
    for unit in range(grid.size_inUnits_section):
        start_index, pedal_index, pedal_len = CalculateSnapshot(midi,unit)
        notes.append(
        {"Notes On":[[midi.pitch[i],midi.position[i],midi.length[i],midi.velocity[i]] for i in start_index],
         "Notes Sustain":[[midi.pitch[pedal_index[i]],midi.position[pedal_index[i]],pedal_len[i],midi.velocity[pedal_index[i]]] for i in range(len(pedal_index))]})
    return notes


def GetAllSnapsInSections(midiSections,grid):
    snapsInSections = []
    for i in range(len(midiSections)):
        midiSnaps = (obj.Midi(midiSections[i]))
        currentSections = GetSnaps(grid,midiSnaps)
        snapsInSections.append(currentSections)
    return snapsInSections
    
def SplitSection_InSnapsInBars(midi,grid):
    snapsInBars = [[[] for j in range(grid.size_inUnits_bar)] for i in range(grid.size_inBars_section)] 
    for i in range(grid.size_inBars_section):
        for j in range(grid.size_inUnits_bar):
            snapsInBars[i][j].append(midi[j+(grid.size_inUnits_bar*i)])
    return snapsInBars

def GetAllSnapsInBars(midiSections,grid):
    snapsInBars = []
    snapsInSections = GetAllSnapsInSections(midiSections,grid)
    for i in snapsInSections:
        currentSection = SplitSection_InSnapsInBars(i,grid)
        snapsInBars.append(currentSection)
    return snapsInBars

##------- SECOND DATA MANAGEMENT FUNCTIONS ---------##

def GetSnapsInBar(item,note):
    snaps = []
    for i in range(len(item)): #snaps in bar
        note_on = item[i][0].get(note.on) #get bar, get all snaps of that bar, get dictionary
        note_sus = item[i][0].get(note.sus)
        snaps.append([i,note_on,note_sus])
    return snaps

##------- COMPARISON FUNCTIONS ---------##

def GetScoreAverages(avgSnap1,avgSnap2,criteria): #Percentage returns a 0 to 1 value and Ratio can go > 1
    if criteria == "Percentage":
        return util.Round(min([avgSnap1,avgSnap2])/max([avgSnap1,avgSnap2]),"ceil",4)
    if criteria == "Ratio":
        return util.Round(avgSnap1/avgSnap2,"ceil",4)

def CompareAmountOfNotes(pos1,pos2,criteria):
    if criteria == "Percentage":
        return util.Round(min([pos1,pos2])/max([pos1,pos2]),"floor",4)
    if criteria == "Ratio":
        return util.Round(pos1/pos2,"floor",4)
    
def CompareAverageNoteData(snap1,snap2,value,criteria): #Returns a single digit score of the average values in both snaps
    list1,list2 = [],[]
    for i in snap1:
        list1.append(i[value]) 
    for i in snap2:
        list2.append(i[value])     
    avgSnap1 = util.average(list1)
    avgSnap2 = util.average(list2)
    score = GetScoreAverages(avgSnap1,avgSnap2,criteria)
    return score

def CompareNoteByNote(): #For Markov, return list or complex data

    pass

def CompareSnapsAverage(snap1,snap2,noteType,ratio,comparison):
    len1,len2 = float(len(snap1[noteType])),float(len(snap2[noteType]))
    if len1 > 0 and len2 > 0:
        pos = CompareAmountOfNotes(len1,len2,comparison)
        pitch = CompareAverageNoteData(snap1[noteType],snap2[noteType],0,comparison)
        length = CompareAverageNoteData(snap1[noteType],snap2[noteType],2,comparison)
        vel = CompareAverageNoteData(snap1[noteType],snap2[noteType],3,comparison)
    elif len1 > 0 and len2 == 0:
        pos,vel,pitch,length = 0,0,0,0
    elif len2 > 0 and len1 == 0:
        pos,vel,pitch,length = 0,0,0,0
    elif len1 == 0 and len2 == 0:
        pos,vel,pitch,length = 1.0,1.0,1.0,1.0
    return pitch*ratio,pos*ratio,vel*ratio,length*ratio





    