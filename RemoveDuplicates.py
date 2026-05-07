def removeDuplicateGames(rows):
    seenGames = set()
    uniqueGames = []
    for row in rows:
        gameNumber = row[0]
        if gameNumber not in seenGames:
            seenGames.add(gameNumber)
            uniqueGames.append(row)
    return uniqueGames