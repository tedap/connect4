import random
import re

redEscape = "\33[31m"
yellowEscape = "\033[33m"
whiteEscape = "\033[0m"
greyEscape = "\033[38;5;245m"

possibleColumns = ["A","B","C","D","E","F","G"]
gameBoard = [[" " for i in range(7)] for j in range(6)]
div = greyEscape + "\n  +---+---+---+---+---+---+---+" + whiteEscape

player = ""
computer = ""
turn = "r"

victor = None

def printGameBoard():
    print(whiteEscape + "\n    A   B   C   D   E   F   G  " + whiteEscape, end="")
    for i in range(6):
        print(div)
        print(greyEscape + "  |" + whiteEscape, end="")
        for j in range(7):
            print(" " + gameBoard[i][j] + greyEscape + " |" + whiteEscape, end="")
    print(div)
    print("\n")

def selectTeams():
    print("\nWould you like to be " + redEscape + "RED" + whiteEscape + " or " + yellowEscape + "YELLOW" + whiteEscape + "? Note: " + redEscape + "RED " + whiteEscape + "starts")
    
    yPattern = "^(y|yellow)$"
    rPattern = "^(r|red)$"

    playerInput = input("")

    while(True): 
        global player
        global computer
           
        if re.match(yPattern, playerInput, re.IGNORECASE):
            player = "y"
            computer = "r"
            print("Team" + yellowEscape + "YELLOW" + whiteEscape + " selected")
            break
        elif re.match(rPattern, playerInput, re.IGNORECASE):
            player = "r"
            computer = "y"
            print("Team " + redEscape + "RED" + whiteEscape + " selected")
            break
        else:
            print("Hmmm... I don't think that team exists")
            playerInput = input("")

def getTurnOptions():
    options = [-1] * 7
    for column in range(7):
        for row in range(6):
            if gameBoard[5-row][column] == " ":
                options[column] = row
                break
    
    #print(options)
    return options

def getColumnOptions(options):
    ColumnOptions = []
    for i in range(7):
        if options[i] != -1:
            ColumnOptions.append(possibleColumns[i])
    return(ColumnOptions)        

def computerChoice(options):
    randColumn = random.randint(0, 6)
    while options[randColumn] == -1:
        randColumn = random.randint(0, 6)    
    return randColumn


def makePlay(column, team, options):
    global gameBoard
    
    if team == "r":
        gameBoard[5-options[column]][column] = redEscape + "O" + whiteEscape
    else:
        gameBoard[5-options[column]][column] = yellowEscape + "O" + whiteEscape


def conclusionTest(column, options):
    columnBound = 6
    rowBound = 5

    row = 5-options[column]
    lastPlay = gameBoard[row][column]

    #print(lastPlay)
    lengths = [0, 0, 0, 0]
    
    #check vertical
    for i in range(0, 4):
        tmpRow = row + i
        if tmpRow <= rowBound:
            if lastPlay == gameBoard[tmpRow][column]:
                lengths[0] += 1
            else:
                lengths[0] = 0
        if lengths[0] == 4:
            #print("vertical")
            return False

    #check horizontal
    for j in range(-3, 4):
        tmpColumn = column + j
        if (tmpColumn <= columnBound) and (tmpColumn >= 0):
            if lastPlay == gameBoard[row][tmpColumn]:
                lengths[1] += 1
            else:
                lengths[1] = 0
        if lengths[1] == 4:
            #print("horizontal")
            return False
    
    #check positive diagonal
    for i, j in zip(range(-3, 4), range(3, -4, -1)):
        tmpRow = row + i
        tmpColumn = column + j
        if(tmpColumn <= columnBound) and (tmpColumn >= 0) and (tmpRow <= rowBound) and (tmpRow >= 0):
            if lastPlay == gameBoard[tmpRow][tmpColumn]:
                lengths[2] += 1
            else:
                lengths[2] = 0
        if lengths[2] == 4:
            #print("pos diag")
            return False

    #check negative diagonal
    for i, j in zip(range(-3, 4), range(-3, 4)):
        tmpRow = row + i
        tmpColumn = column + j
        if(tmpColumn <= columnBound) and (tmpColumn >= 0) and (tmpRow <= rowBound) and (tmpRow >= 0):
            if lastPlay == gameBoard[tmpRow][tmpColumn]:
                lengths[3] += 1
            else:
                lengths[3] = 0
        if lengths[3] == 4:
            #print("neg diag")
            return False

    return True

def main():
    global turn
    global player
    global computer

    notEnded = True
    lastPlay = -1
    options = getTurnOptions()

    selectTeams()
    print("\nCan you outsmart the Computer... let's find out!")


    while notEnded:
        options = getTurnOptions()  

        if all(x == -1 for x in options):
            print("It's a Draw!!!\n")
            break

        elif turn == computer:
            print("Computer's turn")
            computerPlay = computerChoice(options)
            makePlay(computerPlay, computer, options)

            lastPlay = computerPlay
            turn = player       

        else:
            columnOptions = getColumnOptions(options)
            print("\nYour turn... make your choice!")
            printGameBoard()
            playerChoice = input("Choose column: ")

            while not(playerChoice.casefold() in [column.casefold() for column in columnOptions]):
                print("\nInvalid choice, sorry!")
                printGameBoard()
                playerChoice = input("Try another column: ")
            
            playerPlay = possibleColumns.index(playerChoice.upper())
            makePlay(playerPlay, player, options)
            printGameBoard()

            lastPlay = playerPlay
            turn = computer
        
        notEnded = conclusionTest(lastPlay, options)

    printGameBoard()

    if notEnded == False:
        if turn == computer:
            if player == "r":
                print(redEscape + "Red Team Wins. Congratulations!" + whiteEscape)
            else:
                print(yellowEscape + "Yellow Team Wins. Congratulations!" + whiteEscape)    
        else:
            if computer == "r":
                print(redEscape + "Red Team Wins. Unlucky :(" + whiteEscape)
            else:
                print(yellowEscape + "Yellow Team Wins. Unlucky :(" + whiteEscape)                


if __name__ == "__main__":
    main()

