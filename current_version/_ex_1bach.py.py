"""
Re-Compose a Piece
"""
import beto

#-------------------------------------------------------#
##----------Example #1 Re Composing a Bach Piece--------#
#-------------------------------------------------------#
input_path, output_path, plot_path = beto.GetDirectories()
##------------CONFIG--------------##
midiResolution = 960
# A grid consists of:
# num of repetitions in section
# num of bars in a repetition
# num of beats in a bar
# num of units in a beat
# num of beats in a unit
# resolution of midi in tick per beat
grid = beto.DefineGrid(1,4,4,4,0.25,midiResolution) #<---Static Grid
dGrid = [grid] #<--- Dynamic Grid, as a list of grids that are called depending on instructions
##----------READ MIDI CSV---------##
plotInput = [True,plot_path,"Original",15360] #Plot?, Label, Length, output path
midiFiles = beto.ReadMidi(input_path,grid.resolution,plotInput)
##---------------------------#
##------------Setup----------#
bars = beto.GetSnapsInBars(midiFiles,grid)
referenceBar = bars[0][0]
inputSections = range(0,13)
outputSections = 14
harmonicProgression = range(0,grid.size_inBars_section) #Design a change in chord progression
instrumentEnvelopeRatio = {"Attack":2,"Sustain":1} #Related to notes Start and Pedal

##----------Execution--------#
instructions = beto.DefineInstructions("Percentage","Pitch","Highest",harmonicProgression,instrumentEnvelopeRatio)
ReComposed = beto.Compare_ReferenceBar_to_AllBars(grid,referenceBar,bars,inputSections,outputSections,instructions)
#MarkovData = beto.GetMarkovChains(grid,bars,sectionSelection,instructions)

##----------Visualize Data--------#
#beto.PlotSnapsInBar(referenceBar,my_path)
#beto.PrintList(MagicBarsList)

##----------Output--------#
plotOutput = [True,plot_path,"Re-Composed"]
beto.CreateNewMidi(ReComposed,grid,grid.resolution,"newmidi",output_path,plotOutput)
