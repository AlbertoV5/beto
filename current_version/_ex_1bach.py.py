"""
Python 3.7
Re-Compose a Piece - Iteration 06
"""
import beto
#-------------------------------------------------------#
##----------Example #1 Re Composing a Bach Piece--------#
#-------------------------------------------------------#
input_path, output_path, plot_path = beto.GetDirectories()
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
instrumentEnvelopeRatio = ier = {"Attack":2,"Sustain":1}

instructions = beto.DefineInstructions()
##----------Instructions--------#
instructions.targetMidiData = "Pitch"
instructions.scoringMethod = "Average"
instructions.midiDataComparison = "Ratio"
instructions.selectionCriteria = "Closest"
instructions.harmonicProgression = range(0,grid.size_inBars_section)
instructions.NoteOnRatio = ier["Attack"]/(ier["Attack"]+ier["Sustain"])
instructions.NoteSusRatio = ier["Sustain"]/(ier["Attack"]+ier["Sustain"])
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
