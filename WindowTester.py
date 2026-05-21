import cv2
import numpy as np
import SmbScheduleParserTest as s
from ClassifyPage import isRoster, isFranchiseRoster, isSeasonRoster, classifyRosterPage, isSchedule, isStats, isPitchingStats, isBattingStats


printMeanValues = False
testRosterClassification = True
# Schedule ROI
x = 191
y = 172
w = 1440
h = 44

# Roster ROI
x = 1792
y = 115
w = 18
h = 16

# Stats ROI
x = 806
y = 139
w = 326
h = 42

# Stats Minute ROI
x = 868
y = 148
w = 13
h = 25

# Franchise or Season ROI
x = 1019
y = 103
w = 6
h = 11

# Season ROI
x = 867
y = 111
w = 130
y = 15

# Franchise ROI
x = 848
y = 111
w = 168
y = 15

frames = [
    s.testSchedulePg1,
    s.testSchedulePg2,
    s.test9Rows,
    s.test22Rows,
    s.testRosPg1,
    s.testRosPg2,
    s.testRosPg3,
    s.testRosPg4,
    s.sznRosPg1,
    s.sznRosPg2,
    s.sznRosPg3,
    s.sznRosPg4
]

frame_names = [
    "Sched1",
    "Sched2",
    "PitchStats",
    "BatStats",
    "FranchRos1",
    "FranchRos2",
    "FranchRos3",
    "FranchRos4",
    "SznRos1",
    "SznRos2",
    "SznRos3",
    "SznRos4"
]
if printMeanValues:
    for name, frame in zip(frame_names, frames):
        roi = frame[y:y+h, x:x+w]
        avg_color = cv2.mean(roi)[:3]  # BGR
        print(name, avg_color)



if testRosterClassification:
    print("Checking whether it is a Roster Page")
    for frame in frames:
        print(isRoster(frame))

    print("Checking whether it is a Schedule Page")
    for frame in frames:
        print(isSchedule(frame))

    print("Checking whether it is a Stats Page")
    for frame in frames:
        print(isStats(frame))



    print("Checking pitching stats")
    for frame in frames:
        if isStats(frame):
            print(isPitchingStats(frame))

    print("Checking batting stats")
    for frame in frames:
        if isStats(frame):
            print(isBattingStats(frame))

    print("Checking Franchise Roster")
    for frame in frames:
        if isRoster(frame):
            print(isFranchiseRoster(frame))

    print("Checking Season Roster")
    for frame in frames:
        if isRoster(frame):
            print(isSeasonRoster(frame))

    print("Classifying Roster Pages")
    for frame in frames:
        if isRoster(frame):
            print(classifyRosterPage(frame))