"""
Python 3.7
Re-Compose a Piece - Iteration 07
"""
import beto


input_path, output_path, plot_path = beto.GetDirectories("/bach1")
##------------CONFIG--------------##
midiResolution = 960
grid = beto.DefineGrid(1,4,4,4,0.25,midiResolution)
dynamicGrid = [grid] 
##----------READ MIDI CSV---------##
plotInput = [True,plot_path,"Original",15360] #temp
midiFiles = beto.ReadMidi(input_path,grid.resolution,plotInput)
##---------------------------#
##------------Setup----------#
##---------------------------#
bars = beto.GetSnapsInBars(midiFiles,grid)
referenceBar = bars[0][0]
inputSections = range(0,13)
outputSections = 14

instructions = beto.DefineInstructions()
##----------Instructions--------#
instructions.targetMidiData = "Pitch"
instructions.scoringMethod = "Average"
instructions.midiDataComparison = "Ratio"
instructions.selectionCriteria = "Closest"
instructions.harmonicProgression = range(0,grid.size_inBars_section)
instructions.set_noteOnRatio(1)
instructions.set_noteSusRatio(0)
instructions.saveLogs = True
instructions.pathOutput = output_path

##----------Execution--------#
ReCompose = beto.Sequencial_ReferenceBar_to_AllBars(grid,referenceBar,bars,inputSections,outputSections,instructions)
#MarkovData = beto.GetMarkovChains(grid,bars,sectionSelection,instruction)

##----------Visualize Data--------#
#beto.PlotSnapsInBar(referenceBar,my_path)
#beto.PrintList(ReCompose,output_path)

##----------Output--------#
plotOutput = [True,plot_path,"Re-Composed"]
beto.CreateNewMidi(ReCompose,grid,grid.resolution,"newmidi",output_path,plotOutput,instructions)
