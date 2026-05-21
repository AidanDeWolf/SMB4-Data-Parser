#DetectPage.py
import cv2
import numpy as np
import SmbScheduleParserTest as s

#Helper
def meanBGR(frame, x, y, w, h):
    roi = frame[y:y+h, x:x+w]
    b, g, r = cv2.mean(roi)[:3]
    return b, g, r


# Roster Detectors
def isRoster(frame):
    x = 1792
    y = 115
    w = 18
    h = 16

    b, g, r = meanBGR(frame, x, y, w, h)
    if b>5 and b<20 and g>1 and g<8 and r>50 and r<120:
        return True
    else:
        return False
def isFranchiseRoster(frame):
    x = 1019
    y = 103
    w = 6
    h = 11    

    b, g, r = meanBGR(frame, x, y, w, h)
    if b < 10 and g < 5 and r < 5:
        return True
    else:
        return False
def isSeasonRoster(frame):
    x = 1019
    y = 103
    w = 6
    h = 11    

    b, g, r = meanBGR(frame, x, y, w, h)
    if b > 10 and g > 5 and r > 5:
        return True
    else:
        return False    
def classifyRosterPage(frame):
    if isSeasonRoster(frame):
        x = 867
        y = 111
        w = 130
        h = 15
    else:
        x = 848
        y = 111
        w = 168
        h = 15
    
    roi = frame[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    profile = gray.mean(axis=0)
    xPeak = np.argmax(profile)

    if xPeak > 0 and xPeak < 20:
        return 1
    elif xPeak > 40 and xPeak < 60:
        return 2
    elif xPeak > 70 and xPeak < 90:
        return 3
    elif xPeak > 110 and xPeak < 130:
        return 4
    else:
        print("Error detecting Roster Page #")
        print("detected xPeak: ", xPeak)
        return 0


# Schedule Detector
def isSchedule(frame):
    x = 191
    y = 172
    w = 1440
    h = 44

    b, g, r = meanBGR(frame, x, y, w, h)
    if b>6 and b<12 and g>5 and g<11 and r>5 and r<11:
        return True
    else:
        return False


# Stats Detectors
def isStats(frame):
    x = 806
    y = 139
    w = 326
    h = 42

    b, g, r = meanBGR(frame, x, y, w, h)
    if b > 117 and b < 128 and g > 81 and g < 91 and r > 74 and r < 84:
        return True
    else:
        return False
def isPitchingStats(frame):
    x = 868
    y = 148
    w = 13
    h = 25
    b, g, r = meanBGR(frame, x, y, w, h)
    if b < 159 and g < 134 and r < 131:
        return True
    else:
        return False
def isBattingStats(frame):
    x = 868
    y = 148
    w = 13
    h = 25
    b, g, r = meanBGR(frame, x, y, w, h)
    if b > 158 and g > 135 and r > 132:
        return True
    else:
        return False





    
