import cv2
import numpy as np

def detectRowCount(frame):
    frame = frame[299:299+715, 1838:1838+48]
    blue = frame[:,:,0]

    # cv2.imshow("Blue", blue)
    # cv2.waitKey(0)
    rowSignal = np.mean(blue, axis=1)
    rowSignal = cv2.GaussianBlur(rowSignal.reshape(-1,1), (1,15),0).flatten()

    gradient = np.abs(np.diff(rowSignal))

    threshhold = np.mean(gradient) + 0.2 *np.std(gradient)
    rowEdges = np.where(gradient > threshhold)[0]
   
    clusters = []
    current = []

    for y in rowEdges:
        if not current or y - current[-1] < 8:
            current.append(y)
        else:
            clusters.append(current)
            current = [y]
    if current: clusters.append(current)

    return (len(clusters)-1)