/*
 * This is where all the computation of legal moves and best move in position
 * etc. will happen.
 *
 * C++ port of ChessEngine.py.
 */

#pragma once

#include <array>
#include <optional>
#include <string>
#include <vector>

/*
 * A square, stored as the colour/type pair that the Python version packed into
 * a two character string ("wP", "bK", "--").
 */
struct Piece {
    char color = '-';  // 'w', 'b', or '-' for an empty square
    char type = '-';   // 'P', 'R', 'N', 'B', 'Q', 'K', or '-'

    bool isEmpty() const { return color == '-'; }

    bool operator==(const Piece& other) const {
        return color == other.color && type == other.type;
    }
    bool operator!=(const Piece& other) const { return !(*this == other); }
};

using Board = std::array<std::array<Piece, 8>, 8>;

class Move {
public:
    Move(int startSQRow, int startSQCol, int endSQRow, int endSQCol,
         const Board& board, bool whiteToMove);

    int startRow;
    int startCol;
    int endRow;
    int endCol;
    Piece pieceMoved;
    Piece pieceCaptured;
    bool whiteToMove;

    std::optional<std::string> getChessNotation() const;

    bool operator==(const Move& other) const;
    bool operator!=(const Move& other) const { return !(*this == other); }

private:
    // The original stored a reference to the live board and re-read it inside
    // getChessNotation(); keeping a pointer preserves that behaviour.
    const Board* board;

    static std::string getRankFiles(int r, int c);
    static std::string getRanks(int c);
};

class GameState {
public:
    GameState();

    Board board;
    bool whiteToMove = true;
    bool gameOver = false;
    int moveCount = 1;
    std::vector<Move> moveLog;
    std::vector<Move> undoMoveLog;

    bool makeMove(const Move& move);
    void undoMove();
    void redoMove();

    /*
     * This function will check the validity of moves, for example moving a
     * piece that is blocking a check.
     */
    std::vector<Move> getAllValidMoves();

    std::vector<Move> getAllPossibleMoves();

    /*
     * Calculates possible moves for the given piece.
     */
    void getAllPawnMoves(int r, int c, std::vector<Move>& moves);
    void getAllRookMoves(int r, int c, std::vector<Move>& moves);
    void getAllKnightMoves(int r, int c, std::vector<Move>& moves);
    void getAllBishopMoves(int r, int c, std::vector<Move>& moves);
    void getAllKingMoves(int r, int c, std::vector<Move>& moves);
    void getAllQueenMoves(int r, int c, std::vector<Move>& moves);
};
