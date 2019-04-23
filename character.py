import random

class Character:
    ''' nadklasa postaci '''
    def __init__(self):
        self._hp = 0
        self._strenght = 0
        self._dexterity = 0
        self._stamina = 0
        self._movePoints = 0
        self._attackPoints = 0
        self._x = 0
        self._y = 0

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        self._hp = int(value)

    @property
    def strenght(self):
        return self._strenght
    @strenght.setter
    def strenght(self, value):
        self._strenght = int(value)

    @property
    def dexterity(self):
        return self._dexterity
    @dexterity.setter
    def dexterity(self, value):
        self._dexterity = int(value)

    @property
    def stamina(self):
        return self._stamina
    @stamina.setter
    def stamina(self, value):
        self._stamina = int(value)

    @property
    def movePoints(self):
        return self._movePoints
    @movePoints.setter
    def movePoints(self, value):
        self._movePoints = int(value)

    @property
    def attackPoints(self):
        return self._attackPoints
    @attackPoints.setter
    def attackPoints(self, value):
        self._attackPoints = int(value)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = int(value)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = int(value)


class Hero(Character):
    ''' podklasa postaci gracza'''
    def __init__(self):
        super().__init__()
        self._name = ""
        self._profession = 0
        self._weapon = ""
        self._talisman = ""
        self._score = 0
        self._endGame = False
        self._endTurn = False
        self._whichPlayer = 0

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def profession(self):
        return self._profession
    @profession.setter
    def profession(self, value):
        self._profession = int(value)

    @property
    def weapon(self):
        return self._weapon
    @weapon.setter
    def weapon(self, value):
        self._weapon = value

    @property
    def talisman(self):
        return self._talisman
    @talisman.setter
    def talisman(self, value):
        self._talisman = value

    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        self._score = int(value)

    @property
    def endGame(self):
        return self._endGame
    @endGame.setter
    def endGame(self, value):
        self._endGame = bool(value)

    @property
    def endTurn(self):
        return self._endTurn
    @endTurn.setter
    def endTurn(self, value):
        self._endTurn = bool(value)

    @property
    def whichPlayer(self):
        return self._whichPlayer
    @whichPlayer.setter
    def whichPlayer(self, value):
        self._whichPlayer = int(value)

    def newTurn(self):
        ''' odnawianie punktow ruchu i ataku '''
        self.endTurn = False
        if self.profession == 81 or self.profession == 91:
            self.movePoints = 5
            self.attackPoints = 3
        elif self.profession == 82 or self.profession == 92:
            self.movePoints = 7
            self.attackPoints = 2
        elif self.profession == 83 or self.profession == 93:
            self.movePoints = 5
            self.attackPoints = 3

    def defend(self, damage):
        speed = self.dexterity
        if self.talisman != "":
            speed += self.talisman.addDexterity
        speed *= 5

        if speed <= random.randint(1, 100): # jezeli nie uda sie unik
            armor = self.stamina
            if self.weapon != "":
                armor += self.weapon.addStamina
            if self.talisman != "":
                armor += self.talisman.addStamina
            self.hp = self.hp - (damage - int(armor/2))


    def attack(self):
        self.attackPoints -= 1

        speed = self.dexterity
        if self.talisman != "":
            speed += self.talisman.addDexterity
        speed *= 5
        damage = self.strenght
        if self.weapon != "":
            damage += self.weapon.addStrenght

        if speed <= random.randint(1, 100):
            return damage
        else:
            return damage*2

    def counterattack(self):
        damage = self.strenght
        if self.weapon != "":
            damage = self.weapon.addStrenght
        return int(damage*0.75)

    def moveComputer(self, gameMap):
        positionPlayerX, positionPlayerY = 0, 0
        positionMonsterX, positionMonsterY = 0, 0
        positionTreasureX, positionTreasureY = 0, 0
        positionExitX, positionExitY = 0, 0

        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if (i == self.x-1 and j == self.y) or (i == self.x+1 and j == self.y) or (i == self.x and j == self.y+1) or (i == self.x and j == self.y-1):
                    if gameMap[i][j] in range(81, 84):
                        positionPlayerX, positionPlayerY = i, j
                    elif gameMap[i][j] in range(51, 60):
                        positionMonsterX, positionMonsterY = i, j
                    elif gameMap[i][j] in range(31, 45):
                        positionTreasureX, positionTreasureY = i, j
                    elif gameMap[i][j] == 2:
                        positionExitX, positionExitY = i, j

        if positionExitX != 0 and positionExitY != 0:
            result = self.way(positionExitX, positionExitX)
            return result
        elif positionTreasureX!= 0 and positionTreasureY != 0:
            result = self.way(positionTreasureX, positionTreasureY)
            return result
        elif positionMonsterX != 0 and positionMonsterY != 0:
            result = self.way(positionMonsterX, positionMonsterY)
            return result
        elif positionPlayerX != 0 and positionPlayerY != 0:
            result = self.way(positionPlayerX, positionPlayerY)
            return result
        else:
            direction = random.randint(1,4)
            if direction == 1:
                return "up"
            elif direction == 2:
                return "down"
            elif direction == 3:
                return "right"
            elif direction == 4:
                return "left"


    def way(self, positionX, positionY):
        positionX -= self.x
        positionY -= self.y
        print(positionX, positionY)

        if positionX == -1 and positionY == 0:
            return str("up")
        elif positionX == 1 and positionY == 0:
            return str("down")
        elif positionX == 0 and positionY == 1:
            return str("right")
        elif positionX == 0 and positionY == -1:
            return str("left")

class Monster(Character):
    ''' podklasa potworow '''
    def __init__(self):
        super().__init__()
        self._typeMonster = 0
        self._scorePoint = 0

    @property
    def typeMonster(self):
        return self._typeMonster
    @typeMonster.setter
    def typeMonster(self, value):
        self._typeMonster = int(value)

    @property
    def item(self):
        return self._item
    @item.setter
    def item(self, value):
        self._item = int(value)

    def defend(self, damage):
        if (self.dexterity * 5) <= random.randint(1, 100): # jezeli nie uda sie unik
            self.hp = self.hp - (damage - int(self.stamina/2))

    def attack(self):
        self.attackPoints -= 1

        if (self.dexterity * 5) <= random.randint(1, 100):
            return self.strenght
        else:
            return self.strenght*2

    def counterattack(self):
        return int(self.strenght*0.75)

    def monsterAttack(self, map, playerOne, playerTwo):
        if self.attackPoints > 0:
            for i in range(self.x-1, self.x+2):
                for j in range(self.y-1, self.y+2):
                    if (i == self.x - 1 and j == self.y) or (i == self.x + 1 and j == self.y) or (i == self.x and j == self.y + 1) or (i == self.x and j == self.y - 1):
                        if map[i][j] in range(81, 84):
                            self.attackPoints -= 1

                            playerOne.defend(self.attack())
                            if playerOne.hp <= 0:
                                map[playerOne.x][playerOne.y] = random.randint(11, 18)
                                playerOne.endGame = True

                            self.defend(playerOne.counterattack())
                            if self.hp <= 0:
                                map[self.x][self.y] = random.randint(11, 18)
                                playerOne.hp += random.randint(0, 2)
                                playerOne.score += self.scorePoint
                                self.x, self.y = -1, -1

                        elif map[i][j] in range(91,94):
                            self.attackPoints -= 1

                            playerTwo.defend(self.attack())
                            if playerTwo.hp <= 0:
                                map[playerTwo.x][playerTwo.y] = random.randint(11, 18)
                                playerTwo.endGame = True

                            self.defend(playerTwo.counterattack())
                            if self.hp <= 0:
                                map[self.x][self.y] = random.randint(11, 18)
                                playerTwo.hp += random.randint(0, 2)
                                playerTwo.score += self.scorePoint
                                self.x, self.y = -1, -1



    def monsterMove(self, map):
        if self.movePoints > 0:
            way = random.randint(1,4)
            if way == 1:
                if map[self.x+1][self.y] in range(11, 19):
                    self.movePoints -= 1
                    map[self.x][self.y] = random.randint(11, 18)
                    self.x = self.x+1
                    map[self.x][self.y] = self.typeMonster
                else:
                    self.movePoints -= 1

            elif way == 2:
                if map[self.x-1][self.y] in range(11, 19):
                    self.movePoints -= 1
                    map[self.x][self.y] = random.randint(11, 18)
                    self.x = self.x-1
                    map[self.x][self.y] = self.typeMonster
                else:
                    self.movePoints -= 1

            elif way == 3:
                if map[self.x][self.y-1] in range(11, 19):
                    self.movePoints -= 1
                    map[self.x][self.y] = random.randint(11, 18)
                    self.y = self.y-1
                    map[self.x][self.y] = self.typeMonster
                else:
                    self.movePoints -= 1

            elif way == 4:
                if map[self.x][self.y+1] in range(11, 19):
                    self.movePoints -= 1
                    map[self.x][self.y] = random.randint(11, 18)
                    self.y = self.y+1
                    map[self.x][self.y] = self.typeMonster
                else:
                    self.movePoints -= 1


    def monsterTurn(self, map, playerOne, playerTwo):
        self.monsterAttack(map, playerOne, playerTwo)
        self.monsterAttack(map, playerOne, playerTwo)
        self.monsterMove(map)
        self.monsterAttack(map, playerOne, playerTwo)
        self.monsterAttack(map, playerOne, playerTwo)
        self.monsterMove(map)
        self.monsterAttack(map, playerOne, playerTwo)
        self.monsterAttack(map, playerOne, playerTwo)

        self.movePoints = 2
        self.attackPoints = 2