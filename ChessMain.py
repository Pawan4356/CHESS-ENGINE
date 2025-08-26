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
    pieces = ['wP', 'wK', 'wQ', 'wN', 'wB', 'wR',
              'bP', 'bK', 'bQ', 'bN', 'bB', 'bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"),
            (SQ_SIZE, SQ_SIZE)
        ).convert_alpha()


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    # print(gs.board)
    loadImages()
    running = True
    selected_sq = ()
    player_clicks = []
    valid_moves = gs.getAllValidMoves()

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEWHEEL:
                if e.y > 0:  # undo
                    gs.undoMove()
                    valid_moves = gs.getAllValidMoves()
                    print([m.getChessNotation() for m in valid_moves])

                elif e.y < 0:  # redo
                    gs.redoMove()
                    valid_moves = gs.getAllValidMoves()
                    print([m.getChessNotation() for m in valid_moves])


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo
                    gs.undoMove()
                    valid_moves = gs.getAllValidMoves()
                elif e.key == p.K_y:  # redo
                    gs.redoMove()
                    valid_moves = gs.getAllValidMoves()

            elif e.type == p.MOUSEBUTTONDOWN:
                if e.button == 1:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if selected_sq == (row, col):
                        selected_sq = ()
                        player_clicks = []
                    else:
                        selected_sq = (row, col)
                        player_clicks.append(selected_sq)

                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board,gs.WhiteToMove)
                        if move in valid_moves:
                            notation = move.getChessNotation()
                            if notation:
                                if gs.WhiteToMove:  # White move
                                    print(str(gs.moveCount) + ". " + notation + " ", end="")
                                else:  # Black move
                                    print(str(notation) + " ", end="")
                                    gs.moveCount += 1

                            gs.makeMove(move)
                            valid_moves = gs.getAllValidMoves()  # <-- update directly

                        player_clicks = []
                        selected_sq = ()

        clock.tick(MAX_FPS)
        drawGameState(screen, gs, selected_sq,valid_moves)
        p.display.flip()


def drawGameState(screen, gs, selectedSQ, valid_moves):
    drawBoard(screen)

    highlightSquares(screen,gs, selectedSQ,valid_moves)
    drawPieces(screen, gs.board)


def highlightSquares(screen, gs, selectedSQ, valid_moves):
    if selectedSQ != ():
        r, c = selectedSQ
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):  # only highlight correct side's piece
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("green"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # highlight all valid moves for that piece
            for move in valid_moves:
                if move.startRow == r and move.startCol == c:
                    highlight = p.Surface((SQ_SIZE, SQ_SIZE))
                    highlight.set_alpha(100)
                    if gs.board[move.endRow][move.endCol] == "--":
                        highlight.fill(p.Color("yellow"))  # quiet move
                    else:
                        highlight.fill(p.Color("red"))  # capture
                    screen.blit(highlight, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))



def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
