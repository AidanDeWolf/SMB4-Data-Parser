#DetectRoiType
def detectROItypeSMB4Schedule(roi):
    
    h, w = roi.shape[:2]
    print("DEBUG SHAPE:", w, h)
    if w == 400 and h == 1440:
        return "teamNames"
    elif w == 110 and h == 1440:
        return "intScores"
    elif w == 240 and h == 1440:
        return "gameNumber"
    else:
        return False
