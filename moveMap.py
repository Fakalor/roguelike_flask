import random
from item import Item
from character import Monster
from heroMonsterList import makeItem, makeMonster

def playerMove(gameMap, action, player1, listMonster, player2):
    ''' poruszanie się xD '''
    if action == "up":
        x, y = -1, 0
    elif action == "down":
        x, y = 1, 0
    elif action == "left":
        x, y = 0, -1
    elif action == "right":
        x, y = 0, 1
    elif action == "pickup":
        position = player1.x, player1.y
        return position
    else:
        print(action)

    position = player1.x, player1.y
    newPosition = checkCollision(gameMap, player1, x, y, listMonster, player2)
    if newPosition != False:
        return newPosition
    else:
        return position


def checkCollision(gameMap, player1, x, y, listMonster, player2):
    ''' kolizja ze scianami i obiektami w grze '''
    x1, y1 = player1.x, player1.y
    x1 += x
    y1 += y
    x, y = player1.x, player1.y
    if gameMap[x1][y1] != 0:
        if player1.movePoints > 0:
            if gameMap[x1][y1] in range(10,19): # wejscie na zwykle pole
                gameMap[x][y] = random.randint(11,18)
                gameMap[x1][y1] = player1.profession
                player1.movePoints -= 1
                position = x1, y1
                return position

            if gameMap[x1][y1] == 2:    # trafienie na wyjscie
                gameMap[x][y] = random.randint(11, 18)
                player1.score *= 2
                player1.endGame = True
                return True

            if gameMap[x1][y1] in range(31,38):  # trafienie na przedmiot
                item = Item()
                makeItem(item, gameMap[x1][y1])
                if gameMap[x1][y1] in range(31,35):
                    player1.weapon = item
                else:
                    player1.talisman = item

                gameMap[x][y] = random.randint(11, 18)
                gameMap[x1][y1] = player1.profession
                player1.movePoints -= 1
                player1.score += 50
                position = x1, y1
                return position

            if gameMap[x1][y1] == 41: # trafienie na zamknieta skrzynke
                tempChest = random.randint(1, 101)
                if tempChest in range(1,6):     # skrzynia zmienia sie w grozny zwierz
                    gameMap[x1][y1] = 42
                    monster = Monster()
                    makeMonster(monster, 42, x1, y1)
                    listMonster.append(monster)
                elif tempChest in range(6, 21): # w skrzyni jest skarb
                    gameMap[x1][y1] = 43
                else:
                    tempItem = random.randint(31, 37)
                    gameMap[x1][y1] = tempItem       # w skrzyni jest przedmiot
                player1.movePoints -= 1
                position = x, y
                return position

            if gameMap[x1][y1] == 43:  # trafienie na otwarta skrzynke
                gameMap[x][y] = random.randint(11, 18)
                gameMap[x1][y1] = player1.profession
                player1.movePoints -= 1
                player1.score += 500
                position = x1, y1
                return position

            if gameMap[x1][y1] == 44:  # trafienie na skarb
                gameMap[x][y] = random.randint(11, 18)
                gameMap[x1][y1] = player1.profession
                player1.movePoints -= 1
                player1.score += 100
                position = x1, y1
                return position
        if player1.attackPoints > 0:
            if gameMap[x1][y1] in range(51, 60) or gameMap[x1][y1] == 42:    #trafienie na przeciwnika
                position = x, y
                for tempMonster in listMonster:
                    if x1 == tempMonster.x and y1 == tempMonster.y:
                        monster = tempMonster
                        break

                monster.defend(player1.attack())
                if monster.hp <= 0:
                    gameMap[monster.x][monster.y] = random.randint(11, 18)
                    player1.hp += random.randint(0, 1)
                    player1.score += monster.scorePoint
                    monster.x, monster.y = -1, -1
                    return position

                player1.defend(monster.counterattack())
                if player1.hp <= 0:
                    gameMap[player1.x][player1.y] = random.randint(11, 18)
                    player1.endGame = True
                    player1.x, player1.y = -1, -1
                    return True

                return position

            if gameMap[x1][y1] in range(81, 84) or gameMap[x1][y1] in range(91, 94):
                position = x, y

                player2.defend(player1.attack())
                if player2.hp <= 0:
                    gameMap[player2.x][player2.y] = random.randint(11, 18)
                    player1.hp += random.randint(0, 1)
                    player1.score += 500
                    player2.endGame = True
                    player2.x, player2.y = -1, -1
                    return position

                player1.defend(player2.counterattack())
                if player1.hp <= 0:
                    gameMap[player1.x][player1.y] = random.randint(11, 18)
                    player2.hp += random.randint(0, 1)
                    player2.score += 500
                    player1.endGame = True
                    player1.x, player1.y = -1, -1
                    return True

                return position
    else:                           #trafienie na sciane
        return False

    return False