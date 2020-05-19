import beto_snaps as snp
import beto_midi as m1d1

input_path, output_path, plot_path = m1d1.GetDirectories("/test")
grid = m1d1.Grid(4,4,4,4,1)
midi = m1d1.Collection(input_path)

bars, sections = [],[]

b1 = midi.GetNormalizedBars(midi.sections[11], grid)[0]
b2 = midi.GetNormalizedBars(midi.sections[11], grid)[1]

m1d1.Plot.MidiBar("bar1", plot_path, b1, "spring", grid)
m1d1.Plot.MidiBar("bar2", plot_path, b2, "spring", grid)

#SNAPS
for i in range(len(midi.sections)):
    bars.append([])
    barsInSection = midi.GetNormalizedBars(midi.sections[i], grid)
    for bar in barsInSection:
        SnapsInBar = snp.Get(grid, bar, grid.barSize)
        bars[i].append(SnapsInBar.snaps)
        
snp.Plot.ByBar.Snaps("Snaps1", plot_path, bars[11][0], grid)
snp.Plot.ByBar.Snaps("Snaps2", plot_path, bars[11][1], grid)

compare = snp.Compare(target = "Position", criteria = "Percentage", selection = "Highest", weights = [1,0])
sequence = compare.Sequence(bars[0][0], bars, grid)

snp.Plot.Score.ByBar.RateOfChange("Rate of change", plot_path, sequence, grid)

def Evaluate2Bars():
    for i in range(len(bars[0][0])):
        notes1 = bars[11][0][i][1]
        notes2 = bars[11][1][i][1]
        a,b,c,d = snp.CompareNotesAverage(notes1,notes2,1,"Ratio")
        print(a,b,c,d)
    
    compare = snp.Compare(target = "Position", criteria = "Percentage", selection = "Highest", weights = [1,0])
    print(compare.SnapsAverages(bars[0][0],bars[0][1]))

#Evaluate2Bars()

print(snp.Vector.Sequence(bars[0][0]))


