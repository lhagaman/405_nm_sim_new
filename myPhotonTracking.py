import rat
import ROOT
import sys
import runCheckTools as RCT
import json
import matplotlib.pyplot as plt

# Get command line arguments
cmdArgs = sys.argv

file_name = '~/Desktop/RAT_files/405_nm_sim/output.root'

fileIterator = rat.dsreader(file_name)

print_all_steps = False
if print_all_steps:
    for iEntry, anEntry in enumerate(fileIterator):
        print("########################## NEW MC ######################")
        MC = anEntry.GetMC()
        num_tracks = MC.GetMCTrackCount()
        print('num_tracks: ', num_tracks)
        track = MC.GetMCTrack(0)
        starting_momentum = track.GetMCTrackStep(0).GetMomentum()
        for i in range(track.GetMCTrackStepCount()):
            step = track.GetMCTrackStep(i)
            endpoint = step.GetEndpoint()
            volume = step.GetVolume()
            momentum = step.GetMomentum()
            process = step.GetProcess()
            print("######### NEW STEP #########")
            print('endpoint: ', endpoint[0], endpoint[1], endpoint[2])
            print('momentum: ', momentum[0], momentum[1], momentum[2])
            print('volume: ', volume)
            print('process: ', process)

print_all_momentum_changes = False
if print_all_momentum_changes:
    for iEntry, anEntry in enumerate(fileIterator):
        MC = anEntry.GetMC()
        num_tracks = MC.GetMCTrackCount()
        track = MC.GetMCTrack(0)
        starting_momentum = track.GetMCTrackStep(0).GetMomentum()
        for i in range(track.GetMCTrackStepCount()):
            step = track.GetMCTrackStep(i)
            endpoint = step.GetEndpoint()
            volume = step.GetVolume()
            momentum = step.GetMomentum()
            process = step.GetProcess()
            if momentum != starting_momentum:
                print("######### NEW STEP #########")
                print('endpoint: ', endpoint[0], endpoint[1], endpoint[2])
                print('momentum: ', momentum[0], momentum[1], momentum[2])
                print('volume: ', volume)
                print('process: ', process)

volume_counts = {}
for i in range(360):
    volume_counts[i - 180] = 0

for iEntry, anEntry in enumerate(fileIterator):
    MC = anEntry.GetMC()
    track = MC.GetMCTrack(0)
    for i in range(track.GetMCTrackStepCount()):
        step = track.GetMCTrackStep(i)
        volume = step.GetVolume()
        volume_string = str(volume)
        if volume_string[:19] == "collecting_surface_":
            volume_num = int(volume_string[19:])
            volume_counts[volume_num] += 1

x = range(5, 180)
y = []
for i in x:
    y.append(volume_counts[i])

print(x)
print(y)

plt.plot(x, y)
plt.show()



