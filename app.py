import random

from flask import Flask
from flask import render_template, request, redirect, url_for

from generateMap import generatingMap
from moveMap import playerMove
from character import Hero
from heroMonsterList import makeHero, delHero

app = Flask(__name__)

map = ''
size = 0
mode = ''
playerOne = Hero()
playerTwo = Hero()
monsterList = []

@app.route('/')
def index():
    return render_template('formularz.html')
    #return render_template('index.html',  size=20, gameMap=map)

#podejrzenie mapy
@app.route('/map')
def map():
    global map, size
    return render_template('index.html',  size=size, gameMap=map)

#tworzenie postaci w single player i przekierowywanie do innych trybow
@app.route('/makeNewGame', methods = ['POST'])
def makeNewGame():
    global map, size, mode, monsterList
    data = request.form

    makeHero(playerOne, data['name'], int(data['profession']), 1)
    size = int(data['size'])
    mode = data['mode']
    if mode == 'onePlayer':
        professionAI = random.randint(91,94)
        makeHero(playerTwo, 'Bad Guy', professionAI, 2)
    elif mode == 'hotSeat':
        return redirect(url_for('playerTwoChoosing'))
    elif mode == 'twoPlayers':
        return redirect(url_for('waiting'))

    map, positionPlayerOne, positionPlayerTwo, monsterList = generatingMap(size, playerOne.profession, playerTwo.profession)
    playerOne.x, playerOne.y = positionPlayerOne
    playerTwo.x, playerTwo.y = positionPlayerTwo
    return redirect(url_for('onePlayer'))

#oczekiwanie na 2 gracza w multi
@app.route('/makeNewGame/waiting')
def waiting():
    return render_template('waiting.html')

#formularz wyboru postaci dla drugiego gracza w hotseat
@app.route('/makeNewGame/playerTwoChoosing')
def playerTwoChoosing():
    return render_template('playerTwoChoosing.html')

#tworzenie postaci i mapy w hotseat
@app.route('/makeNewGame/playerTwoChoosing/generate', methods = ['POST'])
def generate():
    global map, size, monsterList
    data = request.form
    makeHero(playerTwo, data['name'], int(data['profession']), 2)

    map, positionPlayerOne, positionPlayerTwo, monsterList = generatingMap(size, playerOne.profession, playerTwo.profession)
    playerOne.x, playerOne.y = positionPlayerOne
    playerTwo.x, playerTwo.y = positionPlayerTwo
    return redirect(url_for('hotSeat'))

#obsluga ruchow poszczegolnego gracza
@app.route('/game/<int:player>/move', methods = ['POST'])
def move(player):
    global map, monsterList, mode
    if player == 1:
        player1 = playerOne
        player2 = playerTwo
    elif player == 2:
        player1 = playerTwo
        player2 = playerOne

    data = request.form
    data = data['move']
    positionPlayer = playerMove(map, data, player1, monsterList, player2)

    if playerOne.endGame == True and playerTwo.endGame == True:
        return redirect(url_for('end'))
    if positionPlayer == True:
        if mode == 'hotSeat':
            return redirect(url_for('hotSeat'))
        elif mode == 'onePlayer':
            return redirect(url_for('end'))
    if positionPlayer != False:
        player1.x, player1.y = positionPlayer
    return redirect(url_for('game', player=player1.whichPlayer))

#obsługa ruchu AI
@app.route('/game/AI')
def moveAI():
    global map, monsterList
    player1 = playerTwo
    player2 = playerOne

    while player1.movePoints > 0:
        data = player1.moveComputer(map)
        positionPlayer = playerMove(map, data, player1, monsterList, player2)

        if playerOne.endGame == True and playerTwo.endGame == True:
            return redirect(url_for('end'))
        elif positionPlayer == "END":
            return redirect(url_for('onePlayer'))
        if positionPlayer != False:
            player1.x, player1.y = positionPlayer

    return redirect(url_for('onePlayer'))

#obsluga konca gry
@app.route('/end')
def end():
    return render_template('end.html', playerOne=playerOne, playerTwo=playerTwo)

#zerowanie potworow i graczy
@app.route('/endGame', methods = ['POST'])
def endGame():
    global monsterList
    monsterList = []
    delHero(playerOne)
    delHero(playerTwo)
    return redirect(url_for('index'))

#wyswietlanie interfejsu gry
@app.route('/game/<int:player>')
def game(player):
    global size, map, mode, monsterList
    if player == 1:
        player = playerOne
    else:
        player = playerTwo
    x, y = player.x, player.y
    return render_template('game.html', size=size, gameMap=map, x=x, y=y, player=player, mode=mode, monsterList=monsterList)

#obsluga tury w rozgrywce hotSeat
@app.route('/hotSeat')
def hotSeat():
    global map, monsterList

    if playerOne.endGame == False and playerOne.endTurn == False: #ruch gracza1
        playerOne.endTurn = True
        return redirect(url_for('game', player=1))
    if playerTwo.endGame == False and playerTwo.endTurn == False: #ruch gracza2
        playerTwo.endTurn = True
        return redirect(url_for('game', player=2))

    for monster in monsterList:                         #ruch potworow
        if monster.hp > 0:
            monster.monsterTurn(map, playerOne, playerTwo)

    if playerOne.endGame == True and playerTwo.endGame == True:
        return redirect(url_for('end'))

    return redirect(url_for('nextTurn'))

#obsluga tury w rozgrywce dla jednego gracza
@app.route('/onePlayer')
def onePlayer():
    global map
    if playerOne.endGame == False and playerOne.endTurn == False: #ruch gracza1
        playerOne.endTurn = True
        return redirect(url_for('game', player=1))
    if playerTwo.endGame == False and playerTwo.endTurn == False: #ruch AI
        playerTwo.endTurn = True
        return redirect(url_for('moveAI'))

    for monster in monsterList:                         #ruch potworow
        if monster.hp > 0:
            monster.monsterTurn(map, playerOne, playerTwo)

    if playerOne.endGame == True:
        return redirect(url_for('end'))

    return redirect(url_for('nextTurn'))

#ustawianie argumentów na kolejna ture
@app.route('/nextTurn')
def nextTurn():
    global mode
    playerOne.newTurn()
    playerTwo.newTurn()
    if mode == "hotSeat":
        return redirect(url_for('hotSeat'))
    elif mode == "onePlayer":
        return redirect(url_for('onePlayer'))

#zakończenie tury
@app.route('/endTurn', methods = ['POST'])
def endTurn():
    global mode
    if mode == "hotSeat":
        return redirect(url_for('hotSeat'))
    elif mode == "onePlayer":
        return redirect(url_for('onePlayer'))

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5035)