from random import randint, randrange
from tkinter import Tk
import time
import tkinter

def generate_block(block:str)->tuple:
    #returns initial coordinates of the block based on its shape
    coordHash = {'l':((0,4),(0,5),(0,6),(1,4)),'t':((0,5),(0,4),(0,6),(1,5)),'j':((0,5),(0,6),(0,4),(1,6)),'o':((0,5),(0,6),(1,5),(1,6)),'s':((0,5),(0,6),(1,4),(1,5)),'z':((0,5),(0,4),(1,5),(1,6)),'i':((0,5),(0,4),(0,6),(0,7))}
    #the first tuple in the tuple will be the center of any rotation on the block
    return coordHash[block]
    
def rotate_block(oldCoords:tuple)->tuple:
    #returns the inteded coordinates after rotation without testing for space availibility
    newCoords = []
    top, left = oldCoords[0][0], oldCoords[0][1]
    for square in oldCoords:
        newCoords.append(
            ( left - square[1] + top, square[0] + left - top)
        )
    return tuple(newCoords)

'''def move_block(oldCoords:tuple,direction:str)->tuple:
    #returns the inteded coordinates after movement without testing for space availibility
    dirHash = {'a':(0,-1),'s':(1,0),'d':(0,1)}
    direction = dirHash[direction] #transforms direction string into a vector of magnitude 1
    newCoords = []
    for square in oldCoords:
        newCoords.append(
            (square[0]+direction[0],square[1]+direction[1])
        )
    return newCoords'''

def move_block(oldCoords:tuple,direction:str)->tuple:
    #returns the intended coordinates after movement without testing for space availability
    if direction == 'a':
        return ((i[0],i[1]-1)for i in oldCoords)
    if direction == 's':
        return ((i[0]+1,i[1])for i in oldCoords)
    if direction == 'd':
        return ((i[0],i[1]+1)for i in oldCoords)
    

def lose_game():
    pass

def change_block(coords:tuple, matrix:list, value:int):
    for coord in (coords):
        matrix[coord[0]][coord[1]-1] = value
    return matrix
    

def play_tetris():
    #initiates and runs tetris
    global matrix
    matrix = [[0]*10 for i in range(21)]
    gaming = True
    possibleBlocks = ('l','t','j','o','s','z','i')
    global controlledBlock
    controlledBlock = None
    root = Tk()
    iterate = 0
    scale = 30 
    C = tkinter.Canvas(root, bg = 'white', height = 20*scale, width = 10*scale)

    def key_pressed(key):
        global matrix
        global controlledBlock

        if controlledBlock == None or key.char not in ['w','a','s','d']: return

        if key.char == 'w':
            tempBlock = rotate_block(controlledBlock)
        if key.char in ['a','s','d']:
            tempBlock = move_block(controlledBlock, key.char)

        for i in tempBlock:    
            if not (i[0] <= 21 and 0 <= i[1] <= 10):
                return
            if matrix[i[0]][i[1]] != 0 and not (i in controlledBlock):
                controlledBlock = None
                print(i)
                return

        matrix = change_block(controlledBlock,matrix,0)
        controlledBlock = tempBlock
        matrix = change_block(controlledBlock,matrix,1)
        
        

    root.bind('<Key>', key_pressed)

    while gaming:
        root.update_idletasks()
        root.update()  
        if controlledBlock == None:
            if 1 in matrix[0][3:7]+matrix[1][3:7] :
                lose_game()
                gaming = False
            else:
                nextBlock = possibleBlocks[randint(0,6)]
                controlledBlock = generate_block(nextBlock)
                matrix = change_block(controlledBlock, matrix, 1)



        if iterate % 10 == 0:
            time.sleep(0.5)                
            print(iterate)
            #simulates the downward keypress
            tempBlock = move_block(controlledBlock, "s")

            for i in tempBlock:
                if not (0 <= i[0] < 20) :
                    controlledBlock = None
                    break
                if (i not in controlledBlock) and matrix[i[0]][i[1]] != 0:
                    controlledBlock = None
                    break
            if controlledBlock != None:
                matrix = change_block(controlledBlock,matrix,0)
                controlledBlock = tempBlock
                matrix = change_block(controlledBlock,matrix,1)

        
        C.delete("all")
        for i in range(20):
            for j in range(10):
                if matrix[i][j] != 0:
                    idec, jdec = i*scale, j*scale
                    C.create_polygon(jdec, idec, jdec+scale, idec, jdec+scale, idec+scale, jdec, idec+scale, fill = "blue")
        C.pack()

        iterate += 1 
                    
        if iterate >= 1000:
            gaming = False

            
if __name__ == "__main__":
    play_tetris()
    