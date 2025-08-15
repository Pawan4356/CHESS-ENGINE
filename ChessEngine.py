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
        self.undoMoveLog = []
        self.moveCount = 1

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] == "--" : #empty square can not capture a piece
            return
        piece = self.board[move.startRow][move.startCol]
        if (piece[0] == 'w' and not self.WhiteToMove) or (piece[0] == 'b' and self.WhiteToMove):
            return

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove

    def undoMove(self):
        if len(self.MoveLog) != 0:
            move = self.MoveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            self.undoMoveLog.append(move)
            # self.MoveLog = self.MoveLog[::-1]
            # self.WhiteToMove = not self.WhiteToMove
            # self.board[moveLog[::-1].endRow][moveLog[::-1].endCol] = "--"
            # self.board[moveLog[::-1].startRow][moveLog[::-1].startCol] = moveLog.pieceMoved
    def redoMove(self):
        if len(self.undoMoveLog) != 0:
            move = self.undoMoveLog.pop()
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.WhiteToMove = not self.WhiteToMove
            self.MoveLog.append(move)

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
        piece = self.Board[self.startRow][self.startCol]
        pieceCaptured = self.Board[self.endRow][self.endCol]
        pieces = ["B","R","N","Q"]
        pawn = "P"
        if pieceCaptured !=  "--":
            return self.getRanks(self.startCol) + "x" + self.getRankFiles(self.endRow,self.endCol)
        for C in pieces:
            if(piece[1] == C):
                return C + self.getRankFiles(self.endRow, self.endCol)
            if(piece[1] == pawn):
                return self.getRankFiles(self.endRow, self.endCol)
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow,self.endCol)

    def getRankFiles(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    def getRanks(self,c):
        return self.colsToFiles[c]