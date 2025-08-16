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
            return False
        piece = self.board[move.startRow][move.startCol] # White piece can not move when its not white's turn and vice versa
        if (piece[0] == 'w' and not self.WhiteToMove) or (piece[0] == 'b' and self.WhiteToMove):
            return False

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove
        return True

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
    """
    This function will check the validity of moves for example moving a piece that is blocking a check 
    """
    def getAllValidMoves(self):
        return self.getAllPossibleMoves()
    """
    This function will consider only the moves of whose turn it is without caring about checks 
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.WhiteToMove) and (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getAllPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getAllRookMoves(r,c,moves)
                    elif piece == 'N':
                        self.getAllKnightMoves(r,c,moves)
                    elif piece == 'B':
                        self.getAllBishopMoves(r,c,moves)
                    elif piece == 'K':
                        self.getAllKingMoves(r,c,moves)

    """
    calculates possible moves for given piece
    """

    def getAllPawnMoves(self, r, c, moves):
        pass

    def getAllRookMoves(self, r, c, moves):
        pass

    def getAllKnightMoves(self, r, c, moves):
        pass

    def getAllBishopMoves(self, r, c, moves):
        pass

    def getAllKingMoves(self, r, c, moves):
        pass


class Move():
    def __init__(self, startSQ, endSQ,Board,WhiteToMove):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.Board = Board
        self.pieceMoved = Board[self.startRow][self.startCol]
        self.pieceCaptured = Board[self.endRow][self.endCol]
        self.WhiteToMove = WhiteToMove
        if Board[self.startRow][self.startCol] ==  "--":
            return


    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def getChessNotation(self):
        pieceMoved = self.Board[self.startRow][self.startCol]
        pieceCaptured = self.Board[self.endRow][self.endCol]
        pieces = ["B","R","N","Q","K"]
        pawn = "P"
        if (pieceMoved[0] == "w" and self.WhiteToMove == True) or(pieceCaptured[0] == "b" or  self.WhiteToMove == False): # checks if its whites move if white is moving otherwise it will print moves even tho they were not made
            if pieceMoved == "--":  # empty squares can not move
                return None
            if pieceCaptured != "--": # captured pieces are denoted with x e.g. exd4
                if pieceMoved[1] in pieces: # major pieces captured mentions thier first letter e.g. Bxd4
                    return pieceMoved[1] + "x" + self.getRankFiles(self.endRow, self.endCol)
                return self.getRanks(self.startCol) + "x" + self.getRankFiles(self.endRow, self.endCol) # pawn captures dont mention P it only mentions the file they were in
            for C in pieces:
                if pieceMoved[1] == C: #piece moves mentions their first letter in capital e.g. Bc4
                    return C + self.getRankFiles(self.endRow, self.endCol)
                if pieceMoved[1] == pawn: # pawn moves dont mention P e.g. e4, f5
                    return self.getRankFiles(self.endRow, self.endCol)


    def getRankFiles(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    def getRanks(self,c):
        return self.colsToFiles[c]