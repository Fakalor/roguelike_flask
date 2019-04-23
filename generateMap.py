import random
from character import Hero, Monster
from heroMonsterList import makeMonster

def initializeMap (size=20):
    ''' Funkcja inicjalizuje mape wypełnioną losową zawartością '''
    gameMap = [[0] * size for i in range(size)]
    randNumber = 45

    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if random.randint(1,101) < randNumber:
                gameMap[i][j] = 1

    return gameMap

def countAliveNeighbours(gameMap, x, y, size=20):
    ''' zliczanie sasiadow (The Game Of Life, John Conway) '''
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighboursX = x + i
            neighboursY = y + j
            if i == 0 and j == 0:
                nicSieNieDzieje = 'x'
            elif neighboursX < 0 or neighboursY < 0 or neighboursX >= size-1 or neighboursY >= size-1:
                count += 1
            elif gameMap[neighboursX][neighboursY]:
                count += 1

    return count

def doSimulation(oldGameMap, size=20):
    ''' kolejne kroki symulacji (The Game Of Life, John Conway)'''
    newGameMap = [[0] * size for i in range(size)]
    deathLimit = 3
    birthLimit = 3

    for i in range(1, size-1):
        for j in range(1, size-1):
            numberSteps = countAliveNeighbours(oldGameMap, i, j, size)
            if oldGameMap[i][j] > 0:
                if numberSteps < deathLimit:
                    newGameMap[i][j] = 0
                else:
                    newGameMap[i][j] = 1
            else:
                if numberSteps > birthLimit:
                    newGameMap[i][j] = 1
                else:
                    newGameMap[i][j] = 0

    return newGameMap

def checkMapIntegrity(gameMap, size):
    ''' sprawdzanie spojnosci mapy i przepisuje tylko najwiekszy spojny fragment'''
    trueFalseMap = [[0] * size for i in range(size)]
    numberOfFields = {}

    ''' przechodzimy mape dla kazdej czesci skladowej mapy '''
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            amount = 0
            if gameMap[i][j] == 1 and trueFalseMap[i][j] == 0:
                amount = dfs(i, j, gameMap, trueFalseMap, amount)
                numberOfFields[i, j] = amount

    ''' sprawdzamy czy ktoras spojna czesc mapy jest wystarczajaco duza '''
    print(gameMap == trueFalseMap)
    trueFalseMap = [[0] * size for i in range(size)]
    for el in numberOfFields:
        if numberOfFields[el] > int((size**2)/2):
            x, y = el
            dfs(x, y, gameMap, trueFalseMap, amount)
            return trueFalseMap

    return False

def dfs(x, y, gameMap, trueFalseMap, amount):
    ''' przejscie mapy dfs'sem '''
    trueFalseMap[x][y] = 1
    if gameMap[x+1][y] == 1 and trueFalseMap[x+1][y] == 0:
        amount = dfs(x+1, y, gameMap, trueFalseMap, amount+1)
    if gameMap[x-1][y] == 1 and trueFalseMap[x-1][y] == 0:
        amount = dfs(x-1, y, gameMap, trueFalseMap, amount+1)
    if gameMap[x][y+1] == 1 and trueFalseMap[x][y+1] == 0:
        amount = dfs(x, y+1, gameMap, trueFalseMap, amount+1)
    if gameMap[x][y-1] == 1 and trueFalseMap[x][y-1] == 0:
        amount = dfs(x, y-1, gameMap, trueFalseMap, amount+1)

    return amount

def findPathBfs(startX, startY, gameMap, goalX, goalY, size):
    ''' znajdywanie najkrótrszej drogi bfs'em'''
    lenPathMap = [[0] * size for i in range(size)]
    trueFalseMap = [[0] * size for i in range(size)]
    transparentField = [1, 5, 81, 82, 83, 91, 92, 93, 41, 44]

    queue = []
    queue.append((startX, startY))
    lenPathMap[startX][startY] = 1
    trueFalseMap[startX][startX] = 0

    while len(queue) > 0:
        node = queue.pop(0)

        ''' sprawdzanie czy dotarlo sie do celu '''
        if node[0] == goalX and node[1] == goalY:
            #print(lenPathMap[node[0]][node[1]])
            return lenPathMap[node[0]][node[1]]

        if gameMap[node[0]+1][node[1]] in transparentField and trueFalseMap[node[0]+1][node[1]] == 0:
            queue.append((node[0]+1, node[1]))
            trueFalseMap[node[0]+1][node[1]] = 1
            lenPathMap[node[0]+1][node[1]] = lenPathMap[node[0]][node[1]] + 1

        if gameMap[node[0]-1][node[1]] in transparentField and trueFalseMap[node[0]-1][node[1]] == 0:
            queue.append((node[0]-1, node[1]))
            trueFalseMap[node[0]-1][node[1]] = 1
            lenPathMap[node[0]-1][node[1]] = lenPathMap[node[0]][node[1]] + 1

        if gameMap[node[0]][node[1]+1] in transparentField and trueFalseMap[node[0]][node[1]+1] == 0:
            queue.append((node[0], node[1]+1))
            trueFalseMap[node[0]][node[1]+1] = 1
            lenPathMap[node[0]][node[1]+1] = lenPathMap[node[0]][node[1]] + 1

        if gameMap[node[0]][node[1]-1] in transparentField and trueFalseMap[node[0]][node[1]-1] == 0:
            queue.append((node[0], node[1]-1))
            trueFalseMap[node[0]][node[1]-1] = 1
            lenPathMap[node[0]][node[1]-1] = lenPathMap[node[0]][node[1]] + 1

    return 0 # jakby cos sie popsulo xD

def lastRender(gameMap, size):
    ''' losowanie wygladu pol i potworow'''
    monsterList = []
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if gameMap[i][j] == 1:
                gameMap[i][j] = random.randint(11, 18)
            if gameMap[i][j] == 5:
                typeMonster = random.randint(1, 100)
                if typeMonster == range(1, 31):
                    gameMap[i][j] = random.randint(51, 53)
                else:
                    gameMap[i][j] = random.randint(54, 59)
                tempMonster = Monster()
                makeMonster(tempMonster, gameMap[i][j], i, j)
                monsterList.append(tempMonster)

    return monsterList

def exitLocation(gameMap, size, professionPlayerOne, professionPlayerTwo):
    ''' losowanie pozycji wyjscia i wyznaczanie pozaycji graczy '''
    while True: # pozycja wyjscia
        exitX, exitY = random.randint(1, size - 1), random.randint(1, size - 1)
        if gameMap[exitX][exitY] == 1:
            gameMap[exitX][exitY] = 2
            break

    while True: # pozycja 1 gracza
        playerOneX, playerOneY = random.randint(1, size - 1), random.randint(1, size - 1)
        if gameMap[playerOneX][playerOneY] == 1:
            path = findPathBfs(exitX, exitY, gameMap, playerOneX, playerOneY, size)
            if path > size-5:
                gameMap[playerOneX][playerOneY] = professionPlayerOne
                break

    while True: # pozycja 2 gracza
        playerTwoX, playerTwoY = random.randint(1, size - 1), random.randint(1, size - 1)
        if gameMap[playerTwoX][playerTwoY] == 1:
            path = findPathBfs(exitX, exitY, gameMap, playerTwoX, playerTwoY, size)
            if path > size-5:
                path = findPathBfs(playerOneX, playerOneY, gameMap, playerTwoX, playerTwoY, size)
                if path > size-5:
                    gameMap[playerTwoX][playerTwoY] = professionPlayerTwo
                    break

    positionPlayerOne = playerOneX, playerOneY
    positionPlayerTwo = playerTwoX, playerTwoY

    return positionPlayerOne, positionPlayerTwo

def objectLocation(gameMap, size, positionPlayerOne, positionPlayerTwo):
    ''' losowanie pozycji przedmiotow i przeciwnikow '''
    treasureLocation = []
    chestLocation = []
    monsterLocation = []
    monsterLocation.append(positionPlayerOne)
    monsterLocation.append(positionPlayerTwo)
    chestLocation.append(positionPlayerOne)
    chestLocation.append(positionPlayerTwo)

    for i in range(size): #pozycja skrabow
        treasureOk = True
        while True:
            treasureX, treasureY = random.randint(1, size - 1), random.randint(1, size - 1)
            if gameMap[treasureX][treasureY] == 1:
                for tempLoc in treasureLocation:
                    path = findPathBfs(treasureX, treasureY, gameMap, tempLoc[0], tempLoc[1], size)
                    if path < 5:
                        treasureOk = False
                    else:
                        treasureOk = True
                    if treasureOk == False:
                        break
                if treasureOk == True:
                    gameMap[treasureX][treasureY] = 44
                    treasureLocation.append((treasureX, treasureY))
                    break

    for i in range(int(size/5)): # pozycja skrzyń
        chestOk = True
        while True:
            chestX, chestY = random.randint(1, size - 1), random.randint(1, size - 1)
            if gameMap[chestX][chestY] == 1:
                for tempLoc in chestLocation:
                    path = findPathBfs(chestX, chestY, gameMap, tempLoc[0], tempLoc[1], size)
                    if path < 10:
                        chestOk = False
                    else:
                        chestOk = True
                    if chestOk == False:
                        break
                if chestOk == True:
                    gameMap[chestX][chestY] = 41
                    chestLocation.append((chestX, chestY))
                    break

    for i in range(int(size/2)): # pozycja potworow
        monsterOk = True
        while True:
            monsterX, monsterY = random.randint(1, size - 1), random.randint(1, size - 1)
            if gameMap[monsterX][monsterY] == 1:
                for tempLoc in monsterLocation:
                    path = findPathBfs(monsterX, monsterY, gameMap, tempLoc[0], tempLoc[1], size)
                    if path < 6:
                        monsterOk = False
                    else:
                        monsterOk = True
                    if monsterOk == False:
                        break
                if monsterOk == True:
                    gameMap[monsterX][monsterY] = 5
                    monsterLocation.append((monsterX, monsterY))
                    break

def generatingMap(size, professionPlayerOne, professionPlayerTwo):

    while True:
        gameMap = initializeMap(size)
        for i in range(1):
            gameMap = doSimulation(gameMap, size)

        if checkMapIntegrity(gameMap, size) != False:
            gameMap = checkMapIntegrity(gameMap, size)

            positionPlayerOne, positionPlayerTwo = exitLocation(gameMap, size, professionPlayerOne, professionPlayerTwo)
            objectLocation(gameMap, size, positionPlayerOne, positionPlayerTwo)
            listMonster = lastRender(gameMap, size)
            print("OK")
            return gameMap, positionPlayerOne, positionPlayerTwo, listMonster