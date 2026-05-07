import cv2 #?

import os #?



videoPath = "SMB4_Schedule_Test.mp4"
screenCap = cv2.VideoCapture(videoPath)
successfulFrameRead, frame = screenCap.read()

if not successfulFrameRead:
    print("Failed to read video or empty file.")
else:
    print("First frame captured successfully!")
    cv2.imwrite("first_frame.png", frame)
screenCap.release()
print(frame.shape)
print(frame.dtype)
