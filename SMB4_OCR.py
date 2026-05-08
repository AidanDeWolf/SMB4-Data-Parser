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
    print(f"---Running Batting Stats OCR---")
    battingStats = []


    yvalues = [317, 350, 383, 416, 449, 482, 515, 548, 581, 614, 647, 680, 713, 746, 779, 812, 845, 878, 911, 944, 977, 1010] #pixel values of the center of the 22 relevant rows
    xvalues = [163,391,461,531,601,671,1030,1100,1170,1240,1310,1380,1450,1520,1590,1660,1730,1800] #pixel values of center of the 18 relevant columns
    name_x_Buffer = 115
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


    nameConfig = "--psm 7"
    intConfig = "--psm 7 -c tessedit_char_whitelist=0123456789"
    rowCount = detectRowCount(frame)
    for yvalue in range(rowCount):
        False

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