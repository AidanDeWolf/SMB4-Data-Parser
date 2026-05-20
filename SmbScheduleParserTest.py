from statistics import mode
import cv2
import pytesseract
import numpy as np
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

import os
print("CWD:", os.getcwd())
print("Script Started")

testDetectRows = False
testBattingStats = False
testPitchingStats = False
showRosterPages = False
testRoster1Info = False
testRoster2Info = False
generateCoords = False
testSchedule = True

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


def getWindowCoords(frame):
    window = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    print("Window coordinates:", window)
    cv2.imshow("Selected Window", frame[int(window[1]):int(window[1]+window[3]), int(window[0]):int(window[0]+window[2])])
    

from PreProcessing import preProcessing
from SMB4_OCR import batterStatsOCR, pitcherStatsOCR, scheduleOCR, rosterInfoOCR
from DetectRowCount import detectRowCount



videoPathBaseStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsBaseTestCase.mp4"
videoPathExtremeStats = r"C:\GithubRepos\SMB4-Data-Parser\StatsExtremeTestCase.mp4"
videoPathRoster = r"C:\GithubRepos\SMB4-Data-Parser\AttributesTestCaseFranchise.mp4"
videoPathBaseSchedule = r"C:\GithubRepos\SMB4-Data-Parser\ScheduleBaseTestCase.mp4"
test9Rows = capFrame(videoPathBaseStats, 3)
test14Rows = capFrame(videoPathBaseStats, 6)
test20Rows = capFrame(videoPathBaseStats)
test21Rows = capFrame(videoPathBaseStats, 11)
test22Rows = capFrame(videoPathBaseStats, 28)
testExtremeStats = capFrame(videoPathExtremeStats, 31)
testRosPg1 = capFrame(videoPathRoster, 0)
testRosPg2 = capFrame(videoPathRoster,1)
testRosPg3 = capFrame(videoPathRoster,3)
testRosPg4 = capFrame(videoPathRoster,4)
test2RosPg1 = capFrame(videoPathRoster, 8)
test2RosPg2 = capFrame(videoPathRoster, 10)
test2RosPg3 = capFrame(videoPathRoster, 12)
test2RosPg4 = capFrame(videoPathRoster, 14)



if showRosterPages:
    cv2.imshow("Page 1", test2RosPg1)
    cv2.imshow("Page 2", test2RosPg2) 
    cv2.imshow("Page 3", test2RosPg3)
    cv2.imshow("Page 4", test2RosPg4)
    cv2.waitKey(0)
    cv2.destroyAllWindows   


if testDetectRows:
    print("Number of rows detected in 9 row case:", detectRowCount(test9Rows))
    print("Number of rows detected in 14 row case:", detectRowCount(test14Rows))
    print("Number of rows detected in 20 row case:", detectRowCount(test20Rows))
    print("Number of rows detected in 21 row case:", detectRowCount(test21Rows))
    print("Number of rows detected in 22 row case:", detectRowCount(test22Rows))
    print("Number of rows detected in extreme stats case:", detectRowCount(testExtremeStats))


if testBattingStats:
    import pandas as pd
    #pdDF20 = pd.DataFrame(batterStatsOCR(test20Rows))
    #pdDF21 = pd.DataFrame(batterStatsOCR(test21Rows))
    pdDF22 = pd.DataFrame(batterStatsOCR(test22Rows))
    pdDF22.to_excel("C:\\GithubRepos\\TestData\\test22RowsBattingStats.xlsx", index=False)
if testPitchingStats:
    import pandas as pd
    pdDF9 = pd.DataFrame(pitcherStatsOCR(test9Rows))
    pdDF9.to_excel("C:\\GithubRepos\\TestData\\test9RowsPitchingStats.xlsx", index=False)
    print("9 Row Case Pitching Stats:", pdDF9)


if testRoster1Info:
    import pandas as pd
    pdDFRoster = pd.DataFrame(rosterInfoOCR(testRosPg1, testRosPg2, testRosPg3, testRosPg4))
    pdDFRoster.to_excel("C:\\GithubRepos\\TestData\\testRosterPage.xlsx", index=False)
    print("Roster1 Exported")

if testRoster2Info:

    pdDFRoster = pd.DataFrame(rosterInfoOCR(test2RosPg1, test2RosPg2, test2RosPg3, test2RosPg4))
    pdDFRoster.to_excel("C:\\GithubRepos\\TestData\\test2RosterPage.xlsx", index=False)
    print("Roster2 Exported")


if generateCoords:
    clickedPoint = None

    def clickEvent(event, x, y, flags, param):
        global clickedPoint

        if event == cv2.EVENT_LBUTTONDOWN:
            clickedPoint = (x, y)
            print(f"Clicked coordinates: ({x}, {y})")

    # Example image


    cv2.imshow("Image", testRosPg4)
    cv2.setMouseCallback("Image", clickEvent)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(clickedPoint)
 


if testSchedule:
    frameBase = capFrame(videoPathBaseSchedule)
    pdDFSchedule =  pd.DataFrame(scheduleOCR(frameBase))
    print(pdDFSchedule)


cv2.waitKey(0)
cv2.destroyAllWindows()
print("Script Finished")




""" battingStats.append({
            "name": name,
            "games": games,
            "atBats": atBats,
            "hits": hits,
            "homeRuns": homeRuns,
            "rbi": rbi,
            "runs": runs,
            "totalBases": totalBases,
            "doubles": doubles,
            "triples": triples,
            "walks": walks,
            "strikeouts": battingK,
            "stolenBases": sb,
            "caughtStealing": cs,
            "hitByPitch": hbp,
            "sacrificeHits": sac,
            "sacrificeFlies": sf,
            "errors": errors,
            "passedBalls": ""
        })
        battingStats = batStatsCheck(battingStats) """
