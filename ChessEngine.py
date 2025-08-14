"""
this is where all the computation of legal moves and best move in position etc. will happen
"""

class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.WhiteToMove = True
        self.MoveLog = []
        self.GameOver = False

# under progress
# class Move():
#     def __init__(self, startSQ, endSQ,Board):
#         self.startRow = startSQ[0]
#         self.startCol = startSQ[1]
#         self.endRow = endSQ[0]
#         self.endCol = endSQ[1]
#         self.Board = Board
#         self.pieceMoved = Board[self.startRow][self.startCol]
#         self.pieceCaptured = Board[self.endRow][self.endCol]
