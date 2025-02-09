import random
import re

redEscape = "\33[31m"
yellowEscape = "\033[33m"
whiteEscape = "\033[0m"

possibleColumns = ["A","B","C","D","E","F","G"]
gameBoard = [[" " for i in range(7)] for j in range(6)]
div = "\n  +---+---+---+---+---+---+---+"

player = ""
computer = ""
turn = "r"

def printGameBoard():
    print("\n    A   B   C   D   E   F   G  ", end="")
    for i in range(6):
        print(div)
        print(i, "|", end="")
        for j in range(7):
            print(" " + gameBoard[i][j] + " |", end="")
    print(div)
    print("\n")

def selectTeams():
    print("\nWould you like to be RED or YELLOW? Note: RED starts")
    
    yPattern = "^(y|yellow)$"
    rPattern = "^(r|red)$"

    playerInput = input("")

    while(True): 
        global player
        global computer
           
        if re.match(yPattern, playerInput, re.IGNORECASE):
            player = "y"
            computer = "r"
            print("Team YELLOW selected")
            break
        elif re.match(rPattern, playerInput, re.IGNORECASE):
            player = "r"
            computer = "y"
            print("Team RED selected")
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
    
    #got to here (indexing problems)

    row = options[column]+4
    lastPlay = gameBoard[row][column]
    print(lastPlay)

    columnBound = 6
    rowBound = 5

    return False

def main():
    global turn
    global player
    global computer

    lastPlay = -1
    options = getTurnOptions()

    selectTeams()
    print("\nCan you outsmart the Computer... let's find out!")

    while conclusionTest(lastPlay, options) == False:
        
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
        
        options = getTurnOptions()  
        
    
    print("Game concluded.")

if __name__ == "__main__":
    main()

