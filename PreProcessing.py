def preProcessing(img, type=None):
    import cv2  #OpenCV library for image processing
    import numpy as np

    if type == "rating":
        roi = cv2.resize(img, None, fx=2.5, fy=2, interpolation = cv2.INTER_CUBIC)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        white_mask = (v>170) & (s<110)
        

        filtered = v.copy()
        filtered[~white_mask] = 0
    
        output = cv2.bitwise_not(filtered)
        return output

    if type == "hand":
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)
        img = cv2.convertScaleAbs(img, alpha=1.4, beta=-10)
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi = cv2.threshold(gray, 185, 255, cv2.THRESH_BINARY)[1]
        return roi 

    #Upscale
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #Convert to Grayscale
    grayscaleIMG = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #Invert if White
    whiteRatio = (grayscaleIMG > 200).mean()
    if whiteRatio>0.6:
        grayscaleIMG=cv2.bitwise_not(grayscaleIMG)

    
    #Light Denoising
    if type != "number":
        grayscaleIMG = cv2.GaussianBlur(grayscaleIMG, (3,3),0)
    
    if type == "number":
        processed = cv2.threshold(grayscaleIMG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return processed
    
    return grayscaleIMG