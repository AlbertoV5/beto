"""
Module with Scoring System
"""
import beto_util as util
import beto_snaps as snaps
import beto_classes as obj

##------- COMPARISON FUNCTIONS ---------##

def CompareBarsAverage(bar1,bar2,targetMidiData,note,comparisonMidiData):
    if len(bar1) != len(bar2):
        return print("Not the same amount of snaps in both bars")
    
    snaps1 = snaps.GetSnapsInBar(bar1,note)
    snaps2 = snaps.GetSnapsInBar(bar2,note)
    snapsScores = obj.AllSnapsScores([],[],[],[])

    for i in range(len(snaps1)):
        pitch1,pos1,vel1,len1 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],1,note.on_ratio,comparisonMidiData)
        pitch2,pos2,vel2,len2 = snaps.CompareSnapsAverage(snaps1[i],snaps2[i],2,note.sus_ratio,comparisonMidiData)
        
        snapsScores.pitch.append(pitch1+pitch2)
        snapsScores.position.append(pos1+pos2)
        snapsScores.velocity.append(vel1+vel2)
        snapsScores.length.append(len1+len2)
    
    avgPitch = util.Round(util.average(snapsScores.pitch),"ceil",4)
    avgPos = util.Round(util.average(snapsScores.position),"ceil",4)
    avgVel = util.Round(util.average(snapsScores.velocity),"ceil",4)
    avgLength = util.Round(util.average(snapsScores.length),"ceil",4)

    scores = util.GetTargetMidiData_Scores(targetMidiData,avgPitch,avgPos,avgVel,avgLength)

    finalScoreAverage = util.Round(util.average(scores),"ceil",4)
    return finalScoreAverage
    
    
##------- SCORING FUNCTIONS ---------##

def sort_by_score_normalized(elem):
    if elem[0] > 1:
        return 1/elem[0]
    return elem[0]

def sort_by_score(elem):
    return elem[0]

def SelectBar(allResults,criteria):
    if len(allResults) > 0:
        if criteria == "Highest":
            allResults.sort(key = lambda allResults: sort_by_score(allResults)) 
            return allResults[len(allResults)-1]
        elif criteria == "Lowest":
            allResults.sort(key = lambda allResults: sort_by_score(allResults)) 
            return allResults[0]
        elif criteria == "Second Highest":
            allResults.sort(key = lambda allResults: sort_by_score(allResults))
            if len(allResults) > 1:
                return allResults[len(allResults)-2]
            else:
                return allResults[len(allResults)-1]
        elif criteria == "Closest":
            allResults.sort(key = lambda allResults: sort_by_score_normalized(allResults)) 
            return allResults[len(allResults)-1]
        elif criteria == "Farthest":
            allResults.sort(key = lambda allResults: sort_by_score_normalized(allResults)) 
            return allResults[0]
    else:
        print("No Data on Bars")
        return [0,[[{}]],(0,0)]

def LookForBestBar(allTargets,sectionsRange,barsRange,reference,bannedBars,info,barIndex):
    AllBars =[]
    noteCriteria = obj.NoteCriteria(info.noteOnRatio,info.noteSusRatio)
    for i in sectionsRange:
        sectionNumber = i
        for j in barsRange: #info.harmonicProgression
            barNumber = j
            if (sectionNumber,barNumber) in bannedBars: #CHECK FOR BANNED BARS BY 2D INDEX
                pass
            else:
                target = allTargets[sectionNumber][barNumber]
                if info.scoringMethod == "Average":
                    score = CompareBarsAverage(reference,target,info.targetMidiData,noteCriteria,info.midiDataComparison)
                AllBars.append([score,target,(sectionNumber,barNumber)])
    
    
    #print(info.selectionCriteria)
    singleBar = SelectBar(AllBars,info.selectionCriteria)
    
    if info.saveLogs == True:
        fileName = str(barIndex) + " - " + str(singleBar[0])+", "+str(singleBar[2])
        util.SaveOutputData(AllBars,info.pathOutput,fileName)

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
                    k_[1] = (util.Normalize(k[1], grid.size_inUnits_bar,grid.size_inBars_section) + grid.size_inUnits_bar*i)  
                    #print(k_[1])
                    noteOnList.append(k_) #Removes Grid          
    for i in noteOnList:
        newmidi[0].append(i[1]*resolution) #PITCH
        newmidi[1].append(i[0]) #POSITION
        newmidi[2].append(i[3]) #VELOCITY
        newmidi[3].append(i[2]*resolution) #LENGTH
        
    return newmidi
    