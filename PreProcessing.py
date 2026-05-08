def preProcessing(img, type=None):
    import cv2  #OpenCV library for image processing
    
    
    #Upscale
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #Convert to Grayscale
    grayscaleIMG = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Light Denoising
    grayscaleIMG = cv2.GaussianBlur(grayscaleIMG, (3,3),0)
    if type == "number":
        processed = cv2.threshold(grayscaleIMG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return processed
    
    return grayscaleIMG