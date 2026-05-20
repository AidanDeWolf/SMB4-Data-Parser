#ocr_parsers.py
from ocr_core import extractOCRdata, combineTextOCR, averageConfidence
from SMB4_OCR import manualReview


def ocrNumbersWithConfidence(roi, config, minConfidence=1):

    validTexts, validConfidences = extractOCRdata(roi, config)

    if len(validTexts) == 0: #or max(validConfidences) <15:
        validTexts, validConfidences = retryOCR(roi, ocr_configs.intRetryConfig, validTexts, validConfidences)
        
    combinedText = combineTextOCR(validTexts)
    
    avgConfidence = averageConfidence(validConfidences)
    reviewNeeded = (len(validTexts) == 0 or averageConfidence < minConfidence)
    

    if reviewNeeded:
        combinedText = manualReview(roi, validTexts, validConfidences)    
    return combinedText, averageConfidence

def ocrWordsWithConfidence(roi, config, minConfidence=20):
    texts, confidences = extractOCRdata(roi, config)

    if len(texts) == 0:
        combined = manualReview(roi, texts, confidences)
        return combined, -1
    
    #Combine multi-word outputs (names)
    combinedText = " ".join(texts)
    
    avgConfidence = averageConfidence(confidences)

    if combinedText == "CC" and (config == ocr_configs.priPosConfig or config == ocr_configs.secPosConfig):
        return "C", avgConfidence

    reviewNeeded = (avgConfidence < minConfidence or len(texts) > 3)

    if reviewNeeded:
        combinedText = manualReview(roi, texts, confidences)
    return combinedText, avgConfidence
    
def ocrHandednessWithConfidence(roi, config, minConfidence=20):
    
    VALID = {"R", "L", "S"}
    texts, confidences = extractOCRdata(roi, config)

    if len(texts) == 0:
           combined = manualReview(roi, texts, confidences)
           return combined, -1
    
    raw = "".join(texts).upper()
    filtered = [character for character in raw if character in VALID]
    
    if len(filtered) == 0:
        combined = manualReview(roi, texts, confidences)
        return combined, -1
    from collections import Counter
    best = Counter(filtered).most_common(1)[0][0]
    avgConfidence = averageConfidence(confidences)

    return best, avgConfidence

def ocrTraitsWithConfidence(roi, config, minConfidence = 20):
    texts, confidences = extractOCRdata(roi, config)
    if len(texts)== 0:
        return "", 100
    
    combinedText = " ".join(texts).strip()

    # Count alphabetic characters only
    lettersOnly = re.sub(r"[^A-Za-z]", "", combinedText)

    # Treat tiny garbage outputs like "ee", "SS", "ll" as blank
    if len(lettersOnly) < 4:
        return "", 100

    avgConfidence = sum(confidences) / len(confidences)

    reviewNeeded = (
        avgConfidence < minConfidence
        or len(texts) > 4
    )

    if reviewNeeded:
        combinedText = manualReview(roi, texts, confidences)

    return combinedText, avgConfidence

def ocrSalaryWithConfidence(roi, config, minConfidence = 20):
    texts, confidences = extractOCRdata(roi, config)

    if len(texts) ==0:
        return 0, 100
    
    combinedText = "".join(texts).lower().strip()
    match = re.search(r"\d+(\.\d+)?", combinedText)

    avgConfidence = averageConfidence(confidences)

    if not match:
        return 0, avgConfidence
    
    try:
        value = float(match.group(0))
    except:
        return 0, 0
    
    

    reviewNeeded = (avgConfidence < minConfidence or value>35)
    if reviewNeeded:
        print("ONLY ENTER NUMBER, OMIT '$' and 'm'")
        value = manualReview(roi, texts, confidences)

    return value, avgConfidence

def ocrRatingWithConfidence(roi, config, minConfidence = 20):
    texts, confidences = extractOCRdata(roi, config)
    combinedText = combineTextOCR(texts)
    if not combinedText == "":
        value = int(combinedText)
    else:
        value = -1
    
    avgConfidence = averageConfidence(confidences)

    if (value>9) and (avgConfidence>-1):
        return value, avgConfidence
    elif (avgConfidence>80):
        return value, avgConfidence
    else:
        texts, confidences = retryOCR(roi, ocr_configs.attRetryConfig, texts, confidences)
        text = combineTextOCR(texts)
        avgConfidence = averageConfidence(confidences)
        if not text == "":
            value = int(text)
        else:
            value = -1

    reviewNeeded=False
    if (value<0) or (value>99) or avgConfidence<minConfidence:
        reviewNeeded=True
    if (value<9) and (avgConfidence<20):
        reviewNeeded=True

    if reviewNeeded:
        value = int(manualReview(roi, texts, confidences))

    return value, avgConfidence
