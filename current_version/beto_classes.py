"""
Just Classes
"""

##------- Classes ---------##

class Midi():
    def __init__(self,v):
        self.pitch = v[0]
        self.position = v[1]
        self.length = v[2]
        self.velocity =  v[3]

class Grid():
    def __init__(self,section_size = 4, #size in repetition 
                 repetition_size = 4, #size in bars 
                 bar_size = 4,#size in bar
                 beat_size = 4, #size in beat
                 unit_size = 0.25,
                 midi_resolution = 960): #size in unit
        #Sizes in terms of note size
        self.size_inUnits_section = section_size*repetition_size*bar_size*beat_size #256
        self.size_inUnits_repetition = repetition_size*bar_size*beat_size #64
        self.size_inUnits_bar = bar_size*beat_size #16
        self.size_inUnits_beat = beat_size #4
        self.size_inBeats_unit = unit_size #1/4
        
        self.size_inBars_section = section_size*repetition_size #barsInSect
        
        self.total_units = int(section_size*repetition_size*bar_size/unit_size)#256
        self.total_beats = bar_size*repetition_size*section_size #64
        self.total_bars = repetition_size #barnum
        self.total_repetitions = section_size #repnum
        
        self.resolution = midi_resolution*unit_size

class NoteCriteria():
    def __init__(self,ratio1,ratio2,key1 = "Notes On",key2 = "Notes Sustain"):
        self.on_ratio = ratio1
        self.sus_ratio = ratio2
        self.on = key1
        self.sus = key2

class AllSnapsScores():
    def __init__(self,pitch,position,velocity,length):
        self.pitch = pitch
        self.position = position
        self.velocity = velocity
        self.length = length

class Instructions():
    scoringMethod = "Average"
    targetMidiData = "Pitch"
    analysisCriteria = "Highest"
    harmonicProgression = range(16)
    noteOnRatio = 0.5
    noteSusRatio = 0.5
       
