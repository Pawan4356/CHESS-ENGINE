"""
This is the main python file where pygame will be used to show the board and
colors and pieces on the board
"""


import pygame as p

import ChessEngine
from ChessEngine import GameState

HEIGHT = WIDTH = 720
clock = p.time.Clock()
screen = p.display.set_mode((HEIGHT, HEIGHT))
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



def loadImages():
    pieces = ['wP', 'wK' ,'wQ' , 'wN' , 'wB' , 'wR' , 'bP' , 'bK' , 'bQ' , 'bN' , 'bB' , 'bR' ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" +piece +".png"),(SQ_SIZE,SQ_SIZE)).convert_alpha()
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT) , p.RESIZABLE)
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    print(gs.board)
    loadImages()
    running = True
    selectedSQ = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEWHEEL:
                if e.y > 0:  # undo
                    gs.undoMove()
                elif e.y < 0:  # redo
                    gs.redoMove()

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Ctrl+Z style
                    gs.undoMove()
                elif e.key == p.K_y:
                    gs.redoMove()

            elif e.type == p.MOUSEBUTTONDOWN:
                if e.button == 1:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if selectedSQ == (row, col):
                        selectedSQ = ()
                        playerClicks = []

                    else:
                        selectedSQ = (row, col)
                        playerClicks.append(selectedSQ)
                        # print(playerClicks)
                        # print(selectedSQ)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1],gs.board)
                        notation = move.getChessNotation()
                        if notation:
                            if gs.WhiteToMove: # prints the notation in pgn like format for example 1.e4 e5
                                print(str(gs.moveCount) + ". " +  notation + " ",end="")
                            else:
                                print(str(move.getChessNotation())+ " ", end="")
                                gs.moveCount += 1
                        playerClicks = []
                        selectedSQ = ()
                        gs.makeMove(move)
                    # print("Move log:", [m.getChessNotation() for m in gs.MoveLog])
                    # print("Undo log:", [m.getChessNotation() for m in gs.undoMoveLog])

            # elif e.type == p.MOUSEWHEEL:
            #     if e.y < 0:  # vertical down → undo
            #         gs.undoMove()
            #         selectedSQ = ()
            #         playerClicks = []
            #     elif e.y > 0:  # horizontal left → redo
            #         gs.redoMove()
            #         selectedSQ = ()
            #         playerClicks = []

        # def printBoard(board):
#     for i in range(8):
#         for j in range(8):
#             print(board[i][j], end=" ")





        clock.tick(MAX_FPS)
        drawGameState(screen,gs , selectedSQ)
        p.display.flip()

def drawGameState(screen ,gs,selectedSQ):
    drawBoard(screen)
    if selectedSQ != ():
        highlightSquare(screen, selectedSQ)
    drawPieces(screen,gs.board)

def highlightSquare(screen, square):
    r, c = square
    s = p.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)  # Transparency
    s.fill(p.Color("green"))
    screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # pass

if __name__ == '__main__':
    main()
