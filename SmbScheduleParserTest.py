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
from SMB4_OCR import batterStatsOCR, pitcherStatsOCR, scheduleOCR
from DetectRowCount import detectRowCount



videoPathBaseStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsBaseTestCase.mp4"
videoPathExtremeStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsExtremeTestCase.mp4"
videoPathRoster = r"C:\GithubRepos\SMB4-Data-Parser\AttributesTestCaseSeason.mp4"
test9Rows = capFrame(videoPathBaseStats, 3)
test14Rows = capFrame(videoPathBaseStats, 6)
test20Rows = capFrame(videoPathBaseStats)
test21Rows = capFrame(videoPathBaseStats, 11)
test22Rows = capFrame(videoPathBaseStats, 28)
testExtremeStats = capFrame(videoPathExtremeStats, 31)
testRosPg1 = capFrame(videoPathRoster, 0, 0, "frame")
testRosPg2 = capFrame(videoPathRoster,1)
testRosPg3 = capFrame(videoPathRoster,2)
testRosPg4 = capFrame(videoPathRoster,3)
showRosterPages = True
if showRosterPages:
    cv2.imshow("Page 1", testRosPg1)
    cv2.imshow("Page 2", testRosPg2) 
    cv2.imshow("Page 3", testRosPg3)
    cv2.imshow("Page 4", testRosPg4)
    cv2.waitKey(0)
    cv2.destroyAllWindows   

testDetectRows = False
if testDetectRows:
    print("Number of rows detected in 9 row case:", detectRowCount(test9Rows))
    print("Number of rows detected in 14 row case:", detectRowCount(test14Rows))
    print("Number of rows detected in 20 row case:", detectRowCount(test20Rows))
    print("Number of rows detected in 21 row case:", detectRowCount(test21Rows))
    print("Number of rows detected in 22 row case:", detectRowCount(test22Rows))
    print("Number of rows detected in extreme stats case:", detectRowCount(testExtremeStats))

testBattingStats = False
testPitchingStats = False
if testBattingStats:
    import pandas as pd
    pdDF20 = pd.DataFrame(batterStatsOCR(test20Rows))
    pdDF21 = pd.DataFrame(batterStatsOCR(test21Rows))
    pdDF22 = pd.DataFrame(batterStatsOCR(test22Rows))
if testPitchingStats:
    import pandas as pd
    pdDF9 = pd.DataFrame(pitcherStatsOCR(test9Rows))
    pdDF9.to_excel("C:\\GithubRepos\\TestData\\test9RowsPitchingStats.xlsx", index=False)
    print("9 Row Case Pitching Stats:", pdDF9)



generateCoords = False
if generateCoords:
    clickedPoint = None

    def clickEvent(event, x, y, flags, param):
        global clickedPoint

        if event == cv2.EVENT_LBUTTONDOWN:
            clickedPoint = (x, y)
            print(f"Clicked coordinates: ({x}, {y})")

    # Example image


    cv2.imshow("Image", test9Rows)
    cv2.setMouseCallback("Image", clickEvent)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(clickedPoint)


# getWindowCoords(test20Rows)   

# videoPathBase = "SMB4_Schedule_Test.mp4"
# videoPathExtreme = "ScheduleExtremeTestCase.mp4"
# frameBase = capFirstFrame(videoPathBase)
# frameExtreme = capFirstFrame(videoPathExtreme)

# scheduleOCR(frameBase)


cv2.waitKey(0)
cv2.destroyAllWindows()