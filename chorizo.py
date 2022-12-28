from tkinter import *
 
# declaration
size = 3 # max 100 (not racional)
xoMap = [["" for x in range(size)] for y in range(size)] 

# [0] = x or o, [1] = turn count, bool for victory checking
turn = ["x", 0, False]

# player score x:o
score = [0,0,0]

# Parse through board - disable buttons / reset board
def parseBoard(action):
    turn[1] = 0
    for row in range(size):
        for col in range(size):
            xoMap[row][col] = ""
    children = gui.winfo_children() # Get list of all children widgets of the `gui` object
    if action == "flush":
        for child in children:
            if child["text"] == "x" or child["text"] == "o" or child["text"] == "": 
                child["text"] = ""
                child["state"] = "normal"
                turn[0]  = "x" # player is always x 
    if action == "end":
        for child in children:
            child["state"] = "disabled"
            if child["text"] == "reset board":
                child["state"] = "normal"

# score handler
def round(who):
    if who == "x":
        score[0] = score[0] + 1
    if who == "o":
        score[1] = score[1] + 1
    if who == "tie":
        score[2] = score[2] + 1
    scoreboard["text"]=f"X - {score[0]} | O - {score[1]}\nTie - {score[2]}"
    turn[2] = 0   
    parseBoard("end")

# [1] == best [row,col] to make a move
def findBestMove(xORo, maximizer) :
    bestMove = [-1, -1]
    maximizer = False if maximizer == True else True
    maxVal = -1000 if maximizer == True else 1000
    valueList = []
    xORo = "x" if xORo == "o" else "o"
    for i in range(size) :
        for j in range(size) :
            if (xoMap[i][j] == "") :
                movesLeft = -1
                for x in xoMap:
                    for xx in x:
                        if xx == "":
                            movesLeft +=1
                xoMap[i][j] = xORo
                winCheck(i,j)
                if turn[2] == True and xORo == "o":
                    xoMap[i][j] = ""
                    turn[2] = False
                    moveVal = size*size+movesLeft
                elif turn[2] == True and xORo == "x":
                    xoMap[i][j] = ""
                    turn[2] = False
                    moveVal = -size*size-movesLeft
                elif movesLeft == 0:
                    xoMap[i][j] = ""
                    turn[2] = False
                    moveVal = 0
                else:
                    moveVal, move = findBestMove(xORo, maximizer)
                valueList.append(moveVal)
                xoMap[i][j] = ""
                if maximizer == True:
                    if moveVal > maxVal :
                        bestMove = [i,j]
                        maxVal = moveVal
                else:
                    if moveVal < maxVal :
                        bestMove = [i,j]
                        maxVal = moveVal
    return maxVal, bestMove

# machine move
def roboMove():
    children = gui.winfo_children()
    bestMove = findBestMove("x",False)[1]
    nr = bestMove[0]*size + bestMove[1]
    children[nr].invoke()

# xo switch and machine move initializer
def nextTurn():
    if turn[0] == "x":
        turn[0] = "o"
        if turn[1]%2 == 1:
            roboMove()
    elif turn[0] == "o":
        turn[0] = "x"
        if turn[1]%2 == 1:
            roboMove()

# Create object
gui = Tk()
gui.title("TicTacTwo")
# Adjust size
gui.geometry("500x500")
 
# Grid creator
for i in range(size):
    Grid.rowconfigure(gui,i,weight=1)
    Grid.columnconfigure(gui,i,weight=1)
Grid.rowconfigure(gui,size,weight=1) # ScoreBoard
Grid.rowconfigure(gui,size+1,weight=1) # Board reset

# Eqaul value checker
def lineCheck(x_row,x_col,y_row,y_col,z_row,z_col):
    negativeCheckList = [x_row,x_col,y_row,y_col,z_row,z_col]
    try:
        for x in negativeCheckList:
            if x < 0 or x >= size:
                raise("negative index start at the array end - bad for checking line")
        if xoMap[x_row][x_col] == xoMap[y_row][y_col] == xoMap[z_row][z_col]:
            turn[2] = True
    except:
        pass

# Possible win combination checker
def winCheck(row,col):
    # vertical
    lineCheck(row,col,row+1,col,row+2,col)
    lineCheck(row-1,col,row,col,row+1,col)
    lineCheck(row-2,col,row-1,col,row,col)
    # horizontal
    lineCheck(row,col,row,col+1,row,col+2)
    lineCheck(row,col-1,row,col,row,col+1)
    lineCheck(row,col-2,row,col-1,row,col)
    # \
    lineCheck(row,col,row+1,col+1,row+2,col+2)
    lineCheck(row-1,col-1,row,col,row+1,col+1)
    lineCheck(row-2,col-2,row-1,col-1,row,col)
    # /
    lineCheck(row+2,col-2,row+1,col-1,row,col)
    lineCheck(row+1,col-1,row,col,row-1,col+1)
    lineCheck(row,col,row-1,col+1,row-2,col+2)

# On button click action
def clickAction(button,row,col):
    turn[1] = turn[1] + 1
    button["text"] = turn[0]
    button["state"] = "disabled"
    button["disabledforeground"] = "red"
    xoMap[row][col] = turn[0]
    winCheck(row,col)
    if turn[2] == True:
        round(xoMap[row][col])
    elif turn[1] == size*size and turn[2] == False:
        round("tie")
    nextTurn()

# Button class
class buttonCreator:
    def __init__(self,row,col):
        button = Button(gui,bg='gray',activebackground='gray',command=lambda:clickAction(button,row,col))
        button.grid(row=row,column=col,sticky="NSEW")

# Button creator
for row in range(size):
    for col in range(size):
        buttonCreator(row,col)

# Create scoreboard label
scoreboard = Label(gui,disabledforeground="black",text=f"X - {score[0]} | O - {score[1]}\nTie - {score[2]}",font=("Arial", 16))

# Place scoreboard label at the end of the window
scoreboard.grid(row=size,columnspan=size,sticky="NSEW")

# Board manipulation button
reset = Button(gui,borderwidth=0,text="reset board",command=lambda:parseBoard("flush"))
reset.grid(row=size+1,columnspan=size,sticky="NSEW")

# Execute tkinter
gui.mainloop()
