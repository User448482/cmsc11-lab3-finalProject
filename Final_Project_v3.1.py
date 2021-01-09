import random
import sqlite3
import sys
import time

# declaring global variables
roundDifficulty = ''
question = ''
currentRound = 0 
playerName = ''
currentEarnings = 0
lifelineCallSmartFriendUsed = False
lifelineCallUnsureFriendUsed = False
lifelineCallArrogantFriendUsed = False
lifelineFiftyFiftyUsed = False
questionBankEasyList = []
questionBankAverageList = []
questionBankDifficultList = []
questionBankEasy = ()
questionBankAverage = ()
questionBankDifficult = ()
choicesBank = {}
db = ''
cursor = ''
lifelineEnabled = True
lifelinesList = ()
data = []
returningPlayer = False
correctAnswer = ''
remainingChoices = []
prize = 0
proceedToNextRound = True
playAgain = False

def animate(text,duration):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(duration/len(text))

def updateHighScores():
    global cursor, db
    data = cursor.execute('SELECT Player, Score FROM HighScores ORDER BY Score DESC').fetchall()
    dataList = [list(elem) for elem in data]
    # count distinct Scores if there are 2 or more records
    if len(dataList) > 1:
        counter = 1
        for i in range(len(dataList)-1):
            if dataList[i+1][1] != dataList[i][1]:
                counter += 1
            if counter > 5:
                excess = len(dataList) - i - 1
                for j in range(excess): # delete excess
                    cursor.execute('DELETE from HighScores WHERE Player = (?)', (dataList[j+5][0],))
                    db.commit()

def viewHighScores():
    global cursor
    updateHighScores()
    data = cursor.execute('SELECT Player, Score FROM HighScores ORDER BY Score DESC').fetchall()
    text = '\nTop 5 Scores: \n'
    animate(text,.5)
    for i in range(len(data)):
        text = data[i][0] + ' ' + str(data[i][1])
        animate(text,.5)
        print('')
    print('') 

def roundPrize(round):
    if round == 1:
        prize = 1000
    if round == 2:
        prize = 3000
    if round == 3:
        prize = 5000
    if round == 4:
        prize = 10000
    if round == 5:
        prize = 20000
    if round == 6:
        prize = 35000
    if round == 7:
        prize = 50000
    if round == 8:
        prize = 70000
    if round == 9:
        prize = 100000
    if round == 10:
        prize = 150000
    if round == 11:
        prize = 250000
    if round == 12:
        prize = 400000
    if round == 13:
        prize = 600000
    if round == 14:
        prize = 1000000                                                        
    if round == 15:
        prize = 2000000 
    return prize

def playerCreation():
    global playerName, returningPlayer
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
    data = cursor.execute('SELECT Player, Score FROM HighScores GROUP BY Player').fetchall()
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
    nextRound()

def quitGame():
    cursor.close()
    sys.exit()

def endGame(manner):
    global currentEarnings, currentRound, cursor, playerName, db, returningPlayer, proceedToNextRound, playAgain
    if manner == 'quit':
        proceedToNextRound = False
        text = 'You walk away with ' + str(currentEarnings) + '. Congratulations!'
        animate(text,1)
    if manner == 'mistake':
        text = '\nYour answer is incorrect.'
        if currentRound < 5:
            currentEarnings = 0
            text += '\nYou did not make it to the first safe haven (Round 5). You walk away with 0. Better luck next time!'
        if currentRound >= 5 and currentRound < 10:
            currentEarnings = 20000
            text += '\nYou have made it past the first safe haven (Round 5). You walk away with 20,000. Congratulations!'
        if currentRound >= 10:
            currentEarnings = 150000
            text += '\nYou have made it past the second safe haven (Round 10). You walk away with 150,000. Congratulations!'
        animate(text,2)
    if manner == 'winner':
        text = '\nYou have answered every question correctly. Congratulations on winning the game!'
    selectTable = 'SELECT Player, Score FROM HighScores ORDER BY Score DESC'
    data = cursor.execute(selectTable).fetchall()
    if len(data) != 0:
        lowest = data[len(data)-1][1]
    else:
        lowest = 0
    if currentEarnings < lowest:
        text ='\n\nYou did not make it to high scores. Score atleast ' + str(lowest) + ' to be included. Thanks for playing!\n\n'
        animate(text,1)
    if currentEarnings >= lowest:
        cursor.execute('SELECT * FROM HighScores')
        if returningPlayer == True:
            cursor.execute('UPDATE HighScores SET Score = (?) WHERE Player = (?)', (currentEarnings, playerName) )
            text = '\n\nYour high score has been updated! Congratulations!\n'
        elif returningPlayer == False:
            cursor.execute('INSERT INTO HighScores (Player, Score) VALUES (?,?)', (playerName, currentEarnings))
            text ='\n\nYou have made it to high scores! Congratulations!\n'
        db.commit()
        animate(text,1)
        viewHighScores()
    text = '\nThe game has ended.\n'
    while 1:
        text = 'Do you want to play again? (Y/N)\nYour answer: '
        animate(text,1)
        answer = input()
        if answer == 'Y' or answer == 'y':
            playAgain = True
            break
        elif answer == 'N' or answer == 'n':
            playAgain == False
            text = '\nExiting...\n\n'
            animate(text,1)
            time.sleep(.7)
            quitGame()
        else:
            text = 'Invalid input.'

def answerAndCheck():
    global remainingChoices, proceedToNextRound, currentEarnings
    while 1:
        text = '\nWhat is the letter of your answer? '
        animate(text,1)
        answer = input()
        if answer == 'A' or answer == 'a':
            answer = remainingChoices[0]
            break
        elif answer == 'B' or answer == 'b':
            answer = remainingChoices[1]
            break            
        elif (answer == 'C' or answer == 'c') and len(remainingChoices) == 4:
            answer = remainingChoices[2]
            break            
        elif (answer == 'D' or answer == 'd') and len(remainingChoices) == 4:
            answer = remainingChoices[3]
            break            
        else:
            text = '\nInvalid input.'
            animate(text,.5)
    if answer == correctAnswer:
        proceedToNextRound = True
        currentEarnings += prize
        text = '\nYour answer is correct. You won ' + str(prize) + '. Congratulations!\n\n'
        animate(text,1)       
        if currentRound == 15:
            endGame('winner') 
    if answer != correctAnswer:
        proceedToNextRound = False
        endGame('mistake')

def askForAction():
    text = '\n\nActions:\n(1) Answer the question\n'
    if currentRound != 15 and len(lifelinesList) != 0:
        text += '(2) Use a lifeline\n(3) Walk away with current earnings\n\n'
        actionTwo = 'lifeline'
    else:
        text += '(2) Walk away with current earnings\n\n'
        actionTwo = 'quit'
    animate(text,1)
    if len(lifelinesList) != 0 and roundDifficulty == 'difficult' and currentRound != 15:
        text = '\n\nReminder: Lifelines cannot be used on the final question.\n'
        animate(text,.5)           
    if len(lifelinesList) != 0 and currentRound == 15:
        text = '\n\nNote: Lifelines cannot be used on the final question.\n'
        animate(text,.5)
    while 1:
        text = 'What do you want to do? '
        animate(text,.5) 
        action = str(input())
        if action == '1':
            answerAndCheck()
            break
        elif action == '2' and actionTwo == 'lifeline':
            useLifeline()
            break
        elif action == '3' or (action == '2' and actionTwo == 'quit'):
            endGame('quit')
            break
        else:
            text = 'Invalid input. '
            animate(text,.5)

def useLifeline():
    global lifelinesList, lifelineCallSmartFriendUsed, lifelineCallUnsureFriendUsed, lifelineCallArrogantFriendUsed, lifelineFiftyFiftyUsed
    text = '\nLifelines available:\n'
    animate(text,1)
    choicesAvailable = []
    for i in range(len(lifelinesList)):
        choicesAvailable.append(i+1)
        text = '(' + str((i + 1)) + ') ' + lifelinesList[i]
        animate(text,.5)
        print('')
    text = '\nWhich lifeline do you want to use? '
    animate(text,.5)        
    while 1:
        answer = int(input())
        if (answer in choicesAvailable) == True:
            if lifelinesList[answer-1] == 'Call a Friend (Smart)':
                lifelineCallSmartFriendUsed = True
                lifelinesList.remove('Call a Friend (Smart)')
                if random.randint(1,10) <= 9:
                    suggestion = correctAnswer
                else:
                    wrongAnswers = remainingChoices[:]
                    wrongAnswers.remove(correctAnswer)
                    if len(wrongAnswers) == 1:
                        suggestion = wrongAnswers[0]
                    else:
                        suggestion = wrongAnswers[random.randint(0,len(wrongAnswers)-1)]
                text = 'Lifeline Call a Friend(Smart) used! Calling smart friend...'
                animate(text,.5)
                time.sleep(1)
                text = '\n\n"Hi ' + playerName + '! Thanks for calling me. I' + "'" + 'm pretty sure the answer is ' + suggestion + '. Goodluck!"'
                animate(text,1)
                time.sleep(1)
                break
            if lifelinesList[answer-1] == 'Call a Friend (Unsure)':
                lifelineCallUnsureFriendUsed = True
                lifelinesList.remove('Call a Friend (Unsure)') 
                if random.randint(1,2) == 1:
                    suggestion = correctAnswer
                else:
                    wrongAnswers = remainingChoices[:]
                    wrongAnswers.remove(correctAnswer)
                    if len(wrongAnswers) == 1:
                        suggestion = wrongAnswers[0]
                    else:
                        suggestion = wrongAnswers[random.randint(0,len(wrongAnswers)-1)]
                text = 'Lifeline Call a Friend(Unsure) used! Calling unsure friend...'
                animate(text,.5)
                time.sleep(1)
                text = '\n\n"Hello ' + playerName + '! I appreciate your call but I' + "'" + 'm not sure on this one. But if I were to guess, the answer is ' + suggestion + '. Goodluck!"'
                animate(text,1)
                time.sleep(1)
                break
            if lifelinesList[answer-1] == 'Call a Friend (Arrogant)':
                lifelineCallArrogantFriendUsed = True
                lifelinesList.remove('Call a Friend (Arrogant)') 
                if random.randint(1,5) == 1:
                    suggestion = correctAnswer
                else:
                    wrongAnswers = remainingChoices[:]
                    wrongAnswers.remove(correctAnswer)
                    if len(wrongAnswers) == 1:
                        suggestion = wrongAnswers[0]
                    else:
                        suggestion = wrongAnswers[random.randint(0,len(wrongAnswers)-1)]
                text = 'Lifeline Call a Friend(Arrogant) used! Calling an arrogant friend...'
                animate(text,.5)
                time.sleep(1)
                text = '\n\n"Hey ' + playerName + '! I can' + "'" + 't believe you needed help on this question. This one is so eeaaasy. The answer is ' + suggestion + '. Goodluck!"'
                animate(text,1)
                time.sleep(1)
                break
            if lifelinesList[answer-1] == 'Fifty-fifty':  
                lifelineFiftyFiftyUsed = True         
                lifelinesList.remove('Fifty-fifty')
                wrongAnswers = remainingChoices[:]
                wrongAnswers.remove(correctAnswer)
                removeThese = random.sample(range(3),2)
                remainingChoices.remove(wrongAnswers[removeThese[0]])
                remainingChoices.remove(wrongAnswers[removeThese[1]])
                text = 'Fifty-fifty used. Two random incorrect answers were removed.\n\nRemaining choices:\n'
                for i in range(len(remainingChoices)):
                    if i == 0:
                        text += '(a) '
                    if i == 1:
                        text += '(b) '
                    if i == 2:
                        text += '(c) '
                    if i == 3:
                        text += '(d) '
                    text += remainingChoices[i]
                    if i <= len(remainingChoices) - 2:
                        text += '\n'
                animate(text,1.5)
                time.sleep(1)
                break
        else:
            text = 'Invalid input. Input the number inside () before the choice: '
            animate(text,.5)
    askForAction()

def nextRound():
    global roundDifficulty, question, currentRound, lifelineEnabled, currentEarnings, remainingChoices, prize, correctAnswer
    while 1:
        currentRound += 1
        if currentRound <= 5:
            roundDifficulty = 'easy'
            question = questionBankEasyList[currentRound-1]
            correctAnswer = questionBankEasy[question]['answer']
            content = questionBankEasy[question]['content']
        if currentRound > 5 and currentRound <= 10:
            roundDifficulty = 'average'
            question = questionBankAverageList[currentRound-6]
            correctAnswer = questionBankAverage[question]['answer']                
            content = questionBankAverage[question]['content']            
        if currentRound > 10:
            roundDifficulty = 'difficult'
            question = questionBankDifficultList[currentRound-11]
            correctAnswer = questionBankDifficult[question]['answer']            
            content = questionBankDifficult[question]['content']            
        remainingChoices = list(choicesBank[question])
        random.shuffle(remainingChoices)
        prize = roundPrize(currentRound)
        if currentRound != 15:
            lifelineEnabled = True
        else:
            lifelineEnabled = False
        text = 'ROUND ' + str(currentRound) + '\n' + 'Current Earnings: ' + str(currentEarnings) + '\n' + 'Prize for this Round: ' + str(prize)
        animate(text,1.5)
        if lifelineEnabled == True:
            text = '\nLifelines remaining: '
            for element in range(len(lifelinesList)):
                text += lifelinesList[element]
                if element != len(lifelinesList)-1:
                    text += ', '
            if len(lifelinesList) == 0:
                text += 'None'
            animate(text,1)
        text = '\n\nQuestion: ' + content
        animate(text,1.5)
        text = '\n\n'
        for i in range(len(remainingChoices)):
            if i == 0:
                text += '(a) '
            if i == 1:
                text += '(b) '
            if i == 2:
                text += '(c) '
            if i == 3:
                text += '(d) '
            text += remainingChoices[i]
            if i <= len(remainingChoices) - 2:
                text += '\n'
        animate(text,1.5)
        askForAction()
        if proceedToNextRound == False:
            break
        if currentRound == 15:
            break                                  

def gameStart():
    global playerName, currentEarnings, currentRound, lifelineCallSmartFriendUsed, lifelineCallUnsureFriendUsed, lifelineCallArrogantFriendUsed, lifelineFiftyFiftyUsed
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
            quitGame()            
            break
        else:
            text = '\nInvalid input.\n\n'
            animate(text,.5)
            time.sleep(.5)

def prepareRandomQuestions():
    global questionBankEasyList, questionBankAverageList, questionBankDifficultList
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

def initializeHighScoresDB():
    global db, cursor
    db = sqlite3.connect('highscores.db')
    cursor = db.cursor()
    createTable = 'CREATE TABLE IF NOT EXISTS HighScores (Player VARCHAR NOT NULL, Score INTEGER NOT NULL)'
    cursor.execute(createTable)

def initializeQuestionBanks():
    global questionBankEasy, questionBankAverage, questionBankDifficult, choicesBank
    questionBankEasy = {
        'e01': { 'content': 'How is 4:00 p.m. expressed in military time?',                             'answer': '16:00' },
        'e02': { 'content': 'Cancer is the disease of what?',                                           'answer': 'Cells' },
        'e03': { 'content': 'What product does Tesla produce?',                                         'answer': 'electric cars' },
        'e04': { 'content': 'What city is the first capital city in the Philippines?',                  'answer': 'Cebu' },
        'e05': { 'content': 'What does the word "loquacious" mean?',                                    'answer': 'chatty' },
        'e06': { 'content': 'Which country discovered the first fireworks?',                            'answer': 'China' },
        'e07': { 'content': 'Which of these is not a breed of a feline?',                               'answer': 'Bichon Frise' },
        'e08': { 'content': 'What is the national animal of Australia?',                                'answer': 'kangaroo' },
        'e09': { 'content': 'How many years is an official term of the US Senate?',                     'answer': '6' },
        'e10': { 'content': 'What is the approximate number of islands that comprise the Philippines?', 'answer': '7500' }                                                                                                                                                                                                      
    }

    questionBankAverage = {
        'a01': { 'content': 'Obstetrics is a branch of medicine particularly concerned with what?',                                 'answer': 'childbirth' },
        'a02': { 'content': 'The dance known as the "fandango" is of what origin?',                                                 'answer': 'Spain' },
        'a03': { 'content': 'How many stars are on the American flag?',                                                             'answer': '50' },
        'a04': { 'content': 'What animal represents the year 1999 on the Chinese Calendar?',                                        'answer': 'rabbit' },
        'a05': { 'content': 'What is considered the proper way to address a duke?',                                                 'answer': 'Your Grace' },
        'a06': { 'content': 'Which of these birds has the biggest brain relative to its size?',                                     'answer': 'Hummingbird' },
        'a07': { 'content': 'The Statue of Liberty was originally supposed to function as what?',                                   'answer': 'A lighthouse' },
        'a08': { 'content': 'Which of these religious observances lasts for the shortest period of time during the calendar year?', 'answer': 'Diwali' },
        'a09': { 'content': 'According to Albert Einstein, what is the "hardest thing in the world to understand"?',                'answer': 'Income Taxes' },
        'a10': { 'content': 'What does the Yiddish word "meshuga" mean?',                                                           'answer': 'crazy' }                                                                                                                                                                    
    }

    questionBankDifficult = {
        'd01': { 'content': 'What sort of a treat did the very first vending machine dispense?',                                                    'answer': 'holy water' },
        'd02': { 'content': 'Which of these daunting nicknames is given to the mountain K2?',                                                       'answer': 'Savage Mountain' },
        'd03': { 'content': 'The Incas were the first to domesticate which of these animals?',                                                      'answer': 'guinea pig' },
        'd04': { 'content': 'Which king was married to Eleanor of Aquitaine?',                                                                      'answer': 'Henry II' },
        'd05': { 'content': 'Oberon is the satellite of which planet?',                                                                             'answer': 'Uranus' },
        'd06': { 'content': 'In 1718, which pirate died in battle off the coast of what is now North Carolina?',                                    'answer': 'Blackbeard' },
        'd07': { 'content': 'Before the American colonies switched to the Gregorian calendar, on what date did their new year start?',              'answer': 'March 25' },
        'd08': { 'content': 'Which of the following pieces of currency was the first to use the motto "In God We Trust"?',                          'answer': 'Two-cent piece' },
        'd09': { 'content': 'Playwright Anton Chekhov graduated from the University of Moscow with a degree in what?',                              'answer': 'Medicine' },
        'd10': { 'content': 'Who is the only British politician to have held all four “Great Offices of State” at some point during their career?', 'answer': 'James Callaghan' }                                                                                                                                                                    
    }

    choicesBank = {

        #easy
        'e01': ( '04:00', '08:00', '16:00', '18:00' ),
        'e02': ( 'Brain', 'Lungs', 'Cells', 'Heart' ),
        'e03': ( 'ice cream', 'televisions', 'hair brushes', 'electric cars' ),
        'e04': ( 'Manila', 'Cavite', 'Davao', 'Cebu' ),
        'e05': ( 'chatty', 'angry', 'beautiful', 'shy' ),
        'e06': ( 'Russia', 'Indonesia', 'Switzerland', 'China'),
        'e07': ( 'Norweigan Forest', 'Maine Coon', 'Sphinx', 'Bichon Frise' ),
        'e08': ( 'horse', 'kangaroo', 'dolphin', 'lion' ),
        'e09': ( '4', '6', '7', '8' ),
        'e10': ( '6500', '7500', '8500', '9500' ),

        #average
        'a01': ( 'childbirth', 'broken bones', 'heart conditions', 'old age'),
        'a02': ( 'France', 'Argentina', 'Spain', 'Italy'),
        'a03': ( '40', '45', '50', '55' ),
        'a04': ( 'rabbit', 'pig', 'dragon', 'snake' ),
        'a05': ( 'Your Grace', 'Your Highness', 'Your Royalty', 'Your Majesty' ),
        'a06': ( 'Ostrich', 'Sparrow', 'Hummingbird', 'Eagle' ),
        'a07': ( 'A port of entry', 'A bordermaker', 'A giftshop', 'A lighthouse' ),
        'a08': ( 'Ramadan', 'Diwali', 'Lent', 'Hanukkah' ),
        'a09': ( 'Astronomy', 'Income Taxes', 'Physics', 'Sewing' ),
        'a10': ( 'memorable', 'greedy', 'intelligent', 'crazy' ),

        #difficult
        'd01': ( 'holy water', 'soda', 'sanitary napkins', 'duckfeed' ),
        'd02': ( 'Twin Peaks', 'Old Rocky', 'Mount Impossible', 'Savage Mountain' ),
        'd03': ( 'cat', 'goat', 'chicken', 'guinea pig' ),
        'd04': ( 'Henry I', 'Henry II', 'Richard I', 'Henry V' ),
        'd05': ( 'Mercury', 'Neptune', 'Uranus', 'Mars' ),
        'd06': ( 'Calico Jack', 'Blackbeard', 'Bartholomew Roberts', 'Captain Kidd' ),
        'd07': ( 'March 25', 'July 1', 'September 25', 'December 1' ),
        'd08': ( 'Nickel', 'One dollar bill', 'Two-cent piece', 'Five dollar bill' ),
        'd09': ( 'Law', 'Medicine', 'Philosophy', 'Economics' ),
        'd10': ( 'David Lloyd George', 'Harold Wilson', 'James Callaghan', 'John Major' ) 
    
    }

def initializeLifelines():
    global lifelinesList
    lifelinesList = ['Call a Friend (Smart)', 'Call a Friend (Unsure)', 'Call a Friend (Arrogant)', 'Fifty-fifty']

def verifyIfCorrectAnswersInChoices(): # for debugging
    for i in questionBankEasy:
        if (questionBankEasy[i]['answer'] in choicesBank[i]) == True:
            print(i,'checked')
        else:
            print(i,'error')
    for i in questionBankAverage:
        if (questionBankAverage[i]['answer'] in choicesBank[i]) == True:
            print(i,'checked')
        else:
            print(i,'error')
    for i in questionBankDifficult:
        if (questionBankDifficult[i]['answer'] in choicesBank[i]) == True:
            print(i,'checked')
        else:
            print(i,'error')

while 1:
    initializeQuestionBanks()
    initializeHighScoresDB()
    initializeLifelines()
    #verifyIfCorrectAnswersInChoices() # enable this if you want to verify if correct answers are in choices
    programStart()
    mainMenu()
    if playAgain == False:
        break
quitGame()