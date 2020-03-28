"""
Snapshot Calculation Module
"""
import beto_util as util



##------- COMPARISON FUNCTIONS ---------##

def AverageCalculation(data):
    return float(sum(data))/float(len(data))
    
def GetScoreAverages(avgSnap1,avgSnap2,criteria): #Percentage returns a 0 to 1 value and Ratio can go > 1
    if criteria == "Percentage":
        return util.Round(min([avgSnap1,avgSnap2])/max([avgSnap1,avgSnap2]),"ceil",4)
    if criteria == "Ratio":
        return util.Round(avgSnap1/avgSnap2,"ceil",4)

def CompareSnaps_Averages(snap1,snap2,value): #Returns a single digit score of the average values in both snaps
    list1,list2 = [],[]
    for i in snap1:
        list1.append(i[value]) 
    for i in snap2:
        list2.append(i[value])     
    avgSnap1 = AverageCalculation(list1)
    avgSnap2 = AverageCalculation(list2)
    score = GetScoreAverages(avgSnap1,avgSnap2,"Percentage")
    #print(score)
    return score

def CompareNoteByNote(): #For Markov, return list or complex data

    pass


##-------- Main Data Function ---------##
def CompareAverages(snap1,snap2,noteType,comparisonCriteria,ratio):
    len1,len2 = float(len(snap1[noteType])),float(len(snap2[noteType]))
    
    if comparisonCriteria == "Average": #Average returns a single digit of 
        if len1 > 0 and len2 > 0:
            pos = util.Round(min([len1,len2])/max([len1,len2]),"floor",4)
            #pos = beto_util.Round(len2/len1,"floor",4)
            vel = CompareSnaps_Averages(snap1[noteType],snap2[noteType],3)
            pitch = CompareSnaps_Averages(snap1[noteType],snap2[noteType],0)
            length = CompareSnaps_Averages(snap1[noteType],snap2[noteType],2)
        elif len1 > 0 and len2 == 0:
            pos,vel,pitch,length = 0,0,0,0
        elif len2 > 0 and len1 == 0:
            pos,vel,pitch,length = 0,0,0,0
        elif len1 == 0 and len2 == 0:
            pos,vel,pitch,length = 1.0,1.0,1.0,1.0
        return pitch*ratio,pos*ratio,vel*ratio,length*ratio
    if comparisonCriteria == "Markov": #
        if len1 > 0 and len2 > 0: 
            pos = util.Round(min([len1,len2])/max([len1,len2]),"floor",4)
            #pos = beto_util.Round(len2/len1,"floor",4)
            vel = CompareSnaps_Averages(snap1[noteType],snap2[noteType],3)
            pitch = CompareSnaps_Averages(snap1[noteType],snap2[noteType],0)
            length = CompareSnaps_Averages(snap1[noteType],snap2[noteType],2)
        elif len1 > 0 and len2 == 0:
            pos,vel,pitch,length = 0,0,0,0
        elif len2 > 0 and len1 == 0:
            pos,vel,pitch,length = 0,0,0,0
        elif len1 == 0 and len2 == 0:
            pos,vel,pitch,length = 1.0,1.0,1.0,1.0
    
    