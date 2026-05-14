from statistics import mode
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

import os
print("CWD:", os.getcwd())
print("Script Started")



def capFrame(videoPath, timestampSecs = 0):
    cap = cv2.VideoCapture(videoPath)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestampSecs * 1000)  # Set the position to the desired frame (in milliseconds)
    successRead, frame = cap.read()
    if not successRead:
        print(f"Failed to read video: {videoPath}")
        return None
    return frame

# Needs to be worked on
def videoCapture(videoPath):
    cap = cv2.VideoCapture(videoPath)
    return cap






# This won't work because xvalues is not defined but can use this again if needed by defining xvalues and yvalues in this file or passing them as parameters, just a reference for now
def debugRow(frame, y, xvalues, buffers):
    yb = buffers["yBuffer"]

    crops = {
        "game": frame[y-yb:y+yb, xvalues[0]-buffers["game"]:xvalues[0]+buffers["game"]],
        "awayTeam": frame[y-yb:y+yb, xvalues[1]-buffers["team"]:xvalues[1]+buffers["team"]],
        "awayScore": frame[y-yb:y+yb, xvalues[2]-buffers["score"]:xvalues[2]+buffers["score"]],
        "homeScore": frame[y-yb:y+yb, xvalues[3]-buffers["score"]:xvalues[3]+buffers["score"]],
        "homeTeam": frame[y-yb:y+yb, xvalues[4]-buffers["team"]:xvalues[4]+buffers["team"]],
    }

    for name, img in crops.items():
        cv2.imshow(name, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



def getWindowCoords(frame):
    window = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    print("Window coordinates:", window)
    cv2.imshow("Selected Window", frame[int(window[1]):int(window[1]+window[3]), int(window[0]):int(window[0]+window[2])])
    

from PreProcessing import preProcessing
from SMB4_OCR import batterStatsOCR, scheduleOCR
from DetectRowCount import detectRowCount



videoPathBaseStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsBaseTestCase.mp4"
videoPathExtremeStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsExtremeTestCase.mp4"
test9Rows = capFrame(videoPathBaseStats, 3)
test14Rows = capFrame(videoPathBaseStats, 6)
test20Rows = capFrame(videoPathBaseStats)
test21Rows = capFrame(videoPathBaseStats, 11)
test22Rows = capFrame(videoPathBaseStats, 28)
testExtremeStats = capFrame(videoPathExtremeStats, 31)
#getWindowCoords(test21Rows)

print("Number of rows detected in 9 row case:", detectRowCount(test9Rows))
print("Number of rows detected in 14 row case:", detectRowCount(test14Rows))
print("Number of rows detected in 20 row case:", detectRowCount(test20Rows))
print("Number of rows detected in 21 row case:", detectRowCount(test21Rows))
print("Number of rows detected in 22 row case:", detectRowCount(test22Rows))
print("Number of rows detected in extreme stats case:", detectRowCount(testExtremeStats))


import pandas as pd
pdDF = pd.DataFrame(batterStatsOCR(test20Rows))
print(pdDF)
# pdDF.to_excel("ocr_output.xlsx", index=False)



# getWindowCoords(test20Rows)   

# videoPathBase = "SMB4_Schedule_Test.mp4"
# videoPathExtreme = "ScheduleExtremeTestCase.mp4"
# frameBase = capFirstFrame(videoPathBase)
# frameExtreme = capFirstFrame(videoPathExtreme)

# scheduleOCR(frameBase)


cv2.waitKey(0)
cv2.destroyAllWindows()