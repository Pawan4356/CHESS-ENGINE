import pygame as p

import ChessEngine

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
        IMAGES[piece] = p.transform.scale(p.image.load("images/" +piece +".png"),(SQ_SIZE,SQ_SIZE))
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT) , p.RESIZABLE)
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    print(gs.board)
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        drawGameState(screen,gs)
        p.display.flip()

def drawGameState(screen ,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

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
