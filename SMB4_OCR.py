#SMB4_OCR.py
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

    nameConfig = "--psm 7"
    scoreConfig = "--psm 7 -c tessedit_char_whitelist=0123456789"
    gameConfig = "--psm 7 -c tessedit_char_whitelist=0123456789#"
    
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
            awayTeamROI, config=nameConfig
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
            homeTeamROI, config=nameConfig
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
    xvalues = [164, 390, 461, 531, 601, 672, 1028, 1100, 1171, 1241, 1312, 1382, 1453, 1523, 1594, 1664, 1734, 1804] #pixel values of center of the 18 relevant columns
    name_x_Buffer = 116
    games_xBuffer = 32
    atBat_xBuffer = 35
    hits_xBuffer = 35
    hr_xBuffer = 35
    rbi_xBuffer = 35
    runs_xBuffer = 35
    totalBases_xBuffer = 35
    doubles_xBuffer = 35
    triples_xBuffer = 32
    walks_xBuffer = 35
    battingK_xBuffer = 35
    sb_xBuffer = 35
    cs_xBuffer = 35
    hbp_xBuffer = 35
    sac_xBuffer = 35
    sf_xBuffer = 35
    error_xBuffer = 35
    yBuffer = 16


    nameConfig = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. " #Added period and space to whitelist for cases like "J. Doe" or "J Doe"
    intConfig = "--psm 7 -c tessedit_char_whitelist=0123456789"
    rowCount = detectRowCount(frame)

    # debugFrame = frame.copy()
    # for yvalue in yvalues[:rowCount]:
    #     #Debug
    #     cv2.rectangle(debugFrame,
    #           (xvalues[0] - name_x_Buffer, yvalue - yBuffer),
    #           (xvalues[0] + name_x_Buffer, yvalue + yBuffer),
    #           (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[1] - games_xBuffer, yvalue - yBuffer),
    #                 (xvalues[1] + games_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[2] - atBat_xBuffer, yvalue - yBuffer),
    #                 (xvalues[2] + atBat_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[3] - hits_xBuffer, yvalue - yBuffer),
    #                 (xvalues[3] + hits_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[4] - hr_xBuffer, yvalue - yBuffer),
    #                 (xvalues[4] + hr_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[5] - rbi_xBuffer, yvalue - yBuffer),
    #                 (xvalues[5] + rbi_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[6] - runs_xBuffer, yvalue - yBuffer),
    #                 (xvalues[6] + runs_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[7] - totalBases_xBuffer, yvalue - yBuffer),
    #                 (xvalues[7] + totalBases_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[8] - doubles_xBuffer, yvalue - yBuffer),
    #                 (xvalues[8] + doubles_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[9] - triples_xBuffer, yvalue - yBuffer),
    #                 (xvalues[9] + triples_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[10] - walks_xBuffer, yvalue - yBuffer),
    #                 (xvalues[10] + walks_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[11] - battingK_xBuffer, yvalue - yBuffer),
    #                 (xvalues[11] + battingK_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[12] - sb_xBuffer, yvalue - yBuffer),
    #                 (xvalues[12] + sb_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[13] - cs_xBuffer, yvalue - yBuffer),
    #                 (xvalues[13] + cs_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[14] - hbp_xBuffer, yvalue - yBuffer),
    #                 (xvalues[14] + hbp_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[15] - sac_xBuffer, yvalue - yBuffer),
    #                 (xvalues[15] + sac_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[16] - sf_xBuffer, yvalue - yBuffer),
    #                 (xvalues[16] + sf_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)

    #     cv2.rectangle(debugFrame,
    #                 (xvalues[17] - error_xBuffer, yvalue - yBuffer),
    #                 (xvalues[17] + error_xBuffer, yvalue + yBuffer),
    #                 (0, 255, 0), 1)
    # cv2.imshow("Debug Frame", debugFrame)


    for yvalue in yvalues[:rowCount]:
    
        nameROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[0] - name_x_Buffer : xvalues[0] + name_x_Buffer
        ]
        nameROI = preProcessing(nameROI)
        name = pytesseract.image_to_string(
            nameROI,
            config=nameConfig
        ).strip()

        gamesROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[1] - games_xBuffer : xvalues[1] + games_xBuffer
        ]
        gamesROI = preProcessing(gamesROI, type="number")
        games = pytesseract.image_to_string(
            gamesROI,
            config=intConfig
        ).strip()

        atBatROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[2] - atBat_xBuffer : xvalues[2] + atBat_xBuffer
        ]
        atBatROI = preProcessing(atBatROI, type="number")
        atBats = pytesseract.image_to_string(
            atBatROI,
            config=intConfig
        ).strip()

        hitsROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[3] - hits_xBuffer : xvalues[3] + hits_xBuffer
        ]
        hitsROI = preProcessing(hitsROI, type="number")
        hits = pytesseract.image_to_string(
            hitsROI,
            config=intConfig
        ).strip()

        hrROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[4] - hr_xBuffer : xvalues[4] + hr_xBuffer
        ]
        hrROI = preProcessing(hrROI, type="number")
        homeRuns = pytesseract.image_to_string(
            hrROI,
            config=intConfig
        ).strip()

        rbiROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[5] - rbi_xBuffer : xvalues[5] + rbi_xBuffer
        ]
        rbiROI = preProcessing(rbiROI, type="number")
        rbi = pytesseract.image_to_string(
            rbiROI,
            config=intConfig
        ).strip()

        runsROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[6] - runs_xBuffer : xvalues[6] + runs_xBuffer
        ]
        runsROI = preProcessing(runsROI, type="number")
        runs = pytesseract.image_to_string(
            runsROI,
            config=intConfig
        ).strip()

        totalBasesROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[7] - totalBases_xBuffer : xvalues[7] + totalBases_xBuffer
        ]
        totalBasesROI = preProcessing(totalBasesROI, type="number")
        totalBases = pytesseract.image_to_string(
            totalBasesROI,
            config=intConfig
        ).strip()

        doublesROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[8] - doubles_xBuffer : xvalues[8] + doubles_xBuffer
        ]
        doublesROI = preProcessing(doublesROI, type="number")
        doubles = pytesseract.image_to_string(
            doublesROI,
            config=intConfig
        ).strip()

        triplesROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[9] - triples_xBuffer : xvalues[9] + triples_xBuffer
        ]
        triplesROI = preProcessing(triplesROI, type="number")
        triples = pytesseract.image_to_string(
            triplesROI,
            config=intConfig
        ).strip()

        walksROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[10] - walks_xBuffer : xvalues[10] + walks_xBuffer
        ]
        walksROI = preProcessing(walksROI, type="number")
        walks = pytesseract.image_to_string(
            walksROI,
            config=intConfig
        ).strip()

        battingKROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[11] - battingK_xBuffer : xvalues[11] + battingK_xBuffer
        ]
        battingKROI = preProcessing(battingKROI, type="number")
        battingK = pytesseract.image_to_string(
            battingKROI,
            config=intConfig
        ).strip()

        sbROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[12] - sb_xBuffer : xvalues[12] + sb_xBuffer
        ]
        sbROI = preProcessing(sbROI, type="number")
        sb = pytesseract.image_to_string(
            sbROI,
            config=intConfig
        ).strip()

        csROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[13] - cs_xBuffer : xvalues[13] + cs_xBuffer
        ]
        csROI = preProcessing(csROI, type="number")
        cs = pytesseract.image_to_string(
            csROI,
            config=intConfig
        ).strip()

        hbpROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[14] - hbp_xBuffer : xvalues[14] + hbp_xBuffer
        ]
        hbpROI = preProcessing(hbpROI, type="number")
        hbp = pytesseract.image_to_string(
            hbpROI,
            config=intConfig
        ).strip()

        sacROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[15] - sac_xBuffer : xvalues[15] + sac_xBuffer
        ]
        sacROI = preProcessing(sacROI, type="number")
        sac = pytesseract.image_to_string(
            sacROI,
            config=intConfig
        ).strip()

        sfROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[16] - sf_xBuffer : xvalues[16] + sf_xBuffer
        ]
        sfROI = preProcessing(sfROI, type="number")
        sf = pytesseract.image_to_string(
            sfROI,
            config=intConfig
        ).strip()

        errorROI = frame[
            yvalue - yBuffer : yvalue + yBuffer,
            xvalues[17] - error_xBuffer : xvalues[17] + error_xBuffer
        ]
        errorROI = preProcessing(errorROI, type="number")
        errors = pytesseract.image_to_string(
            errorROI,
            config=intConfig
        ).strip()

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