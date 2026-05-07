def preProcessing(img):
    import cv2  #OpenCV library for image processing
    #Upscale
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #Convert to Grayscale
    grayscaleIMG = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return grayscaleIMG