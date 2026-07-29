#include "ChessEngine.h"

namespace {

// The major pieces, in the order the original iterated over them. The order
// matters: getChessNotation() walks this list and returns on the first hit.
constexpr char kPieces[] = {'B', 'R', 'N', 'Q', 'K'};
constexpr char kPawn = 'P';

Piece makePiece(char color, char type) { return Piece{color, type}; }

constexpr Piece kEmpty{};

}  // namespace

// ---------------------------------------------------------------------------
// Move
// ---------------------------------------------------------------------------

Move::Move(int startSQRow, int startSQCol, int endSQRow, int endSQCol,
           const Board& board, bool whiteToMove)
    : startRow(startSQRow),
      startCol(startSQCol),
      endRow(endSQRow),
      endCol(endSQCol),
      pieceMoved(board[startSQRow][startSQCol]),
      pieceCaptured(board[endSQRow][endSQCol]),
      whiteToMove(whiteToMove),
      board(&board) {}

std::optional<std::string> Move::getChessNotation() const {
    const Piece moved = (*board)[startRow][startCol];
    const Piece captured = (*board)[endRow][endCol];

    // Checks if it's white's move if white is moving, otherwise it would print
    // moves even though they were never made.
    if ((moved.color == 'w' && whiteToMove) ||
        (captured.color == 'b' || !whiteToMove)) {
        if (moved.isEmpty()) {  // empty squares can not move
            return std::nullopt;
        }
        if (!captured.isEmpty()) {  // captures are denoted with x e.g. exd4
            for (const char c : kPieces) {
                // major pieces mention their first letter e.g. Bxd4
                if (moved.type == c) {
                    return std::string(1, moved.type) + "x" +
                           getRankFiles(endRow, endCol);
                }
            }
            // pawn captures don't mention P, only the file they were in
            return getRanks(startCol) + "x" + getRankFiles(endRow, endCol);
        }
        for (const char c : kPieces) {
            // piece moves mention their first letter in capital e.g. Bc4
            if (moved.type == c) {
                return std::string(1, c) + getRankFiles(endRow, endCol);
            }
            if (moved.type == kPawn) {  // pawn moves don't mention P e.g. e4, f5
                return getRankFiles(endRow, endCol);
            }
        }
    }
    return std::nullopt;
}

// colsToFiles / rowsToRanks: column 0 is file 'a', row 0 is rank 8.
std::string Move::getRankFiles(int r, int c) {
    return std::string{static_cast<char>('a' + c), static_cast<char>('8' - r)};
}

std::string Move::getRanks(int c) {
    return std::string(1, static_cast<char>('a' + c));
}

bool Move::operator==(const Move& other) const {
    return startRow == other.startRow && startCol == other.startCol &&
           endRow == other.endRow && endCol == other.endCol &&
           pieceMoved == other.pieceMoved;
}

// ---------------------------------------------------------------------------
// GameState
// ---------------------------------------------------------------------------

GameState::GameState() {
    const char backRank[8] = {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'};
    board = Board{};
    for (int c = 0; c < 8; ++c) {
        board[0][c] = makePiece('b', backRank[c]);
        board[1][c] = makePiece('b', 'P');
        board[6][c] = makePiece('w', 'P');
        board[7][c] = makePiece('w', backRank[c]);
    }
}

bool GameState::makeMove(const Move& move) {
    // Empty square can not capture a piece.
    if (board[move.startRow][move.startCol].isEmpty()) {
        return false;
    }
    // White piece can not move when it's not white's turn and vice versa.
    const Piece piece = board[move.startRow][move.startCol];
    if ((piece.color == 'w' && !whiteToMove) ||
        (piece.color == 'b' && whiteToMove)) {
        return false;
    }

    board[move.startRow][move.startCol] = kEmpty;
    board[move.endRow][move.endCol] = move.pieceMoved;
    moveLog.push_back(move);
    whiteToMove = !whiteToMove;
    return true;
}

void GameState::undoMove() {
    if (!moveLog.empty()) {
        const Move move = moveLog.back();
        moveLog.pop_back();
        board[move.startRow][move.startCol] = move.pieceMoved;
        board[move.endRow][move.endCol] = move.pieceCaptured;
        whiteToMove = !whiteToMove;
        undoMoveLog.push_back(move);
    }
}

void GameState::redoMove() {
    if (!undoMoveLog.empty()) {
        const Move move = undoMoveLog.back();
        undoMoveLog.pop_back();
        board[move.startRow][move.startCol] = kEmpty;
        board[move.endRow][move.endCol] = move.pieceMoved;
        whiteToMove = !whiteToMove;
        moveLog.push_back(move);
    }
}

std::vector<Move> GameState::getAllValidMoves() {
    // TODO: filter moves that leave king in check
    return getAllPossibleMoves();
}

std::vector<Move> GameState::getAllPossibleMoves() {
    std::vector<Move> moves;
    for (int r = 0; r < 8; ++r) {
        for (int c = 0; c < 8; ++c) {
            const char turn = board[r][c].color;
            if ((turn == 'w' && whiteToMove) || (turn == 'b' && !whiteToMove)) {
                switch (board[r][c].type) {
                    case 'P': getAllPawnMoves(r, c, moves); break;
                    case 'R': getAllRookMoves(r, c, moves); break;
                    case 'B': getAllBishopMoves(r, c, moves); break;
                    case 'N': getAllKnightMoves(r, c, moves); break;
                    case 'Q': getAllQueenMoves(r, c, moves); break;
                    case 'K': getAllKingMoves(r, c, moves); break;
                    default: break;
                }
            }
        }
    }
    return moves;
}

void GameState::getAllPawnMoves(int r, int c, std::vector<Move>& moves) {
    const char pieceColor = board[r][c].color;

    if (pieceColor == 'w') {  // White pawn logic
        // Bounds guard added in the port: without promotion a white pawn can
        // reach row 0, where Python's negative indexing quietly wrapped around
        // to row 7 and C++ would read out of bounds.
        if (r - 1 < 0) {
            return;
        }
        if (board[r - 1][c].isEmpty()) {  // single move
            moves.emplace_back(r, c, r - 1, c, board, whiteToMove);
            if (r == 6 && board[r - 2][c].isEmpty()) {  // double move from start
                moves.emplace_back(r, c, r - 2, c, board, whiteToMove);
            }
        }
        // captures
        if (c - 1 >= 0 && board[r - 1][c - 1].color == 'b') {  // capture left
            moves.emplace_back(r, c, r - 1, c - 1, board, whiteToMove);
        }
        if (c + 1 < 8 && board[r - 1][c + 1].color == 'b') {  // capture right
            moves.emplace_back(r, c, r - 1, c + 1, board, whiteToMove);
        }
    } else if (pieceColor == 'b') {  // Black pawn logic
        if (r + 1 > 7) {  // see the note above; the Python version raised here
            return;
        }
        if (board[r + 1][c].isEmpty()) {  // single move
            moves.emplace_back(r, c, r + 1, c, board, whiteToMove);
            if (r == 1 && board[r + 2][c].isEmpty()) {  // double move from start
                moves.emplace_back(r, c, r + 2, c, board, whiteToMove);
            }
        }
        // captures
        if (c - 1 >= 0 && board[r + 1][c - 1].color == 'w') {  // capture left
            moves.emplace_back(r, c, r + 1, c - 1, board, whiteToMove);
        }
        if (c + 1 < 8 && board[r + 1][c + 1].color == 'w') {  // capture right
            moves.emplace_back(r, c, r + 1, c + 1, board, whiteToMove);
        }
    }
}

void GameState::getAllRookMoves(int r, int c, std::vector<Move>& moves) {
    const char pieceColor = board[r][c].color;
    if (pieceColor != 'w' && pieceColor != 'b') {
        return;
    }
    // The original spelled the white and black cases out separately; they are
    // identical once "the other colour" is named, so they collapse into one.
    const char enemyColor = (pieceColor == 'w') ? 'b' : 'w';

    bool rookHitUp = false;
    bool rookHitDown = false;
    bool rookHitLeft = false;
    bool rookHitRight = false;

    for (int i = 1; i < 8; ++i) {
        // checks if the new row or col does not go beyond the edge of the board
        const int newRow = r + i;
        const int newCol = c + i;
        if (newCol >= 0 && newCol < 8 && !rookHitRight) {
            const Piece endPiece = board[r][newCol];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, r, newCol, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, r, newCol, board, whiteToMove);
                rookHitRight = true;
            }
            if (endPiece.color == pieceColor) {
                rookHitRight = true;
            }
        }
        if (newRow >= 0 && newRow < 8 && !rookHitUp) {
            const Piece endPiece = board[newRow][c];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRow, c, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRow, c, board, whiteToMove);
                rookHitUp = true;
            }
            if (endPiece.color == pieceColor) {
                rookHitUp = true;
            }
        }
    }

    for (int i = 1; i < 8; ++i) {
        const int newRow = r - i;
        const int newCol = c - i;
        if (newCol >= 0 && newCol < 8 && !rookHitLeft) {
            const Piece endPiece = board[r][newCol];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, r, newCol, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, r, newCol, board, whiteToMove);
                rookHitLeft = true;
            }
            if (endPiece.color == pieceColor) {
                rookHitLeft = true;
            }
        }
        if (newRow >= 0 && newRow < 8 && !rookHitDown) {
            const Piece endPiece = board[newRow][c];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRow, c, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRow, c, board, whiteToMove);
                rookHitDown = true;
            }
            if (endPiece.color == pieceColor) {
                rookHitDown = true;
            }
        }
    }
}

void GameState::getAllKnightMoves(int r, int c, std::vector<Move>& moves) {
    const char pieceColor = board[r][c].color;
    const int i = 2;
    const int j = 1;

    const int offsets[8][2] = {{i, j},  {i, -j},  {-i, j},  {-i, -j},
                               {j, i},  {j, -i},  {-j, i},  {-j, -i}};

    for (const auto& offset : offsets) {
        const int newRow = r + offset[0];
        const int newCol = c + offset[1];
        if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
            const Piece endPiece = board[newRow][newCol];
            if (endPiece.isEmpty() || endPiece.color != pieceColor) {
                moves.emplace_back(r, c, newRow, newCol, board, whiteToMove);
            }
        }
    }
}

void GameState::getAllBishopMoves(int r, int c, std::vector<Move>& moves) {
    const char pieceColor = board[r][c].color;
    if (pieceColor != 'w' && pieceColor != 'b') {
        return;
    }
    const char enemyColor = (pieceColor == 'w') ? 'b' : 'w';

    bool pieceHitNorthEast = false;
    bool pieceHitSouthEast = false;
    bool pieceHitNorthWest = false;
    bool pieceHitSouthWest = false;

    for (int i = 1; i < 8; ++i) {
        const int newRow = r + i;
        const int newCol = c + i;
        const int newColn = c - i;
        const int newRown = r - i;

        if (newRow >= 0 && newRow < 8 && newCol >= 0 && newCol < 8 &&
            !pieceHitNorthEast) {
            const Piece endPiece = board[newRow][newCol];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRow, newCol, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRow, newCol, board, whiteToMove);
                pieceHitNorthEast = true;
            }
            if (endPiece.color == pieceColor) {
                pieceHitNorthEast = true;
            }
        }
        if (newRow >= 0 && newRow < 8 && newColn >= 0 && newColn < 8 &&
            !pieceHitNorthWest) {
            const Piece endPiece = board[newRow][newColn];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRow, newColn, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRow, newColn, board, whiteToMove);
                pieceHitNorthWest = true;
            }
            if (endPiece.color == pieceColor) {
                pieceHitNorthWest = true;
            }
        }
        if (newRown >= 0 && newRown < 8 && newCol >= 0 && newCol < 8 &&
            !pieceHitSouthEast) {
            const Piece endPiece = board[newRown][newCol];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRown, newCol, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRown, newCol, board, whiteToMove);
                pieceHitSouthEast = true;
            }
            if (endPiece.color == pieceColor) {
                pieceHitSouthEast = true;
            }
        }
        if (newRown >= 0 && newRown < 8 && newColn >= 0 && newColn < 8 &&
            !pieceHitSouthWest) {
            const Piece endPiece = board[newRown][newColn];
            if (endPiece.isEmpty()) {
                moves.emplace_back(r, c, newRown, newColn, board, whiteToMove);
            }
            if (endPiece.color == enemyColor) {
                moves.emplace_back(r, c, newRown, newColn, board, whiteToMove);
                pieceHitSouthWest = true;
            }
            if (endPiece.color == pieceColor) {
                pieceHitSouthWest = true;
            }
        }
    }
}

void GameState::getAllKingMoves(int r, int c, std::vector<Move>& moves) {
    const int i = 1;
    const int j = 1;
    // Stored as (dc, dr) pairs, matching how the original unpacked its list.
    const int directions[8][2] = {{i, 0},   {i, j},  {i, -j}, {-i, j},
                                  {-i, 0},  {-i, -j}, {0, -j}, {0, j}};
    const char pieceColor = board[r][c].color;

    for (const auto& direction : directions) {
        const int dc = direction[0];
        const int dr = direction[1];
        if (0 <= r + dr && r + dr < 8 && 0 <= c + dc && c + dc < 8) {
            const Piece endPiece = board[r + dr][c + dc];
            if (endPiece.isEmpty() || endPiece.color != pieceColor) {
                moves.emplace_back(r, c, r + dr, c + dc, board, whiteToMove);
            }
        }
    }
}

void GameState::getAllQueenMoves(int r, int c, std::vector<Move>& moves) {
    getAllRookMoves(r, c, moves);
    getAllBishopMoves(r, c, moves);
}
