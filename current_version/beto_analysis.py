"""
Module with Scoring System
"""
import beto_util as util
import beto_snaps as snaps
import beto_classes as obj

##------- DATA STORING FUNCTIONS ---------##
      
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

def SeparateSnapsByBars(midi,grid):
    bars = [[[] for j in range(grid.size_inUnits_bar)] for i in range(grid.size_inBars_section)] 
    for i in range(grid.size_inBars_section):
        for j in range(grid.size_inUnits_bar):
            bars[i][j].append(midi[j+(grid.size_inUnits_bar*i)])
    return bars

def GetAllSnapsInBars(midiSections,grid):
    allSnaps,snapsInBars = [],[]
    for i in range(len(midiSections)):
        midiSnaps = (obj.Midi(midiSections[i]))
        snapsInSection = GetSnaps(grid,midiSnaps)
        allSnaps.append(snapsInSection)
    for i in allSnaps:
        bars_ = SeparateSnapsByBars(i,grid)
        snapsInBars.append(bars_)
    return snapsInBars


##------- COMPARISON FUNCTIONS ---------##


def CompareBarsAverage(item1,item2,analysis,note):
    snaps1,snaps2 = [[] for i in range(len(item1))],[[] for i in range(len(item2))]
    
    for i in range(len(snaps1)): #snaps in bar
        note_on = item1[i][0].get(note.on) #get bar, get all snaps of that bar, get dictionary
        note_sus = item1[i][0].get(note.sus)
        snaps1[i] = [i,note_on,note_sus] 
        
    for i in range(len(snaps2)): #snaps in bar
        note_on = item2[i][0].get(note.on) #get bar, get all snaps of that bar, get dictionary
        note_sus = item2[i][0].get(note.sus)
        snaps2[i] = [i,note_on,note_sus]

    ###########     COMPARE   ############
    snapsScores = obj.AllSnapsScores([],[],[],[])
    
    for i in range(len(snaps1)):
        pitch1,pos1,vel1,len1 = snaps.CompareAverages(snaps1[i],snaps2[i],1,"Average",note.on_ratio) #on
        pitch2,pos2,vel2,len2 = snaps.CompareAverages(snaps1[i],snaps2[i],2,"Average",note.sus_ratio) #sus
        
        snapsScores.pitch.append(pitch1+pitch2)
        snapsScores.position.append(pos1+pos2)
        snapsScores.velocity.append(vel1+vel2)
        snapsScores.length.append(len1+len2)
        
    avgPitch = util.Round(snaps.AverageCalculation(snapsScores.pitch),"ceil",4)
    avgPos = util.Round(snaps.AverageCalculation(snapsScores.position),"ceil",4)
    avgVel = util.Round(snaps.AverageCalculation(snapsScores.velocity),"ceil",4)
    avgLength = util.Round(snaps.AverageCalculation(snapsScores.length),"ceil",4)
    
    if analysis == "Position":
        score = [avgPos,avgPos]
    elif analysis == "Velocity":
        score = [avgVel,avgVel]
    elif analysis == "Pitch":
        score = [avgPitch,avgPitch]
    elif analysis == "Length":
        score = [avgLength,avgLength]
    elif analysis == "No Pitch":
        score = [avgPos,avgVel,avgLength]
    elif analysis == "No Position":
        score = [avgPitch,avgVel,avgLength]
    elif analysis == "No Velocity":
        score = [avgPitch,avgPos,avgLength]
    elif analysis == "No Length":
        score = [avgPitch,avgPos,avgVel]
    elif analysis == "PosLen":
        score = [avgPos,avgLength]
    elif analysis == "PosPitch":
        score = [avgPos,avgPitch]
    elif analysis == "PosVel":
        score = [avgPos,avgVel]
    elif analysis == "PitchVel":
        score = [avgPitch,avgVel]
    elif analysis == "PitchLen":
        score = [avgPitch,avgLength]
    elif analysis == "VelLen":
        score = [avgVel,avgLength]
    else:
        score = [avgPos,avgVel,avgPitch,avgLength]
    
    scoreAverage = util.Round(snaps.AverageCalculation(score),"ceil",3)
    return scoreAverage
    
    
##------- SCORING FUNCTIONS ---------##

def sort_by_score(elem):
    return elem[0]

def SelectBar(allResults,criteria):
    if len(allResults) > 0:
        if criteria == "Highest" or "DEFAULT":
            sortedList = sorted(allResults, reverse = True, key = sort_by_score)
            return sortedList[0]
        elif criteria == "Lowest":
            sortedList = sorted(allResults, reverse = False, key = sort_by_score)
            return sortedList[0]
        elif criteria == "Second Highest":
            sortedList = sorted(allResults, reverse = True, key = sort_by_score)
            return sortedList[1]
    else:
        print("No Data on Bars")
        return [0,[[{}]],(0,0)]


def LookForBestBar(allTargets,sectionsRange,barsRange,reference,bannedBars,info):
    AllBars =[]
    noteCriteria = obj.NoteCriteria(info.NoteOnRatio,info.NoteSusRatio,"Notes On","Notes Sustain")
    for i in sectionsRange:
        sectionNumber = i
        for j in barsRange: #info.harmonicProgression
            barNumber = j
            if (sectionNumber,barNumber) in bannedBars: #CHECK FOR BANNED BARS BY 2D INDEX
                pass
            else:
                target = allTargets[sectionNumber][barNumber]
                scoreAverage = CompareBarsAverage(reference,target,info.targetMidiData,noteCriteria)
                AllBars.append([scoreAverage,target,(sectionNumber,barNumber)])
                
    singleBar = SelectBar(AllBars,info.seekType)
    return singleBar

##------- DATA ARRANGEMENT FUNCTIONS ---------##

def ConcatenateBars(AllMagicBars,grid,resolution,key = "Notes On"):
    newmidi,noteOnList = [[],[],[],[]], []
    
    for i in range(len(AllMagicBars)): #NUMBER OF 16, i = 16, 32, etc
        for j in range(len(AllMagicBars[i][1])): #NOTES IN 
            r = (AllMagicBars[i][1][j][0]).get(key)
            if r is None:
                pass
            else:
                for k in r:
                    k_ = k
                    #CREATE A SEQUENCE FROM THE POSITION ON THE MAGICBARSLIST
                    k_[1] = (util.Normalize(k[1], grid.size_inUnits_bar,grid.size_inBars_section) + grid.size_inUnits_bar*i)  
                    #print(k_[1])
                    #NORMALIZED IS 1-16 then +16*position
                    noteOnList.append(k_) #Removes Grid          
    for i in noteOnList:
        newmidi[0].append(i[1]*resolution) #PITCH
        newmidi[1].append(i[0]) #POSITION
        newmidi[2].append(i[3]) #VELOCITY
        newmidi[3].append(i[2]*resolution) #LENGTH
        
    return newmidi
    