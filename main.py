#!/usr/bin/python3
import pygame, random, sys
from pygame.locals import *

GAMESPEED = 5 # 1-10 higher number for faster speed
FPS = 30

WINDOWWIDTH = 480
WINDOWHEIGHT = 640
GAMEWIDTH = 220
GAMEHEIGHT = 550

BOXSIZE = 20
BOXMARGIN = 2
BOXMOVESTEP = BOXSIZE + BOXMARGIN

XBOXCOUNT = int(GAMEWIDTH / BOXMOVESTEP)
YBOXCOUNT = int(GAMEHEIGHT / BOXMOVESTEP)

# print("XBOXCOUNT=", XBOXCOUNT)
# print("YBOXCOUNT=",YBOXCOUNT)

LEFTBORDER = 40 # fixed width
RIGHTBORDER = WINDOWWIDTH - GAMEWIDTH - LEFTBORDER
TOPBORDER = int((WINDOWHEIGHT - GAMEHEIGHT) / 2)
BOTTOMBORDER = int((WINDOWHEIGHT - GAMEHEIGHT) / 2) - BOXMARGIN

GAMECAPTION = 'Tetris'

DEFAULTXPOS = LEFTBORDER + BOXMARGIN
DEFAULTYPOS = (TOPBORDER + BOXMARGIN) - 2 * BOXMOVESTEP

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
ROTATE = 'rotate'

BGCOLOR = (255, 255, 255)
DARKGRAY = (200, 200, 200)
BOXCOLOR = (0, 0, 0)

# default
I = [[0, 1, 0, 0],[0, 1, 0, 0],[0, 1, 0, 0],[0, 1, 0, 0]]
O = [[1, 1, 0, 0],[1, 1, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
L = [[0, 1, 0, 0],[0, 1, 0, 0],[1, 1, 0, 0],[0, 0, 0, 0]]
J = [[1, 1, 0, 0],[0, 1, 0, 0],[0, 1, 0, 0],[0, 0, 0, 0]]
Z = [[1, 0, 0, 0],[1, 1, 0, 0],[0, 1, 0, 0],[0, 0, 0, 0]]
S = [[0, 1, 0, 0],[1, 1, 0, 0],[1, 0, 0, 0],[0, 0, 0, 0]]
T = [[0, 1, 0, 0],[0, 1, 1, 0],[0, 1, 0, 0],[0, 0, 0, 0]]

# first rotation @90 deg
I2 = [[0, 0, 0, 0],[1, 1, 1, 1],[0, 0, 0, 0],[0, 0, 0, 0]]
L2 = [[1, 0, 0, 0],[1, 1, 1, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
J2 = [[0, 0, 1, 0],[1, 1, 1, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
Z2 = [[0, 1, 1, 0],[1, 1, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
S2 = [[1, 1, 0, 0],[0, 1, 1, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
T2 = [[0, 0, 0, 0],[1, 1, 1, 0],[0, 1, 0, 0],[0, 0, 0, 0]]

# second rotation @180 deg
L3 = [[1, 1, 0, 0],[1, 0, 0, 0],[1, 0, 0, 0],[0, 0, 0, 0]]
J3 = [[1, 0, 0, 0],[1, 0, 0, 0],[1, 1, 0, 0],[0, 0, 0, 0]]
T3 = [[0, 1, 0, 0],[1, 1, 0, 0],[0, 1, 0, 0],[0, 0, 0, 0]]

# fourth rotation @270 deg
L4 = [[1, 1, 1, 0],[0, 0, 1, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
J4 = [[1, 1, 1, 0],[1, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
T4 = [[0, 1, 0, 0],[1, 1, 1, 0],[0, 0, 0, 0],[0, 0, 0, 0]]

# all piece state
I_ALLSTATE = [I, I2]
O_ALLSTATE = [O]
L_ALLSTATE = [L, L2, L3, L4]
J_ALLSTATE = [J, J2, J3, J4]
Z_ALLSTATE = [Z, Z2]
S_ALLSTATE = [S, S2]
T_ALLSTATE = [T, T2, T3, T4]

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(GAMECAPTION)

#                     Rect( x, y, width, height )
LEFTMARGINRECT      = Rect(0, 20, LEFTBORDER, WINDOWHEIGHT)
RIGHTMARGINRECT     = Rect((LEFTBORDER + BOXMARGIN + (BOXMOVESTEP * XBOXCOUNT)), 20, RIGHTBORDER, WINDOWHEIGHT)
TOPMARGINRECT       = Rect(0, 0, WINDOWWIDTH, TOPBORDER)
BOTTOMMARGINRECT    = Rect(0, (WINDOWHEIGHT - BOTTOMBORDER), WINDOWWIDTH, BOTTOMBORDER)

GAMEPLAYBORDER = [LEFTMARGINRECT, RIGHTMARGINRECT, BOTTOMMARGINRECT]

staticboxes = []

def main():
    pygame.init()
    pygame.time.set_timer(USEREVENT+1, (1100 - (100 * GAMESPEED)))
    DISPLAYSURF.fill(BGCOLOR)

    global staticboxes
    staticboxes = []

    current_piece, current_piece_label, current_rotation = generate_random_piece()

    move_down = False
    move_left = False
    move_right = False

    pygame.key.set_repeat(200, 50)

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        for rects in current_piece:
            for rect in rects:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, rect)

        draw_border()
        draw_static()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_UP:
                current_piece, current_piece_label, current_rotation = rotate_piece(current_piece, current_piece_label, current_rotation)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                current_piece = move_piece(current_piece, DOWN)
                pygame.time.set_timer(USEREVENT+1, (1100 - (100 * GAMESPEED)))
            elif event.type == KEYDOWN and event.key == K_LEFT:
                current_piece = move_piece(current_piece, LEFT)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                current_piece = move_piece(current_piece, RIGHT)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                drop_piece(current_piece)
                current_piece = None
            elif event.type == USEREVENT+1:
                current_piece = move_piece(current_piece, DOWN)

            if current_piece == None:
                break

        if current_piece == None:
            staticboxes = clear_static()
            current_piece, current_piece_label, current_rotation = generate_random_piece()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def move_piece(piece, direction=None, x=None, y=None):
    tempRect = []

    # print(piece)

    if is_move_collides(piece, direction, x, y):
        if is_floor(piece, direction, x, y):
            for rects in piece:
                for rect in rects:
                    set_static(rect)
            piece = None
        return piece

    for rectCol in piece:
        tempCol = []
        for rectRow in rectCol:
            rect = box_move(rectRow, direction, x, y)
            tempCol.append(rect)
        tempRect.append(tempCol)

    return tempRect

def rotate_piece(currentpiece, currentlabel, currentrotation):
    piecestate = I_ALLSTATE if currentlabel == 'I' else O_ALLSTATE if currentlabel == 'O' else L_ALLSTATE if currentlabel == 'L' else J_ALLSTATE if currentlabel == 'J' else Z_ALLSTATE if currentlabel == 'Z' else S_ALLSTATE if currentlabel == 'S' else T_ALLSTATE if currentlabel == 'T' else []
    index = (currentrotation + 1) % len(piecestate)

    x, y = get_piece_xy_pos(currentpiece, currentlabel, currentrotation)

    if is_collides(generate_piece(piece=piecestate[index], label=currentlabel, x=x, y=y, rotation=index)[0]):
        return currentpiece, currentlabel, currentrotation
    return generate_piece(piece=piecestate[index], label=currentlabel, x=x, y=y, rotation=index)

def drop_piece(currentpiece):
    tempPiece = currentpiece
    while not is_move_collides(tempPiece, DOWN, x=None, y=None):
        tempPiece = move_piece(tempPiece, DOWN)
    for pieces in tempPiece:
        for piece in pieces:
            set_static(piece)

def box_move(rect, direction=None, x=None, y=None):
    x = (-BOXMOVESTEP if direction == LEFT else BOXMOVESTEP if direction == RIGHT else 0) if x == None else x
    y = (BOXMOVESTEP if direction == DOWN else BOXMOVESTEP if direction == UP else 0) if y == None else y
    return rect.move(x, y)

def is_move_collides(piece, direction, x, y):
    for rectCol in piece:
        for rectRow in rectCol:
            tempRect = box_move(rectRow, direction, x, y)
            if tempRect.collidelistall(GAMEPLAYBORDER) != [] or tempRect.collidelistall(staticboxes) != []:
                return True
    return False

def is_collides(piece):
    for rectCol in piece:
        for rectRow in rectCol:
            if rectRow.collidelistall(GAMEPLAYBORDER) != [] or rectRow.collidelistall(staticboxes) != []:
                return True
    return False

def is_floor(piece, direction, x, y):
    for rectCol in piece:
        for rectRow in rectCol:
            tempRect = box_move(rectRow, direction, x, y)
            if tempRect.collidelist(GAMEPLAYBORDER) == 2:
                return True
            elif tempRect.collidelistall(staticboxes) != []:
                if direction == DOWN:
                    return True
    return False

def set_static(rect):
    staticboxes.append(rect)

def clear_static():
    new_static = staticboxes
    count = [0] * (len(staticboxes))
    for rect in new_static:
        # print((597 - rect.y) // 22)
        count[((597 - rect.y) // 22) - 1] += 1

    for x in range(len(count)-1, -1, -1):
        if count[x] == XBOXCOUNT:
            new_static = [i for i in new_static if i.y != 597 - (22 * (x+1))]

            for i in range(len(new_static)):
                if new_static[i].y < 597 - (22 * (x+1)):
                    new_static[i] = box_move(new_static[i], DOWN)

    return new_static if new_static != [] else staticboxes

def draw_border():
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, LEFTMARGINRECT)
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, RIGHTMARGINRECT)

    pygame.draw.rect(DISPLAYSURF, DARKGRAY, TOPMARGINRECT)
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, BOTTOMMARGINRECT)

def draw_static():
    for rect in staticboxes:
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, rect)

def get_piece_xy_pos(currentpiece, currentlabel, currentrotation):
    x = 0
    y = 0
    if currentlabel == 'I':
        x = currentpiece[0][0].left if currentrotation == 0 else currentpiece[1][0].left - BOXMOVESTEP
        y = currentpiece[0 if currentrotation == 0 else 1][0].top
    elif currentlabel == 'O':
        x = currentpiece[0][0].left
        y = currentpiece[0][0].top
    elif currentlabel == 'L':
        x = currentpiece[0][0].left
        y = currentpiece[0][0].top - (BOXMOVESTEP if currentrotation == 0 else 0)
    elif currentlabel == 'J':
        x = currentpiece[0][0].left
        y = currentpiece[0][0].top - (BOXMOVESTEP * 2 if currentrotation == 1 else 0)
    elif currentlabel == 'Z':
        x = currentpiece[0][0].left
        y = currentpiece[0][0].top - (BOXMOVESTEP if currentrotation == 1 else 0)
    elif currentlabel == 'S':
        x = currentpiece[0][0].left
        y = currentpiece[0][0].top - (BOXMOVESTEP if currentrotation == 0 else 0)
    elif currentlabel == 'T':
        x = currentpiece[0][0].left if currentrotation in [0, 2, 3] else currentpiece[1][0].left - BOXMOVESTEP
        y = currentpiece[0][0].top - BOXMOVESTEP if currentrotation == 0 else currentpiece[1][0].top
    return x, y

def generate_random_piece():
    index = int((random.random() * (random.random() * 1000)) % 7)
    return generate_piece(index=index)

def generate_piece(piece=None, index=None, label=None, x=None, y=None, rotation=None):
    xpos = DEFAULTXPOS if x == None else x
    ypos = DEFAULTYPOS if y == None else y
    pieces = [I, O, L, J, Z, S, T]
    pieceslabel = ['I', 'O', 'L', 'J', 'Z', 'S', 'T']
    label = pieceslabel[index] if index != None else label if label != None else ''
    piece = pieces[index] if index != None else piece if piece != None else []
    tempRect = []
    for x in range(len(piece)):
        tempRow = []
        for y in range(len(piece[x])):
            if piece[x][y] == 1:
                tempRow.append(
                    Rect((xpos + (BOXMOVESTEP * x)), (ypos + (BOXMOVESTEP * y)), BOXSIZE, BOXSIZE))
        tempRect.append(tempRow)

    return tempRect, label, (0 if rotation == None else rotation)

if __name__ == '__main__':
    main()


# def boxMove(rect, direction=None, x=None, y=None):
#     # print("box is moving", direction)
#     if direction != None:
#         x = (-BOXMOVESTEP if direction == LEFT else BOXMOVESTEP if direction == RIGHT else 0) if x == None else x
#         y = (BOXMOVESTEP if direction == DOWN else -BOXMOVESTEP if direction == UP else 0) if y == None else y
#     elif (x==None and y==None):
#         print("ERROR: Direction and x and y is undefined!")
#         return rect.move(0,0)
#
#     tempRect = rect.move(x, y)
#
#     if (tempRect.collidelistall(GAMEPLAYBORDER) != []) or (tempRect.collidelistall(STATICBOXES) != []):
#         # print("COLLIDES")
#         if (tempRect.collidelist(GAMEPLAYBORDER) == 3) or (tempRect.collidelistall(STATICBOXES) != []):
#             setStatic(rect)
#             return Rect(DEFAULTXPOS, DEFAULTYPOS, BOXSIZE, BOXSIZE)
#         return rect.move(0,0)
#
#     return rect.move(x, y)
