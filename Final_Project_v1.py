import time
import sys

def viewHighScores(): # unfinished
    pass

def mainMenu():
    while 1:
        text = 'What do you want to do? '
        for i in text:
            print(i, end='', flush=True)
            time.sleep(1/len(text))
        answer = input()
        if answer == 'A' or answer == 'a':
            # proceed to play game
            return False
        if answer == 'B' or answer == 'b':
            viewHighScores()
            break
        if answer == 'C' or answer == 'c':
            # quit
            text = 'Exiting...'
            for i in text:
                print(i, end='', flush=True)
                time.sleep(.5/len(text))
            time.sleep(1)
            sys.exit()
        text = '\nInvalid input. '
        for i in text:
            print(i, end='', flush=True)
            time.sleep(.5/len(text))

# Initialization

print('\n')
text = '>welcome message<\n\n(a) Play Game\n(b) View High Scores\n(c) Quit'
for i in text:
    print(i, end='', flush=True)
    time.sleep(2/len(text))
print('\n')

# Main Menu
while 1:
    again = mainMenu()
    if again == False:
        break

print('end of code reached') # debug