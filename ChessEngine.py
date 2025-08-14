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

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] == "--" : #empty square can not capture a piece
            return
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove



class Move():
    def __init__(self, startSQ, endSQ,Board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.Board = Board
        self.pieceMoved = Board[self.startRow][self.startCol]
        self.pieceCaptured = Board[self.endRow][self.endCol]
        if Board[self.startRow][self.startCol] ==  "--":
            return


    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def getChessNotation(self):
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow,self.endCol)

    def getRankFiles(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
