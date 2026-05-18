#SMB4_OCR.py
import cv2
import pytesseract
import ocr_configs

def extractOCRdata(roi, config):
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

def ocrCell(frame, yValue, xValue, xBuffer, yBuffer, config, preProcessType=None, type="numbers"):
    from PreProcessing import preProcessing
    roi = frame[yValue - yBuffer : yValue + yBuffer, xValue - xBuffer : xValue + xBuffer]
    roi = preProcessing(roi, type=preProcessType)
    if type == "words":
        output, confidence = ocrWordsWithConfidence(roi, config=config)
    elif type == "numbers":
        output, confidence = ocrNumbersWithConfidence(roi, config=config)
    
    elif type == "pos":
        thresholded = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)[1]
        darkPixels = cv2.countNonZero(thresholded)
        """ print("Dark Pixels: ", darkPixels)
        h, w = thresholded.shape[:]
        totalPixels = h*w
        print("Total Pixels: ", totalPixels)
        cv2.imshow("ROI", thresholded)
        cv2.waitKey(0)  """

        if darkPixels >10150:
            output, confidence = "", 100
        else:
            output, confidence = ocrWordsWithConfidence(roi, config = config)

    elif type == "hand":
        roi = cv2.convertScaleAbs(roi, alpha=2.0, beta=0)
        output, confidence = ocrHandednessWithConfidence(roi, config=config)

    elif type == "trait":
        output, confidence = ocrTraitsWithConfidence(roi, config=config)

    elif type == "salary":
        output, confidence = ocrSalaryWithConfidence(roi, config=config)

    elif type == "rating":
        output, confidence = ocrNumbersWithConfidence(roi, config=config)
    else:
        output, confidence = 0, 0
    return output, confidence

def ocrNumbersWithConfidence(roi, config, minConfidence=1):

    validTexts, validConfidences = extractOCRdata(roi, config)

    if len(validTexts) == 0: #or max(validConfidences) <15:
        roi2 = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        roi2 = cv2.convertScaleAbs(roi2, alpha=1.6, beta=15)
        roiInv = cv2.bitwise_not(roi2)
        original = (validTexts, validConfidences)
        second = extractOCRdata(roi2, ocr_configs.intRetryConfig)
        inverted = extractOCRdata(roiInv, ocr_configs.intRetryConfig)
        candidates = [original, second, inverted]
        
        def score(texts, confidences):
            if len(texts) == 0:
                return -1111
            avgConf = sum(confidences) / len(confidences)
            fragmentationPenalty = (-0.5) * (len(texts) - 1)
            return (avgConf - fragmentationPenalty)
        
        validTexts, validConfidences = max(candidates, key=lambda x: score(x[0], x[1]))

    if len(validTexts) == 0:
        combinedText = ""
        averageConfidence = -1
    elif len(validTexts) > 1:
        combinedText = "".join(validTexts)
    else:
        combinedText = validTexts[0]
    
    averageConfidence = (sum(validConfidences) / len(validConfidences) if len(validConfidences) > 0 else -1)
    reviewNeeded = (len(validTexts) == 0 or averageConfidence < minConfidence)
    

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

    if combinedText == "CC" and (config == ocr_configs.priPosConfig or config == ocr_configs.secPosConfig):
        return "C", avgConfidence

    reviewNeeded = (avgConfidence < minConfidence or len(texts) > 3)

    if reviewNeeded:
        combinedText = manualReview(roi, texts, confidences)
    return combinedText, avgConfidence
    
def ocrHandednessWithConfidence(roi, config, minConfidence=20):
    import pytesseract
    data = pytesseract.image_to_data(roi, config=config, output_type = pytesseract.Output.DICT)
    VALID = {"R", "L", "S"}
    texts =[]
    confidences=[]
    data = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)

    for i in range(len(data["text"])):
        text = data ["text"][i].strip()

        if text == "":
            continue
        confidence = int(data["conf"][i])
        if confidence<0:
            continue
        texts.append(text.upper())
        confidences.append(confidence)

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
    avgConfidence = sum(confidences)/len(confidences)

    return best, avgConfidence

def ocrTraitsWithConfidence(roi, config, minConfidence = 20):
    import pytesseract
    import re
    data = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)
    texts = []
    confidences = []
    for i in range(len(data["text"])):
        text = data["text"][i].strip()

        if text == "":
            continue
        confidence = int(data["conf"][i])

        if confidence <0:
            continue
        texts.append(text)
        confidences.append(confidence) 
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
    import pytesseract
    import re
    data = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)
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

    if len(texts) ==0:
        return 0, 100
    
    combinedText = "".join(texts).lower().strip()
    match = re.search(r"\d+(\.\d+)?", combinedText)

    if not match:
        return 0, sum(confidences) / len(confidences)
    
    try:
        value = float(match.group(0))
    except:
        return 0, 0
    
    avgConfidence = sum(confidences) / len(confidences)

    reviewNeeded = (avgConfidence < minConfidence or value>35)
    if reviewNeeded:
        print("ONLY ENTER NUMBER, OMIT '$' and 'm'")
        value = manualReview(roi, texts, confidences)

    return value, avgConfidence

def ocrRatingWithConfidence(roi, config, minConfidence = 20):
    import pytesseract
    import numpy as np

    data = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)
    texts = []
    confidences = []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()

        if text == "":
            continue

        conf = int(data["conf"][i])
        if conf<0:
            continue
        
        texts.append(text)
        confidences.append(conf)
    
    if len(texts) == 0:
        return 0,0
    
    combinedText = "".join(texts)
    value = int(combinedText)

    
    avgConfidence = sum(confidences) / len(confidences)



    

    if (value>9) and (avgConfidence>-1):
        return value, avgConfidence

    
    
    reviewNeeded = (value<0 or value>99 or avgConfidence<minConfidence)
    
    if (value<9) and (avgConfidence<50):
        reviewNeeded=True

    if reviewNeeded:
        value = int(manualReview(roi, texts, confidences))

    return value, avgConfidence

def manualReview(roi, detectedTexts, confidences):
    import cv2
    print(f"Detected: {detectedTexts}")
    print(f"Confidence: {confidences}")
    cv2.imshow("Review Needed", roi)
    cv2.waitKey(1)
    manual = input(f"Enter correct value:").strip()
    cv2.destroyWindow("Review Needed")
    
    if manual != "":
        return manual
    else:
        return "".join(detectedTexts)

def batStatsCheck(playerStats):
    hits = playerStats["hits"]
    atBats = playerStats["atBats"]
    homeRuns = playerStats["homeRuns"]
    doubles = playerStats["doubles"]
    triples = playerStats["triples"]
    totalBases = playerStats["totalBases"]
    rbi = playerStats["rbi"]
    runs = playerStats["runs"]
    strikeouts = playerStats["strikeouts"]
    batStatsNeedReview = False
    
    if (
    hits > atBats
    or homeRuns > hits
    or doubles > hits
    or triples > hits
    or doubles + triples + homeRuns > hits
    or totalBases < hits
    or totalBases < (
        (hits - doubles - triples - homeRuns)
        + (2 * doubles)
        + (3 * triples)
        + (4 * homeRuns)
    )
    or rbi < homeRuns
    or runs < homeRuns
    or strikeouts > atBats
):
        batStatsNeedReview = True
    playerStats["batStatsNeedReview"]=batStatsNeedReview
    return playerStats

def pitchStatsCheck(playerStats):

    wins = playerStats["wins"]
    losses = playerStats["losses"]
    runsAllowed = playerStats["runsAllowed"]
    earnedRunsAllowed = playerStats["earnedRunsAllowed"]
    gamesPitched = playerStats["gamesPitched"]
    gamesStarted = playerStats["gamesStarted"]
    saves = playerStats["saves"]
    inningsPitched = playerStats["inningsPitched"]
    hitsAllowed = playerStats["hitsAllowed"]
    pitchingKs = playerStats["pitchingKs"]
    walksAllowed = playerStats["walksAllowed"]
    wildPitches = playerStats["wildPitches"]
    homeRunsAllowed = playerStats["homeRunsAllowed"]
    completeGames = playerStats["completeGames"]
    shutouts = playerStats["shutouts"]
    hitBatsmen = playerStats["hitBatsmen"]
    battersFaced = playerStats["battersFaced"]
    pitchesThrown = playerStats["pitchesThrown"]

    pitchStatsNeedReview = False

    if (
        earnedRunsAllowed > runsAllowed
        or gamesStarted > gamesPitched
        or saves > gamesPitched
        or completeGames > gamesStarted
        or shutouts > completeGames
        or homeRunsAllowed > hitsAllowed
        or inningsPitched < 0
        or wins > gamesPitched
        or losses > gamesPitched
        or wins + losses > gamesPitched
        or pitchingKs > battersFaced
        or walksAllowed > battersFaced
        or hitsAllowed > battersFaced
        or hitBatsmen > battersFaced
        or pitchesThrown < battersFaced
        or wildPitches > pitchesThrown
        or inningsPitched > (gamesPitched * 9)
        or pitchingKs > (inningsPitched * 3) # greater than 3? technically possible
        or battersFaced < (hitsAllowed + walksAllowed + pitchingKs + hitBatsmen)
    ):
        pitchStatsNeedReview = True

    playerStats["pitchStatsNeedReview"]=pitchStatsNeedReview
    return playerStats

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
            gameNumberROI, config=ocr_configs.gameConfig
            ).strip()

        awayTeamROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[1] - teamName_xBuffer : xvalues[1] + teamName_xBuffer
        ]
        awayTeam = pytesseract.image_to_string(
            awayTeamROI, config=ocr_configs.teamNameConfig
        ).strip()

        awayScoreROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[2] - teamScore_x_Buffer : xvalues[2] + teamScore_x_Buffer
        ]
        awayScore = pytesseract.image_to_string(
            awayScoreROI, config=ocr_configs.scoreConfig
        ).strip().replace("#","")

        homeScoreROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[3] - teamScore_x_Buffer : xvalues[3] + teamScore_x_Buffer
        ]
        homeScore = pytesseract.image_to_string(
            homeScoreROI, config=ocr_configs.scoreConfig
        ).strip()

        homeTeamROI = frame[
            y - yBuffer : y + yBuffer,
            xvalues[4] - teamName_xBuffer : xvalues[4] + teamName_xBuffer
        ]
        homeTeam = pytesseract.image_to_string(
            homeTeamROI, config=ocr_configs.teamNameConfig
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
    from DetectRowCount import detectRowCount

    print(f"---Running Batting Stats OCR---")
    battingStats = []


    yvalues = [318, 350, 382, 414, 446, 478, 511, 543, 575, 606, 638, 670, 702, 734, 766, 799, 831, 863, 895, 927, 959, 991] #pixel values of the center of the 22 relevant rows
    xValues = {"name": 164, "games": 390, "atBats": 461, "hits": 531, "homeRuns": 601, "rbi": 672, "runs": 1028, "totalBases": 1100, "doubles": 1171, "triples": 1241, "walks": 1312, "battingK": 1382, "sb": 1453, "cs": 1523, "hbp": 1594, "sac": 1664, "sf": 1734, "errors": 1804}
    xBuffers = {"name": 116, "games": 36, "atBats": 36, "hits": 36, "homeRuns": 36, "rbi": 36, "runs": 36, "totalBases": 36, "doubles": 36, "triples": 36, "walks": 36, "battingK": 36, "sb": 36, "cs": 36, "hbp": 36, "sac": 36, "sf": 36, "errors": 36}
    yBuffer = 20
    rowCount = detectRowCount(frame)

    for yvalue in yvalues[:rowCount]:
    
        name, nameConfidence = ocrCell(frame, yvalue, xValues["name"], xBuffers["name"], yBuffer, ocr_configs.nameConfig, preProcessType="name", type="words")
        games, gamesConfidence = ocrCell(frame, yvalue, xValues["games"], xBuffers["games"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        atBats, atBatsConfidence = ocrCell(frame, yvalue, xValues["atBats"], xBuffers["atBats"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        hits, hitsConfidence = ocrCell(frame, yvalue, xValues["hits"], xBuffers["hits"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        homeRuns, homeRunsConfidence = ocrCell(frame, yvalue, xValues["homeRuns"], xBuffers["homeRuns"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        rbi, rbiConfidence = ocrCell(frame, yvalue, xValues["rbi"], xBuffers["rbi"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        runs, runsConfidence = ocrCell(frame, yvalue, xValues["runs"], xBuffers["runs"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        totalBases, totalBasesConfidence = ocrCell(frame, yvalue, xValues["totalBases"], xBuffers["totalBases"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        doubles, doublesConfidence = ocrCell(frame, yvalue, xValues["doubles"], xBuffers["doubles"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        triples, triplesConfidence = ocrCell(frame, yvalue, xValues["triples"], xBuffers["triples"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        walks, walksConfidence = ocrCell(frame, yvalue, xValues["walks"], xBuffers["walks"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        battingK, battingKConfidence = ocrCell(frame, yvalue, xValues["battingK"], xBuffers["battingK"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        sb, sbConfidence = ocrCell(frame, yvalue, xValues["sb"], xBuffers["sb"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        cs, csConfidence = ocrCell(frame, yvalue, xValues["cs"], xBuffers["cs"], yBuffer, ocr_configs.ntConfig, preProcessType="number")
        hbp, hbpConfidence = ocrCell(frame, yvalue, xValues["hbp"], xBuffers["hbp"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        sac, sacConfidence = ocrCell(frame, yvalue, xValues["sac"], xBuffers["sac"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        sf, sfConfidence = ocrCell(frame, yvalue, xValues["sf"], xBuffers["sf"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        errors, errorsConfidence = ocrCell(frame, yvalue, xValues["errors"], xBuffers["errors"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        
        games = int(games)
        atBats = int(atBats)
        hits = int(hits)
        homeRuns = int(homeRuns)
        rbi = int(rbi)
        runs = int(runs)
        totalBases = int(totalBases)
        doubles = int(doubles)
        triples = int(triples)
        walks = int(walks)
        battingK = int(battingK)
        sb = int(sb)
        cs = int(cs)
        hbp = int(hbp)
        sac = int(sac)
        sf = int(sf)
        errors = int(errors)
        
        currentHitter = {"name": name,
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
            "errors": errors,
            "passedBalls": ""}
        

        
        currentHitter = batStatsCheck(currentHitter)
        battingStats.append(currentHitter)
        
    return battingStats

def pitcherStatsOCR(frame):
    from DetectRowCount import detectRowCount
    print(f"---Running Pitching Stats OCR---")
    pitchingStats = []

    yvalues = [318, 350, 382, 414, 446, 478, 511, 543, 575, 606, 638, 670, 702, 734, 766, 799, 831, 863, 895, 927, 959, 991] #pixel values of the center of the 22 relevant rows
    xValues = {"name":  164, "wins": 387, "losses": 459, "runsAllowed": 602, "earnedRunsAllowed": 675, "gamesPitched": 813, "gamesStarted": 887, "saves": 957, "inningsPitched": 1026, "hitsAllowed": 1099, "pitchingKs": 1240, "walksAllowed": 1311, "wildPitches": 1383,"homeRunsAllowed": 1453, "completeGames": 1525, "shutouts": 1595, "hitBatsmen": 1666, "battersFaced": 1737, "pitchesThrown": 1809}
    xBuffers = {"name": 116, "wins": 36, "losses": 36, "runsAllowed": 36, "earnedRunsAllowed": 36, "gamesPitched": 36, "gamesStarted": 36, "saves": 36, "inningsPitched": 40, "hitsAllowed": 36, "pitchingKs": 36, "walksAllowed": 36, "wildPitches": 36, "homeRunsAllowed": 36, "completeGames": 36, "shutouts": 36, "hitBatsmen": 36, "battersFaced":38, "pitchesThrown":42}
    yBuffer = 20
    rowCount = detectRowCount(frame)

    for yvalue in yvalues[:rowCount]:
        name, nameConfidence = ocrCell(frame, yvalue, xValues["name"], xBuffers["name"], yBuffer, ocr_configs.nameConfig, preProcessType="name", type="words")
        wins, winsConfidence = ocrCell(frame, yvalue, xValues["wins"], xBuffers["wins"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        losses, lossesConfidence = ocrCell(frame, yvalue, xValues["losses"], xBuffers["losses"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        runsAllowed, runsAllowedConfidence = ocrCell(frame, yvalue, xValues["runsAllowed"], xBuffers["runsAllowed"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        earnedRunsAllowed, earnedRunsAllowedConfidence = ocrCell(frame, yvalue, xValues["earnedRunsAllowed"], xBuffers["earnedRunsAllowed"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        gamesPitched, gamesPitchedConfidence = ocrCell(frame, yvalue, xValues["gamesPitched"], xBuffers["gamesPitched"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        gamesStarted, gamesStartedConfidence = ocrCell(frame, yvalue, xValues["gamesStarted"], xBuffers["gamesStarted"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        saves, savesConfidence = ocrCell(frame, yvalue, xValues["saves"], xBuffers["saves"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        inningsPitched, inningsPitchedConfidence = ocrCell(frame, yvalue, xValues["inningsPitched"], xBuffers["inningsPitched"], yBuffer, ocr_configs.inningsConfig, preProcessType="number")
        hitsAllowed, hitsAllowedConfidence = ocrCell(frame, yvalue, xValues["hitsAllowed"], xBuffers["hitsAllowed"], yBuffer, ocr_configs.intConfig, preProcessType="number")
        pitchingKs, pitchingKsConfidence = ocrCell(frame,yvalue,xValues["pitchingKs"],xBuffers["pitchingKs"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        walksAllowed ,walksAllowedConfidence= ocrCell(frame,yvalue,xValues["walksAllowed"],xBuffers["walksAllowed"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        wildPitches ,wildPitchesConfidence= ocrCell(frame,yvalue,xValues["wildPitches"],xBuffers["wildPitches"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        homeRunsAllowed, homeRunsAllowedConfidence = ocrCell(frame,yvalue,xValues["homeRunsAllowed"],xBuffers["homeRunsAllowed"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        completeGames ,completeGamesConfidence= ocrCell(frame,yvalue,xValues["completeGames"],xBuffers["completeGames"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        shutouts ,shutoutsConfidence= ocrCell(frame,yvalue,xValues["shutouts"],xBuffers["shutouts"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        hitBatsmen ,hitBatsmenConfidence= ocrCell(frame,yvalue,xValues["hitBatsmen"],xBuffers["hitBatsmen"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        battersFaced ,battersFacedConfidence= ocrCell(frame,yvalue,xValues["battersFaced"],xBuffers["battersFaced"],yBuffer,ocr_configs.intConfig ,preProcessType="number")
        pitchesThrown ,pitchesThrownConfidence= ocrCell(frame,yvalue,xValues["pitchesThrown"],xBuffers["pitchesThrown"],yBuffer,ocr_configs.intConfig ,preProcessType="number")

        wins = int(wins)
        losses = int(losses)
        runsAllowed = int(runsAllowed)
        earnedRunsAllowed = int(earnedRunsAllowed)
        gamesPitched = int(gamesPitched)
        gamesStarted = int(gamesStarted)
        saves = int(saves)
        inningsPitched = float(inningsPitched)
        hitsAllowed = int(hitsAllowed)
        pitchingKs = int(pitchingKs)
        walksAllowed = int(walksAllowed)
        wildPitches = int(wildPitches)
        homeRunsAllowed = int(homeRunsAllowed)
        completeGames = int(completeGames)
        shutouts = int(shutouts)
        hitBatsmen = int(hitBatsmen)
        battersFaced = int(battersFaced)
        pitchesThrown = int(pitchesThrown)

        currentPitcher ={
            "name": name,
            "wins": wins,
            "losses": losses,
            "runsAllowed": runsAllowed,
            "earnedRunsAllowed": earnedRunsAllowed,
            "gamesPitched": gamesPitched,
            "gamesStarted": gamesStarted,
            "saves": saves,
            "inningsPitched": inningsPitched,
            "hitsAllowed": hitsAllowed,
            "pitchingKs": pitchingKs,
            "walksAllowed": walksAllowed,
            "wildPitches": wildPitches,
            "homeRunsAllowed": homeRunsAllowed,
            "completeGames": completeGames,
            "shutouts": shutouts,
            "hitBatsmen": hitBatsmen,
            "battersFaced": battersFaced,
            "pitchesThrown": pitchesThrown,
        }
        currentPitcher = pitchStatsCheck(currentPitcher)
        pitchingStats.append(currentPitcher)


    return pitchingStats

def rosterInfoOCR(pg1, pg2, pg3, pg4):
    playerInfo = []
    yValues = [
    199, 235, 269, 304, 343, 378, 417, 452, 486, 522,
    559, 595, 632, 667, 701, 739, 775, 811, 846, 882,
    917, 953
    ]
    xValues1 ={
        "name": 605, "age": 1185, "primary": 962, "secondary": 1074,
        "bats": 1298, "throws": 1413,"salary": 438
        }
    xValues2 ={"power": 961,"contact": 1073,"speed": 1184,"fielding": 1298,"arm": 1409}
    xValues3 ={"velocity": 961, "junk": 1072, "accuracy": 1185}
    xValues4 ={"trait1": 1122, "trait2": 1345, "chemType": 961}
    yBuffer = 19
    yBufferHand=21
    yBufferRating=21
    xBufferName = 116
    xBufferTrait = 70
    xBufferHand = 20
    xBufferSalary = 40
    xBuffer = 34
    xBufferChemType = 19

    for yValue in yValues:
        name, nameConfidence = ocrCell(pg1, yValue, xValues1["name"], xBufferName, yBuffer, ocr_configs.nameConfig, preProcessType="name", type="words")
        age, ageConfidence = ocrCell(pg1, yValue, xValues1["age"], xBuffer, yBuffer, ocr_configs.intConfig, preProcessType="number")

        primary, primaryConfidence = ocrCell(pg1, yValue, xValues1["primary"], xBuffer, yBuffer, ocr_configs.priPosConfig, preProcessType="pos", type="pos")

        isPitcher = primary in ("SP", "RP", "CP", "SP/RP")

        if isPitcher:
            secondary = ""; secondaryConfidence=100
        else:
            secondary, secondaryConfidence = ocrCell(pg1, yValue, xValues1["secondary"], xBuffer, yBuffer, ocr_configs.secPosConfig, preProcessType="pos", type="pos")

        bats, batsConfidence = ocrCell(pg1, yValue, xValues1["bats"], xBufferHand, yBufferHand, ocr_configs.handConfig, preProcessType="hand", type="hand")
        throws, throwsConfidence = ocrCell(pg1, yValue, xValues1["throws"], xBufferHand, yBufferHand, ocr_configs.handConfig, preProcessType="hand", type="hand")
        salary, salaryConfidence = ocrCell(pg1, yValue, xValues1["salary"], xBufferSalary, yBuffer, ocr_configs.salaryConfig, preProcessType="salary", type="salary")

        power, powerConfidence = ocrCell(pg2, yValue, xValues2["power"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")
        contact, contactConfidence = ocrCell(pg2, yValue, xValues2["contact"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")
        speed, speedConfidence = ocrCell(pg2, yValue, xValues2["speed"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")
        fielding, fieldingConfidence = ocrCell(pg2, yValue, xValues2["fielding"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")

        if isPitcher:
           arm = "-"; armConfidence = 100
        else:
            arm, armConfidence = ocrCell(pg2, yValue, xValues2["arm"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")

        if not isPitcher:
            velocity = "-"; velocityConfidence=100
            junk = "-"; junkConfidence=100
            accuracy = "-"; accuracyConfidence=100
        else:
            velocity, velocityConfidence = ocrCell(pg3, yValue, xValues3["velocity"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")
            junk, junkConfidence = ocrCell(pg3, yValue, xValues3["junk"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")
            accuracy, accuracyConfidence = ocrCell(pg3, yValue, xValues3["accuracy"], xBuffer, yBufferRating, ocr_configs.playerRatingConfig, preProcessType="rating", type="rating")

        trait1, trait1Confidence = ocrCell(pg4, yValue, xValues4["trait1"], xBufferTrait, yBuffer, ocr_configs.traitConfig, preProcessType="trait", type="trait")
        trait2, trait2Confidence = ocrCell(pg4, yValue, xValues4["trait2"], xBufferTrait, yBuffer, ocr_configs.traitConfig, preProcessType="trait", type="trait")
        chemType, chemTypeConfidence = ocrCell(pg4, yValue, xValues4["chemType"], xBufferChemType, yBuffer, ocr_configs.chemistryConfig, preProcessType="trait", type="words")

        playerInfo.append({ "name": name, "age": age, "primary": primary, "secondary": secondary, 
                           "bats": bats, "throws": throws, "salary": salary, 
                           "power": power, "contact": contact, "speed": speed, 
                           "fielding": fielding, "arm": arm, 
                           "velocity": velocity, "junk": junk, "accuracy": accuracy, 
                           "chemType": chemType, "trait1": trait1, "trait2": trait2 })
    return playerInfo
