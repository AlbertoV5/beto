"""
Module with Scoring System
"""
import beto_util as util
import beto_snaps as snaps
import beto_classes as obj

##------- COMPARISON FUNCTIONS ---------##

def CompareBarsAverage(bar1,bar2,targetMidiData,note):
    if len(bar1) != len(bar2):
        return print("Not the same amount of snaps in both bars")
    
    snaps1 = snaps.GetSnapsInBar(bar1,note)
    snaps2 = snaps.GetSnapsInBar(bar2,note)
    snapsScores = obj.AllSnapsScores([],[],[],[])

    for i in range(len(snaps1)):
        pitch1,pos1,vel1,len1 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],1,note.on_ratio)
        pitch2,pos2,vel2,len2 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],2,note.sus_ratio)
        
        snapsScores.pitch.append(pitch1+pitch2)
        snapsScores.position.append(pos1+pos2)
        snapsScores.velocity.append(vel1+vel2)
        snapsScores.length.append(len1+len2)
    
    avgPitch = util.Round(util.average(snapsScores.pitch),"ceil",4)
    avgPos = util.Round(util.average(snapsScores.position),"ceil",4)
    avgVel = util.Round(util.average(snapsScores.velocity),"ceil",4)
    avgLength = util.Round(util.average(snapsScores.length),"ceil",4)

    scores = util.GetTargetMidiData_Scores(targetMidiData,avgPitch,avgPos,avgVel,avgLength)

    finalScoreAverage = util.Round(util.average(scores),"ceil",3)
    return finalScoreAverage
    

def CompareBarsPercentage(bar1,bar2,targetMidiData,note):
    if len(bar1) != len(bar2):
        return print("Not the same amount of snaps in both bars")
    
    snaps1 = snaps.GetSnapsInBar(bar1,note)
    snaps2 = snaps.GetSnapsInBar(bar2,note)
    snapsScores = obj.AllSnapsScores([],[],[],[])
    
    for i in range(len(snaps1)):
        pitch1,pos1,vel1,len1 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],1,note.on_ratio)
        pitch2,pos2,vel2,len2 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],2,note.sus_ratio)
        
        snapsScores.pitch.append(pitch1+pitch2)
        snapsScores.position.append(pos1+pos2)
        snapsScores.velocity.append(vel1+vel2)
        snapsScores.length.append(len1+len2)
    
    avgPitch = util.Round(util.average(snapsScores.pitch),"ceil",4)
    avgPos = util.Round(util.average(snapsScores.position),"ceil",4)
    avgVel = util.Round(util.average(snapsScores.velocity),"ceil",4)
    avgLength = util.Round(util.average(snapsScores.length),"ceil",4)
    
    scores = util.GetTargetMidiData_Scores(targetMidiData,avgPitch,avgPos,avgVel,avgLength)
    
    finalScoreAverage = util.Round(util.average(scores),"ceil",3)
    return finalScoreAverage
    
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
    noteCriteria = obj.NoteCriteria(info.noteOnRatio,info.noteSusRatio) #Defaults the keys
    for i in sectionsRange:
        sectionNumber = i
        for j in barsRange: #info.harmonicProgression
            barNumber = j
            if (sectionNumber,barNumber) in bannedBars: #CHECK FOR BANNED BARS BY 2D INDEX
                pass
            else:
                target = allTargets[sectionNumber][barNumber]
                if info.scoringMethod == "Average":
                    score = CompareBarsAverage(reference,target,info.targetMidiData,noteCriteria)
                if info.scoringMethod == "Percentage":
                    score = CompareBarsPercentage(reference,target,info.targetMidiData,noteCriteria)
                AllBars.append([score,target,(sectionNumber,barNumber)])
                
    singleBar = SelectBar(AllBars,info.selectionCriteria)
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
                    noteOnList.append(k_) #Removes Grid          
    for i in noteOnList:
        newmidi[0].append(i[1]*resolution) #PITCH
        newmidi[1].append(i[0]) #POSITION
        newmidi[2].append(i[3]) #VELOCITY
        newmidi[3].append(i[2]*resolution) #LENGTH
        
    return newmidi
    