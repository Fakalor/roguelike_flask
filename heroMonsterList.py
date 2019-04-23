from character import Hero, Monster
import random

def makeHero(player, name, profession, whichPlayer):
    ''' tworzenie obiektu bohatera gracza '''
    player.name = name
    player.profession = profession
    player.whichPlayer = whichPlayer

    if player.profession == 81 or player.profession == 91: # tworzenie rycerza
        player.hp = 6
        player.strenght = 4
        player.dexterity = 2
        player.stamina = 3
        player.movePoints = 5
        player.attackPoints = 3
    elif player.profession == 82 or player.profession == 92: # tworzenie zlodzieja
        player.hp = 5
        player.strenght = 3
        player.dexterity = 6
        player.stamina = 2
        player.movePoints = 7
        player.attackPoints = 2
    elif player.profession == 82 or player.profession == 93: # tworzenie berserkera
        player.hp = 6
        player.strenght = 4
        player.dexterity = 4
        player.stamina = 2
        player.movePoints = 5
        player.attackPoints = 3

def makeMonster(monster, type, x, y):
    ''' tworzenie obiektu potwora gracza '''
    monster.typeMonster = type
    monster.movePoints = 2
    monster.attackPoints = 2
    monster.x = x
    monster.y = y

    if monster.typeMonster == 42:
        monster.hp = 6
        monster.strenght = 3
        monster.dexterity = 8
        monster.stamina = 2
        monster.scorePoint = 100
    if monster.typeMonster == 51:
        monster.hp = 8
        monster.strenght = 5
        monster.dexterity = 3
        monster.stamina = 4
        monster.scorePoint = 300
    elif monster.typeMonster == 52:
        monster.hp = 8
        monster.strenght = 4
        monster.dexterity = 3
        monster.stamina = 4
        monster.scorePoint = 300
    elif monster.typeMonster == 53:
        monster.hp = 10
        monster.strenght = 5
        monster.dexterity = 4
        monster.stamina = 0
        monster.scorePoint = 300
    elif monster.typeMonster == 54:
        monster.hp = 6
        monster.strenght = 3
        monster.dexterity = 4
        monster.stamina = 0
        monster.scorePoint = 100
    elif monster.typeMonster == 55:
        monster.hp = 6
        monster.strenght = 4
        monster.dexterity = 3
        monster.stamina = 2
        monster.scorePoint = 200
    elif monster.typeMonster == 56:
        monster.hp = 5
        monster.strenght = 3
        monster.dexterity = 5
        monster.stamina = 2
        monster.scorePoint = 100
    elif monster.typeMonster == 57:
        monster.hp = 5
        monster.strenght = 3
        monster.dexterity = 10
        monster.stamina = 4
        monster.scorePoint = 150
    elif monster.typeMonster == 58:
        monster.hp = 5
        monster.strenght = 3
        monster.dexterity = 4
        monster.stamina = 2
        monster.scorePoint = 100
    elif monster.typeMonster == 59:
        monster.hp = 6
        monster.strenght = 3
        monster.dexterity = 2
        monster.stamina = 4
        monster.scorePoint = 150

def makeItem(item, typeItem):
    item.typeItem = typeItem
    if typeItem in range(31,35):
        item.addStrenght = random.randint(1, 2)
        item.addStamina = random.randint(0, 2)
    else:
        item.addDexterity = random.randint(1, 2)
        item.addStamina = random.randint(1, 2)

def delHero(player):
    player.hp = 0
    player.strenght = 0
    player.dexterity = 0
    player.stamina = 0
    player.movePoints = 0
    player.attackPoints = 0
    player.x = 0
    player.y = 0

    player.name = ""
    player.profession = 0
    player.weapon = ""
    player.talisman = ""
    player.score = 0
    player.endGame = False
    player.endTurn = False
    player.whichPlayer = 0
