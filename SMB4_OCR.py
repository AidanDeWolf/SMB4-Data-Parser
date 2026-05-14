#SMB4_OCR.py
import cv2

nameConfig = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. "
intConfig = "--psm 7 -c tessedit_char_whitelist=0123456789"
teamNameConfig = "--psm 7"
scoreConfig = "--psm 7 -c tessedit_char_whitelist=0123456789"
gameConfig = "--psm 7 -c tessedit_char_whitelist=0123456789#"
traitConfig = "--psm 7 -c tessedit_char_whitelist= -()24AaBbcCdDeEFfgGHhiIJjkKlLmMnNoOpPrRsStTuUVvwWxyZz"
playerRatingConfig = "--psm 7 -c tessedit_char_whitelist=0123456789-"
chemistryConfig = "--psm 7 -c tessedit_char_whitelist=SPICMHDRA"
priPosConfig = "--psm 7 -c tessedit_char_whitelist=123BSFCLRSP/"
secPosConfig = "--psm 7 -c tessedit_char_whitelist=123BSFCLRSPOI/"
handConfig = "--psm 7 -c tessedit_char_whitelist=LRS"
salaryConfig = "--psm 7 -c tessedit_char_whitelist=0123456789$m"

def debugOCRCell(roi, text, confidence, label):
    import pytesseract
    import cv2
    if confidence <90 or text == "":
    
        cv2.imshow(label, roi)
        print(f"{label}: '{text}' confidence = {confidence}")
        cv2.waitKey(0)

def ocrStatCell(frame, yValue, xValue, xBuffer, yBuffer, config, preProcessType=None):
    from PreProcessing import preProcessing
    roi = frame[yValue - yBuffer : yValue + yBuffer, xValue - xBuffer : xValue + xBuffer]
    roi = preProcessing(roi, type=preProcessType)
    output, confidence = ocrIntsWithConfidence(roi, config=config)
    return output, confidence

def ocrNameCell(frame, yValue, xValue, xBuffer, yBuffer, config, preProcessType=None):
    from PreProcessing import preProcessing
    roi = frame[yValue - yBuffer : yValue + yBuffer, xValue - xBuffer : xValue + xBuffer]
    roi = preProcessing(roi, type=preProcessType)
    output, confidence = ocrWordsWithConfidence(roi, config=config)
    return output, confidence



def ocrIntsWithConfidence(roi, config, minConfidence=20):
    import pytesseract
    import cv2
    data = pytesseract.image_to_data(
        roi,
        config=config,
        output_type=pytesseract.Output.DICT
    )
    validTexts = []
    validConfidences = []

    for ocrIndex in range(len(data["text"])):
        currentText = data["text"][ocrIndex].strip()
        if currentText == "":
            continue
        confidence = int(data["conf"][ocrIndex])

        
        validTexts.append(currentText)
        validConfidences.append(confidence)
    reviewNeeded = False

    if len(validTexts) == 0:
        reviewNeeded = True
        combinedText = ""
    elif len(validTexts) > 1:
        reviewNeeded = True
        combinedText = "".join(validTexts)
    else:
        combinedText = validTexts[0]
    
    averageConfidence = (sum(validConfidences) / len(validConfidences) if len(validConfidences) > 0 else -1)
    if averageConfidence < minConfidence:
        reviewNeeded = True
    

    if reviewNeeded:
        combinedText = manualReview(roi, validTexts, validConfidences)        
    return combinedText, averageConfidence

def ocrWordsWithConfidence(roi, config, minConfidence=20):
    import pytesseract

    data = pytesseract.image_to_data(roi, config = config, output_type=pytesseract.Output.DICT)

    texts = []
    confidences = []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if text == "":
            continue
        
        confidence = int(data["conf"][i])
        if confidence < 0:
            continue

        texts.append(text)
        confidences.append(confidence)

    if len(texts) == 0:
        combined = manualReview(roi, texts, confidences)
        return combined, -1
    
    #Combine multi-word outputs (names)
    combinedText = " ".join(texts)
    avgConfidence = sum(confidences) / len(confidences)

    reviewNeeded = (avgConfidence < minConfidence or len(texts) > 3)

    if reviewNeeded:
        combinedText = manualReview(roi, texts, confidences)
    return combinedText, avgConfidence
    
def ocrCell(roi, config, mode="int", minConfidence=20):
    if mode == "int":
        return ocrIntsWithConfidence(roi, config, minConfidence)
    elif mode == "word":
        return ocrWordsWithConfidence(roi, config, minConfidence)

def manualReview(roi, detectedTexts, confidences):
    import cv2
    print("Manual Review Triggered:")
    print(f"Detected OCR tokens: {detectedTexts}")
    print(f"Confidences: {confidences}")
    cv2.imshow("Review Needed", roi)
    cv2.waitKey(1)
    manual = input(f"Enter correct value:").strip()
    cv2.destroyWindow("Review Needed")
    
    if manual != "":
        return manual
    else:
        return "".join(detectedTexts)

def scheduleOCR(frame):
    import pytesseract
    import cv2
    print(f"---Running Schedule OCR---")

    yvalues = [251, 293, 335, 378, 419, 461, 503, 545, 587, 629, 671, 713, 754, 797, 839, 881, 923] #pixel values of the center of the 17 relevant rows
    xvalues = [210, 595, 818, 877, 1097] #pixel values of center of the 5 relevant columns
    teamScore_x_Buffer = 29
    teamName_xBuffer = 115
    gameNumber_xBuffer = 40
    yBuffer = 16

    games = []


    
    for y in yvalues:
        gameNumberROI = frame[
        y - yBuffer : y + yBuffer,
        xvalues[0] - gameNumber_xBuffer : xvalues[0] + gameNumber_xBuffer
        ]

        gameNumber = pytesseract.image_to_string(
            gameNumberROI, config=gameConfig
            ).strip()

        awayTeamROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[1] - teamName_xBuffer : xvalues[1] + teamName_xBuffer
        ]
        awayTeam = pytesseract.image_to_string(
            awayTeamROI, config=teamNameConfig
        ).strip()

        awayScoreROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[2] - teamScore_x_Buffer : xvalues[2] + teamScore_x_Buffer
        ]
        awayScore = pytesseract.image_to_string(
            awayScoreROI, config=scoreConfig
        ).strip().replace("#","")

        homeScoreROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[3] - teamScore_x_Buffer : xvalues[3] + teamScore_x_Buffer
        ]
        homeScore = pytesseract.image_to_string(
            homeScoreROI, config=scoreConfig
        ).strip()

        homeTeamROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[4] - teamName_xBuffer : xvalues[4] + teamName_xBuffer
        ]
        homeTeam = pytesseract.image_to_string(
            homeTeamROI, config=teamNameConfig
        ).strip()

        if awayScore == "":
            print(f"Failed to read away score for row with game number: {gameNumber}")
            cv2.imshow("Failed Away Score", awayScoreROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if homeScore == "":
            print(f"Failed to read home score for row with game number: {gameNumber}")  
            cv2.imshow("Failed Home Score", homeScoreROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if gameNumber == "" or gameNumber == "#":
            print(f"Failed to read game number for row: {y}")
            cv2.imshow("Failed Game Number", gameNumberROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if awayTeam == "":
            cv2.imshow("Failed Away Team", awayTeamROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if homeTeam == "":
            cv2.imshow("Failed Home Team", homeTeamROI)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        games.append({
            "gameNumber": gameNumber,
            "awayTeam": awayTeam,
            "homeTeam": homeTeam,
            "awayScore": awayScore,
            "homeScore": homeScore,
        })  
    return games

def batterStatsOCR(frame):
    import pytesseract
    import cv2
    from DetectRowCount import detectRowCount
    from PreProcessing import preProcessing

    print(f"---Running Batting Stats OCR---")
    battingStats = []


    yvalues = [317, 350, 382, 414, 446, 478, 511, 543, 575, 606, 638, 670, 702, 734, 766, 799, 831, 863, 895, 927, 959, 991] #pixel values of the center of the 22 relevant rows
    xValues = {"name": 164, "games": 390, "atBats": 461, "hits": 531, "homeRuns": 601, "rbi": 672, "runs": 1028, "totalBases": 1100, "doubles": 1171, "triples": 1241, "walks": 1312, "battingK": 1382, "sb": 1453, "cs": 1523, "hbp": 1594, "sac": 1664, "sf": 1734, "errors": 1804}
    xBuffers = {"name": 116, "games": 32, "atBats": 35, "hits": 35, "homeRuns": 35, "rbi": 35, "runs": 35, "totalBases": 35, "doubles": 35, "triples": 32, "walks": 35, "battingK": 35, "sb": 35, "cs": 35, "hbp": 35, "sac": 35, "sf": 35, "errors": 35}
    yBuffer = 19
    rowCount = detectRowCount(frame)

    for yvalue in yvalues[:rowCount]:
    
        name, nameConfidence = ocrNameCell(frame, yvalue, xValues["name"], xBuffers["name"], yBuffer, nameConfig, preProcessType="name")
        games, gamesConfidence = ocrStatCell(frame, yvalue, xValues["games"], xBuffers["games"], yBuffer, gameConfig, preProcessType="number")
        atBats, atBatsConfidence = ocrStatCell(frame, yvalue, xValues["atBats"], xBuffers["atBats"], yBuffer, intConfig, preProcessType="number")
        hits, hitsConfidence = ocrStatCell(frame, yvalue, xValues["hits"], xBuffers["hits"], yBuffer, intConfig, preProcessType="number")
        homeRuns, homeRunsConfidence = ocrStatCell(frame, yvalue, xValues["homeRuns"], xBuffers["homeRuns"], yBuffer, intConfig, preProcessType="number")
        rbi, rbiConfidence = ocrStatCell(frame, yvalue, xValues["rbi"], xBuffers["rbi"], yBuffer, intConfig, preProcessType="number")
        runs, runsConfidence = ocrStatCell(frame, yvalue, xValues["runs"], xBuffers["runs"], yBuffer, intConfig, preProcessType="number")
        totalBases, totalBasesConfidence = ocrStatCell(frame, yvalue, xValues["totalBases"], xBuffers["totalBases"], yBuffer, intConfig, preProcessType="number")
        doubles, doublesConfidence = ocrStatCell(frame, yvalue, xValues["doubles"], xBuffers["doubles"], yBuffer, intConfig, preProcessType="number")
        triples, triplesConfidence = ocrStatCell(frame, yvalue, xValues["triples"], xBuffers["triples"], yBuffer, intConfig, preProcessType="number")
        walks, walksConfidence = ocrStatCell(frame, yvalue, xValues["walks"], xBuffers["walks"], yBuffer, intConfig, preProcessType="number")
        battingK, battingKConfidence = ocrStatCell(frame, yvalue, xValues["battingK"], xBuffers["battingK"], yBuffer, intConfig, preProcessType="number")
        sb, sbConfidence = ocrStatCell(frame, yvalue, xValues["sb"], xBuffers["sb"], yBuffer, intConfig, preProcessType="number")
        cs, csConfidence = ocrStatCell(frame, yvalue, xValues["cs"], xBuffers["cs"], yBuffer, intConfig, preProcessType="number")
        hbp, hbpConfidence = ocrStatCell(frame, yvalue, xValues["hbp"], xBuffers["hbp"], yBuffer, intConfig, preProcessType="number")
        sac, sacConfidence = ocrStatCell(frame, yvalue, xValues["sac"], xBuffers["sac"], yBuffer, intConfig, preProcessType="number")
        sf, sfConfidence = ocrStatCell(frame, yvalue, xValues["sf"], xBuffers["sf"], yBuffer, intConfig, preProcessType="number")
        errors, errorsConfidence = ocrStatCell(frame, yvalue, xValues["errors"], xBuffers["errors"], yBuffer, intConfig, preProcessType="number")
        
        

        battingStats.append({
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
            "errors": errors
        })
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return battingStats

def pitcherStatsOCR(frame):
    import pytesseract
    print(f"---Running OCR---")
    pitchingStats = []
    return pitchingStats

def attFirstOCR(frame):
    import pytesseract
    print(f"---Running OCR---")
    playersAtt1 = []
    return playersAtt1

def attSecondOCR(frame):
    import pytesseract
    print(f"---Running OCR---")
    playersAtt2 = []
    return playersAtt2

def attThirdOCR(frame):
    import pytesseract
    print(f"---Running OCR---")
    playersAtt3 = []
    return playersAtt3

def attFourthOCR(frame):
    import pytesseract
    print(f"---Running OCR---")
    playersAtt4 = []
    return playersAtt4

