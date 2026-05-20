#ocr_core.py
def extractOCRdata(roi, config):
    """
    Performs OCR on an image
    Args:
        roi: the image to be processed
        config: the configuration for tesseract to use
    Returns:
        texts: detected text
        confidences: confidences for each text
    """

    data = pytesseract.image_to_data(
            roi,
            config=config,
            output_type=pytesseract.Output.DICT
        )
    
    texts = []
    confidences = []
    
    for ocrIndex in range(len(data["text"])):
            currentText = data["text"][ocrIndex].strip()
            if currentText == "":
                continue
            confidence = int(data["conf"][ocrIndex])
            texts.append(currentText)
            confidences.append(confidence)
    return texts, confidences

def retryOCR(roi, config, validTexts, validConfidences):
        """
        Retries OCR using alternative preprocessing strategies and returns the highest scoring result

        Args:
            roi: the image to be processed
            config: the configuration for tesseract to use on the retry
            validTexts: the original OCR output
            validConfidences: confidence for the original OCR output
        Returns:
            tuple[list[str], list[int]]: The highest scoring OCR text results and their associated confidence value
        """
    
        roi2 = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        roi2 = cv2.convertScaleAbs(roi2, alpha=1.6, beta=15)


        roi3 = cv2.resize(roi, None, fx=4, fy=2, interpolation=cv2.INTER_CUBIC)
        roi3 = cv2.convertScaleAbs(roi3, alpha = 1.6, beta = 15)

        extraXscaled = cv2.resize(roi, None, fx=6, fy=2, interpolation=cv2.INTER_CUBIC)
        extraXscaled = cv2.convertScaleAbs(roi, alpha = 1.6, beta = 15)

        roi4 = cv2.copyMakeBorder(roi2, top=5, bottom=5, left = 5, right=5, borderType=cv2.BORDER_CONSTANT, value =255)
        roiInv = cv2.bitwise_not(roi2)
        original = (validTexts, validConfidences)
        second = extractOCRdata(roi2, config)
        inverted = extractOCRdata(roiInv, config)
        xscaled = extractOCRdata(roi3, config)
        bordered = extractOCRdata(roi4, config)
        psm72 = extractOCRdata(roi2, ocr_configs.playerRatingConfig)
        extraXscaled = extractOCRdata(extraXscaled, ocr_configs.playerRatingConfig)

        candidates = [original, second, inverted, xscaled, bordered, psm72, extraXscaled]
        
        def score(texts, confidences):
            if len(texts) == 0:
                return -1111
            avgConf = sum(confidences) / len(confidences)
            fragmentationPenalty = (-0.5) * (len(texts) - 1)
            return (avgConf - fragmentationPenalty)
        
        validTexts, validConfidences = max(candidates, key=lambda x: score(x[0], x[1]))
        return validTexts, validConfidences
        
def combineTextOCR(validTexts):
    if len(validTexts) == 0:
        combinedText = ""
        avgConfidence = -1
    elif len(validTexts) > 1:
        combinedText = "".join(validTexts)
    else:
        combinedText = validTexts[0]
    return combinedText

def averageConfidence(confidences):    
    if not confidences:
        return -1
    return sum(confidences) / len(confidences)