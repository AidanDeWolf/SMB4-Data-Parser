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
testSchedule = False
testSznRosterInfo = False
savePNGs = False


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



videoPathBaseStats = r"C:\GithubRepos\SMB4-Data-Parser\mp4\StatsBaseTestCase.mp4"
videoPathExtremeStats = r"C:\GithubRepos\SMB4-Data-Parser\mp4\StatsExtremeTestCase.mp4"
videoPathRoster = r"C:\GithubRepos\SMB4-Data-Parser\mp4\AttributesTestCaseFranchise.mp4"
videoPathSznRoster = r"C:\GithubRepos\SMB4-Data-Parser\mp4\AttributesTestCaseSeason.mp4"
videoPathBaseSchedule = r"C:\GithubRepos\SMB4-Data-Parser\mp4\ScheduleBaseTestCase.mp4"

testSchedulePg1 = capFrame(videoPathBaseSchedule,0)
testSchedulePg2 = capFrame(videoPathBaseSchedule,12)
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
sznRosPg1 = capFrame(videoPathSznRoster, 8)
sznRosPg2 = capFrame(videoPathSznRoster, 9)
sznRosPg3 = capFrame(videoPathSznRoster, 11)
sznRosPg4 = capFrame(videoPathSznRoster, 13)

#getWindowCoords(testRosPg1)

if savePNGs:
    out_dir = r"C:\GithubRepos\SMB4-Data-Parser\png"

    cv2.imwrite(out_dir + r"\franchiseRos1.png", test2RosPg1)
    cv2.imwrite(out_dir + r"\franchiseRos2.png", test2RosPg2)
    cv2.imwrite(out_dir + r"\franchiseRos3.png", test2RosPg3)
    cv2.imwrite(out_dir + r"\franchiseRos4.png", test2RosPg4)

    cv2.imwrite(out_dir + r"\sznRos1.png", sznRosPg1)
    cv2.imwrite(out_dir + r"\sznRos2.png", sznRosPg2)
    cv2.imwrite(out_dir + r"\sznRos3.png", sznRosPg3)
    cv2.imwrite(out_dir + r"\sznRos4.png", sznRosPg4)

    cv2.imwrite(out_dir + r"\batStats.png", test22Rows)

    cv2.imwrite(out_dir + r"\scheduleFirst.png", testSchedulePg1)
    cv2.imwrite(out_dir + r"\scheduleLast.png", testSchedulePg2)

    cv2.imwrite(out_dir + r"\pitchStats.png", test9Rows)


centerScheduleX = 911
centerScheduleY = 194
xBuffer = 720
yBuffer = 22




if showRosterPages:
    cv2.imshow("Page 1", sznRosPg1)
    cv2.imshow("Page 2", sznRosPg2) 
    cv2.imshow("Page 3", sznRosPg3)
    cv2.imshow("Page 4", sznRosPg4)
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
    pdDF9 = pd.DataFrame(pitcherStatsOCR(test9Rows))
    pdDF9.to_excel("C:\\GithubRepos\\TestData\\test9RowsPitchingStats.xlsx", index=False)


if testRoster1Info:

    pdDFRoster = pd.DataFrame(rosterInfoOCR(testRosPg1, testRosPg2, testRosPg3, testRosPg4))
    pdDFRoster.to_excel("C:\\GithubRepos\\TestData\\testRosterPage.xlsx", index=False)
    print("Roster1 Exported")

if testRoster2Info:

    pdDFRoster = pd.DataFrame(rosterInfoOCR(test2RosPg1, test2RosPg2, test2RosPg3, test2RosPg4))
    pdDFRoster.to_excel("C:\\GithubRepos\\TestData\\test2RosterPage.xlsx", index=False)
    print("Roster2 Exported")

if testSznRosterInfo:
    pdDFRoster = pd.DataFrame(rosterInfoOCR(sznRosPg1, sznRosPg2, sznRosPg3, sznRosPg4, type="season"))
    pdDFRoster.to_excel("C:\\GithubRepos\\TestData\\testSznRosterPage.xlsx", index=False)
    print("SznRoster Exported")


if generateCoords:
    clickedPoint = None

    def clickEvent(event, x, y, flags, param):
        global clickedPoint

        if event == cv2.EVENT_LBUTTONDOWN:
            clickedPoint = (x, y)
            print(f"Clicked coordinates: ({x}, {y})")

    # Example image


    cv2.imshow("Image", sznRosPg4)
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

