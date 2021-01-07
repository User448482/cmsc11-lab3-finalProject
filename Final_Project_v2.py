import random
import sqlite3
import sys
import time

def animate(text,duration):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(duration/len(text))

def viewHighScores():
    selectTable = 'SELECT Player, Score FROM HighScores GROUP BY Player'
    data = cursor.execute(selectTable).fetchall()
    text = '\nTop 5 Scores: \n'
    animate(text,.5)
    for i in range(len(data)):
        text = data[i][0] + ' ' + str(data[i][1])
        animate(text,.5)
        print('')
    print('') 

def playerCreation():
    while 1:
        invalidName = False
        text = '\nWhat is your name? '
        animate(text,.5)
        name = str(input())
        for character in name:
            if ord(character) == 32 or (ord(character) >= 48 and ord(character) <= 57) or (ord(character) >= 65 and ord(character) <= 90) or (ord(character) >= 97 and ord(character) <= 122):
                pass
            else:
                text = 'Invalid character detected. Only letters, numbers, and spaces are allowed.\n'
                animate(text,1)
                invalidName = True
        if invalidName == False:
            playerName = name
            break
    selectTable = 'SELECT Player, Score FROM HighScores GROUP BY Player'
    data = cursor.execute(selectTable).fetchall()
    returningPlayer = False
    for i in range(len(data)):
        if playerName == data[i][0]:
            text = '\nWelcome back, ' + playerName + '!\nYour highest score is ' + str(data[i][1]) + '. Goodluck!\n\n'
            animate(text,1.5)
            returningPlayer = True
            break
    if returningPlayer == False:
        text = '\nWelcome, ' + playerName + '! Goodluck!\n\n'
        animate(text,1)

def gameStart():
    global playerName
    global currentEarnings
    global currentRound
    global lifelineCallSmartFriendUsed
    global lifelineCallUnsureFriendUsed
    global lifelineCallArrogantFriendUsed
    global lifelineFiftyFiftyUsed
    playerName = ''
    currentEarnings = 0
    currentRound = 0
    lifelineCallSmartFriendUsed = False
    lifelineCallUnsureFriendUsed = False
    lifelineCallArrogantFriendUsed = False
    lifelineFiftyFiftyUsed = False
    playerCreation()

def mainMenu():
    while 1:
        text = 'What do you want to do?\n(a) Play Game\n(b) View High Scores\n(c) Quit Game\n\nYour answer: '
        animate(text,1.5)
        answer = input()
        if answer == 'A' or answer == 'a':
            gameStart()
            break
        elif answer == 'B' or answer == 'b':
            viewHighScores()                  
        elif answer == 'C' or answer == 'c':
            text = '\nExiting...\n\n'
            animate(text,1)
            time.sleep(.7)
            sys.exit()            
            break
        else:
            print(answer) # debug
            text = '\nInvalid input.\n\n'
            animate(text,.5)
            time.sleep(.5)

def prepareRandomQuestions():
    global questionBankEasyList
    global questionBankAverageList
    global questionBankDifficultList
    questionBankEasyList = list(questionBankEasy)
    questionBankAverageList = list(questionBankAverage)
    questionBankDifficultList = list(questionBankDifficult)
    random.shuffle(questionBankEasyList)
    random.shuffle(questionBankAverageList)
    random.shuffle(questionBankDifficultList)

def programStart():
    prepareRandomQuestions()
    text = '\nWelcome to "Who Wants to be a Millionnaire"!!!\n\n'
    animate(text,1)
    mainMenu()

def initializeHighScoresDB():
    global db, cursor
    db = sqlite3.connect('highscores.db')
    cursor = db.cursor()
    createTable = 'CREATE TABLE IF NOT EXISTS HighScores (Player VARCHAR NOT NULL, Score INTEGER NOT NULL)'
    cursor.execute(createTable)

def initializeQuestionBanks():
    global questionBankEasy, questionBankAverage, questionBankDifficult, choicesBank
    questionBankEasy = {
        'e01': { 'content': 'e01 content', 'answer': 'e01 answer' },
        'e02': { 'content': 'e02 content', 'answer': 'e02 answer' },
        'e03': { 'content': 'e03 content', 'answer': 'e03 answer' },
        'e04': { 'content': 'e04 content', 'answer': 'e04 answer' },
        'e05': { 'content': 'e05 content', 'answer': 'e05 answer' },
        'e06': { 'content': 'e06 content', 'answer': 'e06 answer' },
        'e07': { 'content': 'e07 content', 'answer': 'e07 answer' },
        'e08': { 'content': 'e08 content', 'answer': 'e08 answer' },
        'e09': { 'content': 'e09 content', 'answer': 'e09 answer' },
        'e10': { 'content': 'e10 content', 'answer': 'e10 answer' }                                                                                                                                                                                                      
    }

    questionBankAverage = {
        'a01': { 'content': 'a01 content', 'answer': 'a01 answer' },
        'a02': { 'content': 'a02 content', 'answer': 'a02 answer' },
        'a03': { 'content': 'a03 content', 'answer': 'a03 answer' },
        'a04': { 'content': 'a04 content', 'answer': 'a04 answer' },
        'a05': { 'content': 'a05 content', 'answer': 'a05 answer' },
        'a06': { 'content': 'a06 content', 'answer': 'a06 answer' },
        'a07': { 'content': 'a07 content', 'answer': 'a07 answer' },
        'a08': { 'content': 'a08 content', 'answer': 'a08 answer' },
        'a09': { 'content': 'a09 content', 'answer': 'a09 answer' },
        'a10': { 'content': 'a10 content', 'answer': 'a10 answer' }                                                                                                                                                                    
    }

    questionBankDifficult = {
        'd01': { 'content': 'd01 content', 'answer': 'd01 answer' },
        'd02': { 'content': 'd02 content', 'answer': 'd02 answer' },
        'd03': { 'content': 'd03 content', 'answer': 'd03 answer' },
        'd04': { 'content': 'd04 content', 'answer': 'd04 answer' },
        'd05': { 'content': 'd05 content', 'answer': 'd05 answer' },
        'd06': { 'content': 'd06 content', 'answer': 'd06 answer' },
        'd07': { 'content': 'd07 content', 'answer': 'd07 answer' },
        'd08': { 'content': 'd08 content', 'answer': 'd08 answer' },
        'd09': { 'content': 'd09 content', 'answer': 'd09 answer' },
        'd10': { 'content': 'd10 content', 'answer': 'd10 answer' }                                                                                                                                                                    
    }

    choicesBank = {

        #easy
        'e01': ( 'e01choice01', 'e01choice02', 'e01choice03', 'e01choice04' ),
        'e02': ( 'e02choice01', 'e02choice02', 'e02choice03', 'e02choice04' ),
        'e03': ( 'e03choice01', 'e03choice02', 'e03choice03', 'e03choice04' ),
        'e04': ( 'e04choice01', 'e04choice02', 'e04choice03', 'e04choice04' ),
        'e05': ( 'e05choice01', 'e05choice02', 'e05choice03', 'e05choice04' ),
        'e06': ( 'e06choice01', 'e06choice02', 'e06choice03', 'e06choice04' ),
        'e07': ( 'e07choice01', 'e07choice02', 'e07choice03', 'e07choice04' ),
        'e08': ( 'e08choice01', 'e08choice02', 'e08choice03', 'e08choice04' ),
        'e09': ( 'e09choice01', 'e09choice02', 'e09choice03', 'e09choice04' ),
        'e10': ( 'e10choice01', 'e10choice02', 'e10choice03', 'e10choice04' ),

        #average
        'a01': ( 'a01choice01', 'a01choice02', 'a01choice03', 'a01choice04' ),
        'a02': ( 'a02choice01', 'a02choice02', 'a02choice03', 'a02choice04' ),
        'a03': ( 'a03choice01', 'a03choice02', 'a03choice03', 'a03choice04' ),
        'a04': ( 'a04choice01', 'a04choice02', 'a04choice03', 'a04choice04' ),
        'a05': ( 'a05choice01', 'a05choice02', 'a05choice03', 'a05choice04' ),
        'a06': ( 'a06choice01', 'a06choice02', 'a06choice03', 'a06choice04' ),
        'a07': ( 'a07choice01', 'a07choice02', 'a07choice03', 'a07choice04' ),
        'a08': ( 'a08choice01', 'a08choice02', 'a08choice03', 'a08choice04' ),
        'a09': ( 'a09choice01', 'a09choice02', 'a09choice03', 'a09choice04' ),
        'a10': ( 'a10choice01', 'a10choice02', 'a10choice03', 'a10choice04' ),

        #difficult
        'd01': ( 'd01choice01', 'd01choice02', 'd01choice03', 'd01choice04' ),
        'd02': ( 'd02choice01', 'd02choice02', 'd02choice03', 'd02choice04' ),
        'd03': ( 'd03choice01', 'd03choice02', 'd03choice03', 'd03choice04' ),
        'd04': ( 'd04choice01', 'd04choice02', 'd04choice03', 'd04choice04' ),
        'd05': ( 'd05choice01', 'd05choice02', 'd05choice03', 'd05choice04' ),
        'd06': ( 'd06choice01', 'd06choice02', 'd06choice03', 'd06choice04' ),
        'd07': ( 'd07choice01', 'd07choice02', 'd07choice03', 'd07choice04' ),
        'd08': ( 'd08choice01', 'd08choice02', 'd08choice03', 'd08choice04' ),
        'd09': ( 'd09choice01', 'd09choice02', 'd09choice03', 'd09choice04' ),
        'd10': ( 'd10choice01', 'd10choice02', 'd10choice03', 'd10choice04' )    

    }

while 1:
    initializeQuestionBanks()
    initializeHighScoresDB()
    programStart()
    break

sys.exit()