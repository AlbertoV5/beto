import beto_midi as m1d1
import beto_snaps as snp
import os

path = os.getcwd() + "/test/input"
grid = m1d1.Grid(4, 4, 4, 4)

midi = m1d1.Collection(path)
SnapsInSection = snp.Get(grid, midi.sections[0], grid.sectionSize)

# Collection and Sections obtained with __init__, bars and beats obtained with separated methods
bars = midi.GetBarsInSection(midi.sections[0], grid)

SnapsInBar = snp.Get(grid, bars[0], grid.barSize)

print(bars[0])