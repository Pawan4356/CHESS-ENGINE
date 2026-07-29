/*
 * This is the main file where SDL2 will be used to show the board and colors
 * and pieces on the board.
 *
 * C++ port of ChessMain.py (SDL2 stands in for pygame).
 */

#define SDL_MAIN_HANDLED  // keep a plain main() so console output still works

#include <SDL.h>
#include <SDL_image.h>

#include <algorithm>
#include <array>
#include <iostream>
#include <optional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "ChessEngine.h"

namespace {

constexpr int HEIGHT = 720;
constexpr int WIDTH = 720;
constexpr int DIMENSION = 8;
constexpr int SQ_SIZE = HEIGHT / DIMENSION;
constexpr int MAX_FPS = 15;

using Square = std::pair<int, int>;  // (row, col)

std::unordered_map<std::string, SDL_Texture*> IMAGES;

std::string pieceKey(const Piece& piece) {
    return std::string{piece.color, piece.type};
}

std::string assetDirectory() {
    // Images live next to the executable (CMake copies them there); fall back
    // to the working directory so running from the source tree also works.
    if (char* base = SDL_GetBasePath()) {
        std::string path = std::string(base) + "images";
        SDL_free(base);
        return path;
    }
    return "images";
}

bool loadImages(SDL_Renderer* renderer) {
    const std::array<const char*, 12> pieces = {"wP", "wK", "wQ", "wN", "wB",
                                                "wR", "bP", "bK", "bQ", "bN",
                                                "bB", "bR"};
    const std::string dir = assetDirectory();
    for (const char* piece : pieces) {
        const std::string path = dir + "/" + piece + ".png";
        SDL_Texture* texture = IMG_LoadTexture(renderer, path.c_str());
        if (texture == nullptr) {
            std::cerr << "Failed to load " << path << ": " << IMG_GetError()
                      << '\n';
            return false;
        }
        IMAGES[piece] = texture;
    }
    return true;
}

void destroyImages() {
    for (auto& entry : IMAGES) {
        SDL_DestroyTexture(entry.second);
    }
    IMAGES.clear();
}

// Mirrors `print([m.getChessNotation() for m in valid_moves])`.
void printNotations(const std::vector<Move>& moves) {
    std::cout << '[';
    for (std::size_t i = 0; i < moves.size(); ++i) {
        if (i > 0) {
            std::cout << ", ";
        }
        const std::optional<std::string> notation = moves[i].getChessNotation();
        if (notation) {
            std::cout << '\'' << *notation << '\'';
        } else {
            std::cout << "None";
        }
    }
    std::cout << "]\n";
}

void drawBoard(SDL_Renderer* renderer) {
    const SDL_Color colors[2] = {{255, 255, 255, 255}, {128, 128, 128, 255}};
    for (int r = 0; r < DIMENSION; ++r) {
        for (int c = 0; c < DIMENSION; ++c) {
            const SDL_Color color = colors[(r + c) % 2];
            SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
            const SDL_Rect rect = {c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE};
            SDL_RenderFillRect(renderer, &rect);
        }
    }
}

void highlightSquares(SDL_Renderer* renderer, const GameState& gs,
                      const std::optional<Square>& selectedSQ,
                      const std::vector<Move>& validMoves) {
    if (!selectedSQ) {
        return;
    }
    const int r = selectedSQ->first;
    const int c = selectedSQ->second;

    // only highlight the correct side's piece
    if (gs.board[r][c].color != (gs.whiteToMove ? 'w' : 'b')) {
        return;
    }

    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);

    // highlight selected square
    SDL_SetRenderDrawColor(renderer, 0, 255, 0, 100);
    const SDL_Rect selected = {c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE};
    SDL_RenderFillRect(renderer, &selected);

    // highlight all valid moves for that piece
    for (const Move& move : validMoves) {
        if (move.startRow == r && move.startCol == c) {
            if (gs.board[move.endRow][move.endCol].isEmpty()) {
                SDL_SetRenderDrawColor(renderer, 255, 255, 0, 100);  // quiet move
            } else {
                SDL_SetRenderDrawColor(renderer, 255, 0, 0, 100);  // capture
            }
            const SDL_Rect target = {move.endCol * SQ_SIZE,
                                     move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE};
            SDL_RenderFillRect(renderer, &target);
        }
    }
}

void drawPieces(SDL_Renderer* renderer, const Board& board) {
    for (int r = 0; r < DIMENSION; ++r) {
        for (int c = 0; c < DIMENSION; ++c) {
            const Piece piece = board[r][c];
            if (!piece.isEmpty()) {
                const SDL_Rect rect = {c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE,
                                       SQ_SIZE};
                SDL_RenderCopy(renderer, IMAGES.at(pieceKey(piece)), nullptr,
                               &rect);
            }
        }
    }
}

void drawGameState(SDL_Renderer* renderer, const GameState& gs,
                   const std::optional<Square>& selectedSQ,
                   const std::vector<Move>& validMoves) {
    drawBoard(renderer);
    highlightSquares(renderer, gs, selectedSQ, validMoves);
    drawPieces(renderer, gs.board);
}

}  // namespace

int main() {
    SDL_SetMainReady();

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "SDL_Init failed: " << SDL_GetError() << '\n';
        return 1;
    }
    if ((IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG) == 0) {
        std::cerr << "IMG_Init failed: " << IMG_GetError() << '\n';
        SDL_Quit();
        return 1;
    }

    SDL_Window* window =
        SDL_CreateWindow("Chess", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                         WIDTH, HEIGHT, SDL_WINDOW_RESIZABLE);
    if (window == nullptr) {
        std::cerr << "SDL_CreateWindow failed: " << SDL_GetError() << '\n';
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer =
        SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == nullptr) {
        std::cerr << "SDL_CreateRenderer failed: " << SDL_GetError() << '\n';
        SDL_DestroyWindow(window);
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    // Keeps the 720x720 board coordinate space (and mouse coordinates) intact
    // when the window is resized.
    SDL_RenderSetLogicalSize(renderer, WIDTH, HEIGHT);
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "linear");

    if (!loadImages(renderer)) {
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    GameState gs;
    bool running = true;
    std::optional<Square> selectedSQ;
    std::vector<Square> playerClicks;
    std::vector<Move> validMoves = gs.getAllValidMoves();

    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) {
                running = false;

            } else if (e.type == SDL_MOUSEWHEEL) {
                if (e.wheel.y > 0) {  // undo
                    gs.undoMove();
                    validMoves = gs.getAllValidMoves();
                    printNotations(validMoves);
                } else if (e.wheel.y < 0) {  // redo
                    gs.redoMove();
                    validMoves = gs.getAllValidMoves();
                    printNotations(validMoves);
                }

            } else if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_z) {  // undo
                    gs.undoMove();
                    validMoves = gs.getAllValidMoves();
                } else if (e.key.keysym.sym == SDLK_y) {  // redo
                    gs.redoMove();
                    validMoves = gs.getAllValidMoves();
                }

            } else if (e.type == SDL_MOUSEBUTTONDOWN) {
                if (e.button.button == SDL_BUTTON_LEFT) {
                    const int col = e.button.x / SQ_SIZE;
                    const int row = e.button.y / SQ_SIZE;
                    if (row < 0 || row >= DIMENSION || col < 0 ||
                        col >= DIMENSION) {
                        continue;
                    }

                    if (selectedSQ && *selectedSQ == Square{row, col}) {
                        selectedSQ.reset();
                        playerClicks.clear();
                    } else {
                        selectedSQ = Square{row, col};
                        playerClicks.push_back(*selectedSQ);
                    }

                    if (playerClicks.size() == 2) {
                        const Move move(playerClicks[0].first,
                                        playerClicks[0].second,
                                        playerClicks[1].first,
                                        playerClicks[1].second, gs.board,
                                        gs.whiteToMove);
                        const bool isValid =
                            std::find(validMoves.begin(), validMoves.end(),
                                      move) != validMoves.end();
                        if (isValid) {
                            const std::optional<std::string> notation =
                                move.getChessNotation();
                            if (notation) {
                                if (gs.whiteToMove) {  // White move
                                    std::cout << gs.moveCount << ". "
                                              << *notation << ' ' << std::flush;
                                } else {  // Black move
                                    std::cout << *notation << ' ' << std::flush;
                                    gs.moveCount += 1;
                                }
                            }

                            gs.makeMove(move);
                            validMoves = gs.getAllValidMoves();
                        }

                        playerClicks.clear();
                        selectedSQ.reset();
                    }
                }
            }
        }

        SDL_Delay(1000 / MAX_FPS);
        drawGameState(renderer, gs, selectedSQ, validMoves);
        SDL_RenderPresent(renderer);
    }

    destroyImages();
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    SDL_Quit();
    return 0;
}
