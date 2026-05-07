from statistics import mode

import cv2 #?
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"






def capFirstFrame(videoPath):
    cap = cv2.VideoCapture(videoPath)
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



def originalROIcode(frame):
    frame = False   #Ignore, just so This can be closed
    # Original hardcoded ROIs, not used in final code but kept for reference
    # x1, y1, w1, h1 = 500, 225, 200, 720
    # awayTeamROI = frame[y1:y1+h1, x1:x1+w1]

    # x2, y2, w2, h2 = 995, 225, 200 , 720
    # homeTeamROI = frame[y2:y2+h2, x2:x2+w2]

    # x3, y3, w3, h3 = 795, 225, 55, 720
    # awayScoreROI = frame[y3:y3+h3, x3:x3+w3]

    # x4, y4, w4, h4 = 845, 225, 55, 720
    # homeScoreROI = frame[y4:y4+h4, x4:x4+w4]

    # x5, y5, w5, h5 = 155, 225, 120, 720
    # gameNumberROI = frame[y5:y5+h5, x5:x5+w5]
    exit()

def getWindowCoords(frame):
    window = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    print("Window coordinates:", window)

from PreProcessing import preProcessing
from SMB4_OCR import scheduleOCR
    




videoPathBase = "SMB4_Schedule_Test.mp4"
videoPathExtreme = "ScheduleExtremeTestCase.mp4"
frameBase = capFirstFrame(videoPathBase)
frameExtreme = capFirstFrame(videoPathExtreme)

scheduleOCR(frame)


cv2.waitKey(0)
cv2.destroyAllWindows()
screenCap.release()