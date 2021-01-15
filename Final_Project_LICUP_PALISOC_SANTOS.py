# CMSC11 LEC3-LAB3 Final Project: Machine Problem
# Licup, John Paolo
# Palisoc, May Ann Grace
# Santos, Ethan Mark

# import modules, arranged alphabetically
import os
import pathlib
import random
import sqlite3
import sys
import time

# declare global variables, arranged alphabetically
actionsList = []
averageQuestions = []
choicesList = []
choicesString = ''
contentCursor = ''
contentDB = ''
correctAnswer = ''
currentEarnings = 0
currentRound = 0
difficultQuestions = []
easyQuestions = []
fiftyFiftyUsed = False
gameOver = False
highScoresCursor = ''
highScoresDB = ''
instantText = ''
instantUI = False
lifelinesEnabled = True
lifelinesList = []
newInstantText = ''
playerName = ''
questionContent = ''
questionID = ''
returningPlayer = False
roundDifficulty = ''
roundPrize = 0

# defining functions

def reloadUI():
    os.system('cls')
    print(instantText+newInstantText, sep='', end='')

def wait(duration):
    time.sleep(duration)

def animateCaps(text,duration):
    caps = list(text.upper())
    textList = list(text)
    for i in range(len(textList)):
        textList[i] = caps[i]
        os.system('cls')
        toPrint = ''.join(str(elem) for elem in textList)
        print(toPrint)
        wait(duration/len(textList))

def typeWrite(text,duration):
    for letter in text:
        print(letter, end='', flush=True)
        wait(duration/len(text))

def convertScore(text):
    if len(text) >= 4:
        spaceCount = int(len(text)/3)
        if len(text)%3 == 0:
            spaceCount -= 1
    else:
        spaceCount = 0
    textList = list(text)
    if spaceCount >= 1:
        j = 0
        for i in range(spaceCount):
            textList.insert(((-3*(i+1))+j),',')
            j -= 1
    newText = '$'
    for elem in textList:
        newText += elem
    return newText

def convertChoice(str):
    if str == '0':
        return 'a'
    if str == '1':
        return 'b'
    if str == '2':
        return 'c'
    if str == '3':
        return 'd'
    if str == 'a' or str == 'A':
        return '0'
    if str == 'b' or str == 'B':
        return '1'
    if str == 'c' or str == 'C':
        return '2'
    if str == 'd' or str == 'D':
        return '3'

def prepareContentDB():
    global contentCursor, contentDB
    contentDB = sqlite3.connect('content.db')
    contentCursor = contentDB.cursor()

def exitProgram():
    global contentCursor, highScoresCursor
    text = 'Exiting program...\n\n'
    typeWrite(text,.5)
    #highScoresCursor.close()
    #contentCursor.close()
    wait(1)
    sys.exit()

def checkDB():
    if os.path.isfile('content.db'):
        prepareContentDB()
    else:
        text = '\nERROR! "content.db" file which contains the questions and choices is not found. Make sure the "content.db" file is in the current working directory.\n\n'
        typeWrite(text,1)
        wait(1)
        exitProgram()

def prepareHighScoresDB():
    global highScoresCursor, highScoresDB
    highScoresDB = sqlite3.connect('highscores.db')
    highScoresCursor = highScoresDB.cursor()
    highScoresCursor.execute('CREATE TABLE IF NOT EXISTS HighScores (Player VARCHAR NOT NULL, Score INTEGER NOT NULL)')

def prepareLifelines():
    global lifelinesList
    lifelinesList = ['Call a Friend (Smart)', 'Call a Friend (Unsure)', 'Call a Friend (Arrogant)', 'Fifty-fifty']

def randomizeQuestions():
    global easyQuestions, averageQuestions, difficultQuestions
    data = contentCursor.execute('SELECT questionID FROM Easy').fetchall()
    easyQuestions = random.sample(data,5)
    data = contentCursor.execute('SELECT questionID FROM Average').fetchall()
    averageQuestions = random.sample(data,5)
    data = contentCursor.execute('SELECT questionID FROM Difficult').fetchall()
    difficultQuestions = random.sample(data,5)
    random.shuffle(easyQuestions)
    random.shuffle(averageQuestions)
    random.shuffle(difficultQuestions)

def playerLogin():
    global playerName, returningPlayer
    os.system('cls')
    validName = False
    while validName == False:
        text = '\nWhat is your name? '
        typeWrite(text,1)
        temp = input()
        for character in temp:
            if ord(character) == 32 or (ord(character) >= 48 and ord(character) <= 57) or (ord(character) >= 65 and ord(character) <= 90) or (ord(character) >= 97 and ord(character) <= 122):
                validName = True
            else:
                text = '\nInvalid character detected. Only letters, numbers, and spaces are allowed.\n'
                typeWrite(text,1)
                break
    playerName = temp        
    data = highScoresCursor.execute('SELECT Player, Score from HighScores')
    returningPlayer = False
    for elem in data:
        if playerName == elem[0]:
            returningPlayer = True
            text = '\nWelcome back, ' + playerName + '! Your highest score is ' + convertScore(str(elem[1])) + '. Goodluck!'
            typeWrite(text,2)
            wait(2)
            break
    if returningPlayer == False:
        text = '\nGoodluck, ' + playerName + '!'
        typeWrite(text,1)
        wait(1)

def setRoundDifficulty(currentRound):
    if currentRound <= 5:
        return 'easy'
    if currentRound > 5 and currentRound <= 10:
        return 'average'
    if currentRound > 10 and currentRound <= 15:
        return 'difficult'

def setRoundPrize(currentRound):
    if currentRound == 1:
        return 1000
    if currentRound == 2:
        return 3000
    if currentRound == 3:
        return 5000
    if currentRound == 4:
        return 10000
    if currentRound == 5:
        return 20000
    if currentRound == 6:
        return 35000
    if currentRound == 7:
        return 50000
    if currentRound == 8:
        return 70000
    if currentRound == 9:
        return 100000
    if currentRound == 10:
        return 150000
    if currentRound == 11:
        return 250000
    if currentRound == 12:
        return 400000
    if currentRound == 13:
        return 600000
    if currentRound == 14:
        return 1000000
    if currentRound == 15:
        return 2000000

def getRandomQuestion(roundDifficulty):
    if roundDifficulty == 'easy':
        return easyQuestions[currentRound-1][0]
    if roundDifficulty == 'average':
        return averageQuestions[currentRound-6][0]
    if roundDifficulty == 'difficult':
        return difficultQuestions[currentRound-11][0]

def setContent():
    global actionsList, choicesList, correctAnswer, fiftyFiftyUsed, gameOver, instantText, lifelinesEnabled, newInstantText, questionContent
    instantText = ''
    newInstantText = ''
    lifelinesEnabled = True
    fiftyFiftyUsed = False
    actionsList = ['Answer the question', 'Use a lifeline', 'Walk away with current earnings']
    if currentRound == 1:
        actionsList.remove('Walk away with current earnings')
    if roundDifficulty == 'easy':
        questionContent = str(contentCursor.execute('SELECT questionContent FROM Easy WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        correctAnswer = str(contentCursor.execute('SELECT correctAnswer FROM Easy WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        choicesList = list(contentCursor.execute('SELECT choice1, choice2, choice3, choice4 FROM Easy WHERE questionID = (?)', (questionID,)).fetchall()[0])
    if roundDifficulty == 'average':
        questionContent = str(contentCursor.execute('SELECT questionContent FROM Average WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        correctAnswer = str(contentCursor.execute('SELECT correctAnswer FROM Average WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        choicesList = list(contentCursor.execute('SELECT choice1, choice2, choice3, choice4 FROM Average WHERE questionID = (?)', (questionID,)).fetchall()[0])
    if roundDifficulty == 'difficult':
        questionContent = str(contentCursor.execute('SELECT questionContent FROM Difficult WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        correctAnswer = str(contentCursor.execute('SELECT correctAnswer FROM Difficult WHERE questionID = (?)', (questionID,)).fetchall()[0][0])
        choicesList = list(contentCursor.execute('SELECT choice1, choice2, choice3, choice4 FROM Difficult WHERE questionID = (?)', (questionID,)).fetchall()[0])
    if currentRound == 15:   
        lifelinesEnabled = False
        actionsList.remove('Use a lifeline')
    if len(lifelinesList) == 0:
        actionsList.remove('Use a lifeline')
    random.shuffle(choicesList)

def updateHighScores():
    global highScoresDB
    if returningPlayer == True:
        highScoresCursor.execute('UPDATE HighScores SET Score = (?) WHERE Player = (?)', (currentEarnings, playerName))
        highScoresDB.commit()
    else:
        highScoresCursor.execute('INSERT INTO HighScores (Player, Score) VALUES (?,?)', (playerName, currentEarnings))
        highScoresDB.commit()
        # count distinct Scores if there are 2 or more records
        data = highScoresCursor.execute('SELECT Player, Score FROM HighScores ORDER BY Score DESC').fetchall()
        if len(data) > 1:
            counter = 1
            for i in range(len(data)-1):
                if data[i+1][1] != data[i][1]:
                    counter += 1
                if counter > 5:
                    excess = len(data) - i - 1
                    for j in range(excess): # delete excess
                        highScoresCursor.execute('DELETE from HighScores WHERE Player = (?)',(data[j+5][0],))
            highScoresDB.commit()
    text = '\nNEW High Scores:\n\n'
    data = highScoresCursor.execute('SELECT Player, Score FROM HighScores ORDER BY Score DESC').fetchall()
    for elem in data:
        text += str(elem[0]) + ': ' + convertScore(str(elem[1])) + '\n'
    wait(1)
    typeWrite(text,1)

def checkIfHighScore():
    if returningPlayer == False:
        highScoresList = highScoresCursor.execute('SELECT Player, Score from HighScores ORDER BY Score DESC').fetchall()
        if len(highScoresList) > 1:
            counter = 1
            for i in range(len(highScoresList)-1):
                if highScoresList[i+1][1] != highScoresList[i][1]:
                    counter += 1
        else:
            counter = 0
        if counter < 5:
            lowest = 0
        else:
            lowest = highScoresList[-1][1]
        if currentEarnings >= lowest:
            text = '\n\nYou have made it to TOP 5 scores! Congratulations!\n'
            typeWrite(text,1)
            updateHighScores()
            wait(1)
        else:
            text = '\n\nYour score did not make it TOP 5. Better luck next time!\n'
            typeWrite(text,1)
            wait(1)
    if returningPlayer == True:
        lastscore = highScoresCursor.execute('SELECT Score FROM HighScores WHERE Player = (?)', (playerName,)).fetchall()
        if currentEarnings > lastscore[0][0]:
            text = '\n\nYou have set a new record! Congratulations!\n'
            typeWrite(text,1)
            updateHighScores()
            wait(1)
        else:
            text = '\n\nYou did not beat your old score! Better luck next time!\n'
            typeWrite(text,1)
            wait(1)    

def walkAway():
    global gameOver
    text = '\nYou walk away with ' + convertScore(str(currentEarnings)) + '. Congratulations!'
    typeWrite(text,1)
    checkIfHighScore()
    gameOver = True
    wait(1)

def askAndCheckAnswer():
    global currentEarnings, gameOver
    finalAnswer = False
    reloadUI()
    text = '\nWhat is the letter of your answer? '
    typeWrite(text,1)
    while 1:
        answer = input()
        if answer == 'a' or answer == 'A' or answer == 'b' or answer == 'B' or answer == 'c' or answer == 'C' or answer == 'd' or answer == 'D':
            if roundDifficulty == 'average' or roundDifficulty == 'difficult':
                text = '\n(y/n) Is that your final answer? '
                typeWrite(text,1)
                while 1:
                    confirm = input()
                    if confirm == 'y' or confirm == 'Y':
                        finalAnswer = True
                        break
                    elif confirm == 'n' or confirm == 'N':
                        finalAnswer = False
                        break
                    else:
                        text = '\nInvalid input. (y/n) Is that your final answer? '
                        typeWrite(text,1)
            else:
                finalAnswer = True
            if finalAnswer == False:
                reloadUI()
                text = '\nWhat is the letter of your answer? '
                typeWrite(text,1)
            if finalAnswer == True:
                text = '\nYour answer is... '
                typeWrite(text,1)
                wait(1)
                if correctAnswer == choicesList[int(convertChoice(answer))]:
                    currentEarnings = roundPrize
                    text = 'correct! Your current earnings is now ' + convertScore(str(roundPrize)) + '! Congratulations!'
                    typeWrite(text,1)
                    wait(1.5)
                    if currentRound == 15:
                        text = '\n\nCongratulations on winning the game! You are now a millionnaire!'
                        typeWrite(text,1)
                        wait(.5)
                        checkIfHighScore()
                        gameOver = True
                        wait(1)
                else:
                    text = 'incorrect!'
                    if currentRound >= 5 and currentRound < 10:
                        currentEarnings = 20000
                        text += ' Since you made it past the first safe haven Round 5, you walk away with ' + convertScore(str(currentEarnings)) + '. Congratulations!'
                        typeWrite(text,1)
                        checkIfHighScore()
                        gameOver = True
                    elif currentRound >= 10:
                        currentEarnings = 150000
                        text += ' Since you made it past the second safe haven Round 10, you walk away with ' + convertScore(str(currentEarnings)) + '. Congratulations!'
                        typeWrite(text,1)
                        checkIfHighScore()
                        gameOver = True
                    else:
                        currentEarnings = 0
                        text += ' You did not make it the first safe haven Round 5. You walk away with ' + convertScore(str(currentEarnings)) + '. Better luck next time!\n'   
                        typeWrite(text,1)
                        wait(1.5)
                        gameOver = True
                break
        else:
            text = '\nInvalid input. What is the letter of your answer? '
            typeWrite(text,1)

def useLifeline():
    global choicesList, choicesString, fiftyFiftyUsed, instantText, instantUI, lifelinesList, newInstantText
    reloadUI()
    text = '\n'
    for i in range(len(lifelinesList)):
        text += '(' + str(i+1) + ') ' + lifelinesList[i]
        if i != len(lifelinesList)-1:
            text += '\n'
    typeWrite(text,1)
    wait(.5)
    text = '\n\nWhich lifeline do you want to use? '
    typeWrite(text,1)
    while 1:
        answer = input()
        if answer == '1' or answer == '2' or answer == '3' or answer == '4':
            if lifelinesList[int(answer)-1] == 'Call a Friend (Smart)':
                lifelinesList.remove('Call a Friend (Smart)')
                if random.randint(1,10) <= 9:
                    suggestion = correctAnswer
                else:
                    wrongAnswersList = choicesList[:]
                    wrongAnswersList.remove(correctAnswer)
                    if len(wrongAnswersList) == 1:
                        suggestion = wrongAnswersList[0]
                    else:
                        suggestion = wrongAnswersList[random.randint(0,len(wrongAnswersList)-1)]   
                text = '\nCalling (smart) friend...\n'
                typeWrite(text,1)
                wait(1)
                text = '"Hi ' + playerName + '! Thanks for calling me. I' + "'" + 'm pretty sure the answer is ' + suggestion + '. Goodluck!"'
                typeWrite(text,2)
                instantUI = True  
                newInstantText += '\nSmart friend suggestion: ' + suggestion + '\n'
                wait(2)
                break
            if lifelinesList[int(answer)-1] == 'Call a Friend (Unsure)':
                lifelinesList.remove('Call a Friend (Unsure)')
                if random.randint(1,2) == 1:
                    suggestion = correctAnswer
                else:
                    wrongAnswersList = choicesList[:]
                    wrongAnswersList.remove(correctAnswer)
                    if len(wrongAnswersList) == 1:
                        suggestion = wrongAnswersList[0]
                    else:
                        suggestion = wrongAnswersList[random.randint(0,len(wrongAnswersList)-1)]                        
                text = '\nCalling (unsure) friend...\n'
                typeWrite(text,1)
                wait(1)
                text = '"Hello ' + playerName + '! I appreciate your call but I' + "'" + 'm not sure on this one. But if I were to guess, the answer is ' + suggestion + '. Goodluck!"'
                typeWrite(text,2)
                instantUI = True
                newInstantText += '\nUnsure friend suggestion: ' + suggestion + '\n'
                wait(2)
                break
            if lifelinesList[int(answer)-1] == 'Call a Friend (Arrogant)':
                lifelinesList.remove('Call a Friend (Arrogant)')
                if random.randint(1,5) == 1:
                    suggestion = correctAnswer
                else:
                    wrongAnswersList = choicesList[:]
                    wrongAnswersList.remove(correctAnswer)
                    if len(wrongAnswersList) == 1:
                        suggestion = wrongAnswersList[0]
                    else:
                        suggestion = wrongAnswersList[random.randint(0,len(wrongAnswersList)-1)]                        
                text = '\nCalling (arrogant) friend...\n'
                typeWrite(text,1)
                wait(1)
                text = '"Hey ' + playerName + '! I can' + "'" + 't believe you needed help on this question. This one is so eeaaasy. The answer is ' + suggestion + '. Goodluck!"'
                typeWrite(text,2)
                instantUI = True
                newInstantText += '\nArrogant friend suggestion: ' + suggestion + '\n'
                wait(2)
                break
            if lifelinesList[int(answer)-1] == 'Fifty-fifty':
                fiftyFiftyUsed = True
                lifelinesList.remove('Fifty-fifty')        
                wrongAnswersList = choicesList[:]
                wrongAnswersList.remove(correctAnswer)
                removeThese = random.sample(range(3),2)
                choicesList.remove(wrongAnswersList[removeThese[0]])
                choicesList.remove(wrongAnswersList[removeThese[1]])
                text = '\nTwo random wrong answers have been removed.'
                typeWrite(text,1)
                instantUI = True
                newInstantText += '\nFifty-fifty was used this round.\n' 
                wait(2)
                break                                    
        else:
            text = '\nInvalid input. Which lifeline do you want to use? '
            typeWrite(text,1)    

def askAction():
    global instantText
    while 1:
        if instantUI == True:
            return True
        text = '\nActions:\n'
        for i in range(len(actionsList)):
            text += '(' + str(i+1) + ') ' + actionsList[i]
            if i != len(actionsList)-1:
                text += '\n'
        text += '\n\nWhat do you want to do? '
        typeWrite(text,1)            
        while 1:
            answer = input()
            if answer == '1' or answer == '2' or (answer == '3' and len(actionsList) == 3):
                if actionsList[int(answer)-1] == 'Answer the question':
                    askAndCheckAnswer()
                    break
                elif actionsList[int(answer)-1] == 'Use a lifeline':
                    useLifeline()
                    break
                elif actionsList[int(answer)-1] == 'Walk away with current earnings':
                    walkAway()
                    break
            else:
                text = '\nInvalid input. What do you want to do? '
                typeWrite(text,1)
        if instantUI == False:
            return False        

def displayUI():
    global actionsList, choicesString, instantText, instantUI
    while 1:
        os.system('cls')
        if instantUI == True:
            instantText = ''
        text = '\nROUND ' + str(currentRound) + ' - ' + roundDifficulty.upper()
        instantText += text
        if instantUI == False:
            typeWrite(text,.5)
            wait(1)
        text = '\n\nCurrent Earnings: ' + convertScore(str(currentEarnings))
        instantText += text
        if instantUI == False:       
            typeWrite(text,.5)
        text = '\nPrize: ' + convertScore(str(roundPrize))
        instantText += text
        if instantUI == False:
            typeWrite(text,.5)
        if currentRound != 15:
            text = '\nLifelines available: '
            if len(lifelinesList) != 0:
                for i in range(len(lifelinesList)):
                    text += lifelinesList[i]
                    if i < len(lifelinesList)-1:
                        text += ', '
            else:
                text += 'None'
            instantText += text    
            if instantUI == False:
                typeWrite(text,1)
        if instantUI == False:
            wait(1)        
        text = '\n\nQuestion: ' + questionContent +'\n\n'
        instantText += text
        if instantUI == False:
            typeWrite(text,1)
            wait(1)
        text = ''
        for i in range(len(choicesList)):
            text += '(' + convertChoice(str(i)) +') ' + choicesList[i] + '\n'
        choicesString = text
        instantText += text
        if instantUI == False: 
            typeWrite(text,1)
            wait(1)
        if instantUI == True:
            reloadUI()
        instantUI = False    
        if askAction() == False:
            break

def playGame():
    global currentEarnings, currentRound, gameOver, questionID, roundDifficulty, roundPrize
    playerLogin()
    currentRound = 0
    gameOver = False
    currentEarnings = 0
    while currentRound < 15 and gameOver == False:
        currentRound += 1
        roundDifficulty = setRoundDifficulty(currentRound)
        roundPrize = setRoundPrize(currentRound)
        questionID = getRandomQuestion(roundDifficulty)
        setContent()
        displayUI()

def viewHighScores():
    os.system('cls')
    text = '\nHigh Scores:\n\n'
    data = highScoresCursor.execute('SELECT Player, Score from HighScores ORDER BY Score DESC').fetchall()
    if (len(data) == 0):
        text += "And.... there's nothing here :/\n"
    else:
        for elem in data:
            text += str(elem[0]) + ': ' + convertScore(str(elem[1])) + '\n'
    typeWrite(text,2)
    wait(.75)
    text = '\n(a) Play Game\n(b) Quit\n\nWhat do you want to do? '
    typeWrite(text,1)
    while 1:
        choice = input()
        if choice == 'a' or choice == 'A':
            playGame()
            break
        elif choice == 'b' or choice == 'B':
            print('\n',end='')
            exitProgram()
        else:
            text = '\nInvalid input. What do you want to do? '
            typeWrite(text,1)

def mainMenu():
    text = '(a) Play Game\n(b) View High Scores\n(c) Quit\n\nWhat do you want to do? '
    typeWrite(text,1)
    while 1:
        choice = input()
        if choice == 'a' or choice == 'A':
            playGame()
            break
        elif choice == 'b' or choice == 'B':
            viewHighScores()
            break
        elif choice == 'c' or choice == 'C':
            print('',sep='')
            exitProgram()
        else:
            text = '\nInvalid input. What do you want to do? '
            typeWrite(text,1)

def gameStart():
    os.system('cls')
    text = '\nWelcome to Who Wants to be a Millionnaire!\n'
    typeWrite(text,1)
    animateCaps(text,.5)
    mainMenu()

def askPlayAgain():
    text = '\n(y/n) Do you want to play again? '
    typeWrite(text,1)
    while 1:
        answer = input()
        if answer == 'y' or answer == 'Y':
            return True
        elif answer == 'n' or answer == 'N':
            print('',end='')
            return False
        else:
            text = '\nInvalid input. (y/n) Do you want to play again? '
            typeWrite(text,1)

def startProgram():
    while 1:
        checkDB()
        prepareContentDB()
        prepareHighScoresDB()
        prepareLifelines()
        randomizeQuestions()
        gameStart()
        if gameOver == True:
            if askPlayAgain() == False:
                exitProgram()
    
startProgram()
exitProgram()

# list of functions and what they do, arranged alphabetically

# animateCaps(text,duration) = turn letters of text to caps over duration 
# askAction() = asks user if he wants to answer, use lifeline, or quit. returns True if instantUI == True and False if False
# askAndCheckAnswer() = ask for answer and check
# askPlayAgain() = asks the user if he wants to play again
# checkDB() = checks if content.db file exists, else returns an error message
# checkIfHighScore() = checks if player score made it to high scores
# convertChoice(str) = converts str to int equivalent or vice versa
# convertScore(text) = converts text to a string with dollar sign and spaces
# displayUI() = displays UI for current round
# exitProgram() = exits program after a message and a delay
# gameStart() = starts the game with welcome message
# getRandomQuestion(roundDifficulty) = returns a random questionID based on difficulty
# mainMenu() = displays main menu
# playerLogin() = asks for name and check for previous scores
# playGame() = starts the next round
# prepareContentDB() = prepares the database of questions, choices, and correct answers
# prepareHighScoresDB() = prepares the database of highscores
# prepareLifelines() = prepares the lifelines which can be used later in the game
# randomizeQuestions() = gets 15 random question-choice-answer from database
# reloadUI() = clears screen and prints instantText instantly
# setContent() = sets question content, choices, correct answer
# setRoundDifficulty(currentRound) = sets currentRoundDifficulty based on currentRound
# setRoundPrize(currentRound) = sets prize for this round
# startProgram() = starts program/game after all functions have been defined
# typeWrite(text, duration) = prints the text over duration with a typewriting animation
# updateHighScores() = adds player to high scores and delete 6th scores above
# useLifeline() = use a lifeline
# viewHighScores() = view high scores
# wait(duration) = waits duration seconds using time.sleep() 
# walkAway() = walk away with current earnings

