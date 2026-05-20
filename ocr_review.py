#ocr_review.py
import cv2

def manualReview(roi, detectedTexts, confidences):
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
