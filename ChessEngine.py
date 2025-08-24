"""
This is where all the computation of legal moves and best move in position etc. will happen
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
        self.MoveFunctions = {'P':self.getAllPawnMoves,'R':self.getAllRookMoves,'B':self.getAllBishopMoves,'N':self.getAllKnightMoves,'Q':self.getAllQueenMoves,'K': self.getAllKingMoves}
        self.WhiteToMove = True
        self.MoveLog = []
        self.GameOver = False
        self.undoMoveLog = []
        self.moveCount = 1

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] == "--" : #empty square can not capture a piece
            return False
        piece = self.board[move.startRow][move.startCol] # White piece can not move when it's not white's turn and vice versa
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
        # TODO: filter moves that leave king in check
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.MoveFunctions[piece](r,c,moves)
        return moves
    """
    calculates possible moves for given piece
    """

    def getAllPawnMoves(self, r, c, moves):
        pieceColor = self.board[r][c][0]

        if pieceColor == "w":  # White pawn logic
            if self.board[r - 1][c] == "--":  # single move
                moves.append(Move((r, c), (r - 1, c), self.board, self.WhiteToMove))
                if r == 6 and self.board[r - 2][c] == "--":  # double move from start
                    moves.append(Move((r, c), (r - 2, c), self.board, self.WhiteToMove))
            # captures
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":  # capture left
                moves.append(Move((r, c), (r - 1, c - 1), self.board, self.WhiteToMove))
            if c + 1 < 8 and self.board[r - 1][c + 1][0] == "b":  # capture right
                moves.append(Move((r, c), (r - 1, c + 1), self.board, self.WhiteToMove))

        elif pieceColor == "b":  # Black pawn logic
            if self.board[r + 1][c] == "--":  # single move
                moves.append(Move((r, c), (r + 1, c), self.board, self.WhiteToMove))
                if r == 1 and self.board[r + 2][c] == "--":  # double move from start
                    moves.append(Move((r, c), (r + 2, c), self.board, self.WhiteToMove))
            # captures
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":  # capture left
                moves.append(Move((r, c), (r + 1, c - 1), self.board, self.WhiteToMove))
            if c + 1 < 8 and self.board[r + 1][c + 1][0] == "w":  # capture right
                moves.append(Move((r, c), (r + 1, c + 1), self.board, self.WhiteToMove))

        return moves

    def getAllRookMoves(self, r, c, moves):
        pieceColor = self.board[r][c][0]
        rookHitUp= False
        rookHitDown = False
        rookHitLeft = False
        rookHitRight = False

        if pieceColor == "w":
            for i in range(1,8):
                new_row = r + i # checks if the new row or col does not go beyond the edge of the board
                new_col = c + i
                if (new_col >= 0) and (new_col<8):
                    if rookHitRight == False:
                        if self.board[r][c+i] == "--":
                            moves.append(Move((r,c),(r, c + i), self.board, self.WhiteToMove))

                        if self.board[r][c+i][0] == "b":
                            moves.append(Move((r,c),(r, c + i), self.board, self.WhiteToMove))
                            rookHitRight = True
                        if self.board[r][c+i][0] == "w":
                            rookHitRight = True
                if (new_row >= 0) and (new_row<8):
                    if rookHitUp == False:
                        if self.board[r + i][c] == "--":
                            moves.append(Move((r,c),(r + i, c), self.board, self.WhiteToMove))

                        if self.board[r + i][c][0] == "b":
                            moves.append(Move((r,c),(r + i, c), self.board, self.WhiteToMove))
                            rookHitUp = True
                        if self.board[r + i][c][0] == "w":
                            rookHitUp = True

            for i in range(1,8):
                new_row = r - i  # checks if the new row or col does not go beyond the edge of the board
                new_col = c - i
                if (new_col >= 0) and (new_col < 8):
                    if rookHitLeft == False:
                        if self.board[r][c - i] == "--":
                            moves.append(Move((r, c), (r, c - i), self.board, self.WhiteToMove))

                        if  self.board[r][c - i][0] == "b":
                            moves.append(Move((r, c), (r, c - i), self.board, self.WhiteToMove))
                            rookHitLeft = True
                        if self.board[r][c - i][0] == "w":
                            rookHitLeft = True
                if (new_row >= 0) and (new_row < 8):
                    if rookHitDown == False:
                        if self.board[r - i][c] == "--":
                            moves.append(Move((r,c),(r - i, c), self.board, self.WhiteToMove))

                        if self.board[r - i][c][0] == "b":
                            moves.append(Move((r,c),(r - i, c), self.board, self.WhiteToMove))
                            rookHitDown = True
                        if self.board[r - i][c][0] == "w":
                            rookHitDown = True

        if pieceColor == "b":
            for i in range(1,8):
                new_row = r + i  # checks if the new row or col does not go beyond the edge of the board
                new_col = c + i
                if (new_col >= 0) and (new_col < 8):
                    if rookHitRight == False:
                        if self.board[r][c + i] == "--":
                            moves.append(Move((r, c), (r, c + i), self.board, self.WhiteToMove))

                        if  self.board[r][c + i][0] == "w":
                            moves.append(Move((r, c), (r, c + i), self.board, self.WhiteToMove))
                            rookHitRight = True
                        if self.board[r][c + i][0] == "b":
                            rookHitRight = True
                if (new_row >= 0) and (new_row < 8):
                    if rookHitUp == False:
                        if self.board[r + i][c] == "--":
                            moves.append(Move((r, c), (r + i, c), self.board, self.WhiteToMove))

                        if  self.board[r + i][c][0] == "w":
                            moves.append(Move((r, c), (r + i, c), self.board, self.WhiteToMove))
                            rookHitUp = True
                        if self.board[r + i][c][0] == "b":
                            rookHitUp = True

            for i in range(1,8):
                new_row = r - i  # checks if the new row or col does not go beyond the edge of the board
                new_col = c - i
                if (new_col >= 0) and (new_col < 8):
                    if rookHitLeft == False:
                        if self.board[r][c - i] == "--":
                            moves.append(Move((r, c), (r, c - i), self.board, self.WhiteToMove))

                        if self.board[r][c - i][0] == "w":
                            moves.append(Move((r, c), (r, c - i), self.board, self.WhiteToMove))
                            rookHitLeft = True
                        if self.board[r][c - i][0] == "b":
                            rookHitLeft = True

                if (new_row >= 0) and (new_row < 8):
                    if rookHitDown == False:
                        if self.board[r - i][c] == "--":
                            moves.append(Move((r, c), (r - i, c), self.board, self.WhiteToMove))

                        if self.board[r - i][c][0] == "w":
                            moves.append(Move((r, c), (r - i, c), self.board, self.WhiteToMove))
                            rookHitDown = True
                        if self.board[r - i][c][0] == "b":
                            rookHitDown = True
        return moves
        # pass

    def getAllKnightMoves(self, r, c, moves):
        pieceColor = self.board[r][c][0]
        i = 2
        j = 1
        if 0 <= r + i < 8 and 0 <= c + j < 8:
            if self.board[r + i][c + j] == "--" or self.board[r + i][c + j][0] != pieceColor:
                moves.append(Move((r, c), (r + i, c + j), self.board, self.WhiteToMove))

        if 0 <= r + i < 8 and 0 <= c - j < 8:
            if self.board[r + i][c - j] == "--" or self.board[r + i][c - j][0] != pieceColor:
                moves.append(Move((r, c), (r + i, c - j), self.board, self.WhiteToMove))

        if 0 <= r - i < 8 and 0 <= c + j < 8:
            if self.board[r - i][c + j] == "--" or self.board[r - i][c + j][0] != pieceColor:
                moves.append(Move((r, c), (r - i, c + j), self.board, self.WhiteToMove))

        if 0 <= r - i < 8 and 0 <= c - j < 8:
            if self.board[r - i][c - j] == "--" or self.board[r - i][c - j][0] != pieceColor:
                moves.append(Move((r, c), (r - i, c - j), self.board, self.WhiteToMove))

        if 0 <= r + j < 8 and 0 <= c + i < 8:
            if self.board[r + j][c + i] == "--" or self.board[r + j][c + i][0] != pieceColor:
                moves.append(Move((r, c), (r + j, c + i), self.board, self.WhiteToMove))

        if 0 <= r + j < 8 and 0 <= c - i < 8:
            if self.board[r + j][c - i] == "--" or self.board[r + j][c - i][0] != pieceColor:
                moves.append(Move((r, c), (r + j, c - i), self.board, self.WhiteToMove))

        if 0 <= r - j < 8 and 0 <= c + i < 8:
            if self.board[r - j][c + i] == "--" or self.board[r - j][c + i][0] != pieceColor:
                moves.append(Move((r, c), (r - j, c + i), self.board, self.WhiteToMove))

        if 0 <= r - j < 8 and 0 <= c - i < 8:
            if self.board[r - j][c - i] == "--" or self.board[r - j][c - i][0] != pieceColor:
                moves.append(Move((r, c), (r - j, c - i), self.board, self.WhiteToMove))

        return moves



    def getAllBishopMoves(self, r, c, moves):
        pieceColor = self.board[r][c][0]
        pieceHitNorthEast = False
        pieceHitSouthEast = False
        pieceHitNorthWest = False
        pieceHitSouthWest = False
        for i in range(1,8):
            new_row = r + i
            new_col = c + i
            new_coln = c - i
            new_rown = r - i

            if (new_row >= 0) and (new_row < 8) and (new_col >= 0) and (new_col < 8):
                endPiece = self.board[new_row][new_col]


                if pieceHitNorthEast == False:

                    if endPiece == "--":
                        moves.append(Move((r, c), (new_row, new_col), self.board, self.WhiteToMove))
                    if (endPiece[0] == "b" and pieceColor == "w") or (endPiece[0]=='w' and pieceColor == "b"):
                        moves.append(Move((r, c), (new_row, new_col), self.board, self.WhiteToMove))
                        pieceHitNorthEast = True
                    if (endPiece[0] == "w" and pieceColor == "w") or (endPiece[0]=='b' and pieceColor == "b"):
                        pieceHitNorthEast = True
            if (new_row >= 0) and (new_row < 8) and (new_coln >= 0) and (new_coln < 8):
                endPiece1 = self.board[new_row][new_coln]
                if pieceHitNorthWest == False:
                    if endPiece1 == "--":
                        moves.append(Move((r, c), (new_row, new_coln), self.board, self.WhiteToMove))
                    if (endPiece1[0] == "b" and pieceColor == "w") or (endPiece1[0]=='w' and pieceColor == "b"):
                        moves.append(Move((r, c), (new_row, new_coln), self.board, self.WhiteToMove))
                        pieceHitNorthWest = True
                    if (endPiece1[0] == "w" and pieceColor == "w") or (endPiece1[0] =='b' and pieceColor == "b"):
                        pieceHitNorthWest = True
            if (new_rown >= 0) and (new_rown < 8) and (new_col >= 0) and (new_col < 8):
                endPiece2 = self.board[new_rown][new_col]
                if pieceHitSouthEast == False:
                    if endPiece2 == "--":
                        moves.append(Move((r, c), (new_rown, new_col), self.board, self.WhiteToMove))
                    if (endPiece2[0] == "b" and pieceColor == "w") or (endPiece2[0] == 'w' and pieceColor == "b"):
                        moves.append(Move((r, c), (new_rown, new_col), self.board, self.WhiteToMove))
                        pieceHitSouthEast = True
                    if (endPiece2[0] == "w" and pieceColor == "w") or (endPiece2[0] == 'b' and pieceColor == "b"):
                        pieceHitSouthEast = True
            if (new_rown >= 0) and (new_rown < 8) and (new_coln >= 0) and (new_coln < 8):
                endPiece3 = self.board[new_rown][new_coln]
                if pieceHitSouthWest == False:
                    if endPiece3 == "--":
                        moves.append(Move((r, c), (new_rown, new_coln), self.board, self.WhiteToMove))
                    if (endPiece3[0] == "b" and pieceColor == "w") or (endPiece3[0] == 'w' and pieceColor == "b"):
                        moves.append(Move((r, c), (new_rown, new_coln), self.board, self.WhiteToMove))
                        pieceHitSouthWest = True
                    if (endPiece3[0] == "w" and pieceColor == "w") or (endPiece3[0] == 'b' and pieceColor == "b"):
                        pieceHitSouthWest = True

        return moves
    def getAllKingMoves(self, r, c, moves):
        i = 1
        j = 1
        directions = [(i,0),(i,j),(i,-j),(-i,j),(-i,0),(-i,-j),(0,-j),(0,j)]
        pieceColor = self.board[r][c][0]
        for dc,dr in directions:
            if 0 <= r + dr < 8 and 0 <= c + dc < 8:
                if self.board[r + dr][c + dc] == "--" or self.board[r + dr][c + dc][0] != pieceColor:
                    moves.append(Move((r,c),(r+dr,c+dc),self.board, self.WhiteToMove))

        return moves


    def getAllQueenMoves(self, r, c, moves):
        self.getAllRookMoves(r, c, moves)
        self.getAllBishopMoves(r, c, moves)
        return moves


class Move:
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
        pieces = ["B", "R", "N", "Q", "K"]
        pawn = "P"
        if (pieceMoved[0] == "w" and self.WhiteToMove == True) or (pieceCaptured[0] == "b" or self.WhiteToMove == False):  # checks if its whites move if white is moving otherwise it will print moves even tho they were not made
            if pieceMoved == "--":  # empty squares can not move
                return None
            if pieceCaptured != "--":  # captured pieces are denoted with x e.g. exd4
                if pieceMoved[1] in pieces:  # major pieces captured mentions their first letter e.g. Bxd4
                    return pieceMoved[1] + "x" + self.getRankFiles(self.endRow, self.endCol)
                return self.getRanks(self.startCol) + "x" + self.getRankFiles(self.endRow, self.endCol)  # pawn captures don't mention P it only mentions the file they were in
            for C in pieces:
                if pieceMoved[1] == C:  # piece moves mentions their first letter in capital e.g. Bc4
                    return C + self.getRankFiles(self.endRow, self.endCol)
                if pieceMoved[1] == pawn:  # pawn moves dont mention P e.g. e4, f5
                    return self.getRankFiles(self.endRow, self.endCol)
        return None

    def getRankFiles(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    def getRanks(self,c):
        return self.colsToFiles[c]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.startRow == other.startRow and self.startCol == other.startCol \
                and self.endRow == other.endRow and self.endCol == other.endCol \
                and self.pieceMoved == other.pieceMoved
        return False
