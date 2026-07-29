# CHESS-ENGINE (C++)

This is translation of the ChessEngine made in python in cpp for performance.

SDL2 replaces pygame. The game logic is a direct translation of `ChessEngine.py`
and `ChessMain.py` from the `main` branch, so behaviour matches the Python
version move for move.

```
├── CMakeLists.txt
├── ChessEngine.h     <- GameState + Move        (was ChessEngine.py)
├── ChessEngine.cpp
├── ChessMain.cpp     <- window, input, drawing  (was ChessMain.py)
├── cmake_modules/FindSDL2.cmake
└── images/           <- piece PNGs, copied next to the executable at build time
```

## Building (MSYS2 UCRT64)

Dependencies, if they are not installed yet:

```bash
pacman -S --needed mingw-w64-ucrt-x86_64-SDL2 mingw-w64-ucrt-x86_64-SDL2_image
```

Then:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
```

```bash
cmake --build build
```

```bash
./build/Chess_Engine.exe
```

Run it from a terminal — move notation is printed to stdout, the same as the
Python version.

`cmake_modules/FindSDL2.cmake` is still in the tree if you go back to a
hand-downloaded SDL2, but the build now uses pkg-config: SDL2_image is needed
for the piece PNGs and there is no find module for it here.

## Controls

| Input | Action |
| --- | --- |
| Left click | Select a piece, then click a target square to move |
| Left click same square | Deselect |
| `Z` / scroll up | Undo |
| `Y` / scroll down | Redo |

Selected square is green, quiet moves yellow, captures red.

## How the translation maps

| Python | C++ |
| --- | --- |
| `board[r][c]` is `"wP"` / `"--"` | `Piece { char color; char type; }`, `"--"` becomes `isEmpty()` |
| `self.MoveFunctions[piece](...)` dispatch dict | `switch` on `board[r][c].type` in `getAllPossibleMoves` |
| `getChessNotation()` returns `None` | returns `std::optional<std::string>` |
| `Move` holds a reference to the live board | `const Board*` member, re-read by `getChessNotation()` |
| `move in valid_moves` | `std::find` over `operator==` |
| `p.Surface` + `set_alpha(100)` | `SDL_BLENDMODE_BLEND` + alpha 100 fill rect |
| `clock.tick(15)` | `SDL_Delay(1000 / 15)` |

Two intentional differences:

- **Pawn bounds check.** A pawn that reaches the last rank has nowhere to go,
  and there is no promotion yet. Python's negative indexing silently wrapped a
  white pawn on row 0 around to row 7, and a black pawn on row 7 raised
  `IndexError`. Both are guarded in `getAllPawnMoves`, since either would be
  undefined behaviour in C++.
- **Resizing.** `SDL_RenderSetLogicalSize` keeps the 720x720 board scaling
  correctly when the window is resized, instead of drawing into the corner.

The white/black branches of `getAllRookMoves` were identical apart from which
colour counted as the enemy, so they are one code path here. Move generation
order is unchanged.

The board is drawn white/gray to match the Python version, rather than the
green/cream of the earlier `ChessMain.cpp` on this branch.

## Still to do

Carried over from the Python version — deliberately left unimplemented:

- `getAllValidMoves()` still returns pseudo-legal moves; it does not filter out
  moves that leave the king in check (`// TODO` in `ChessEngine.cpp`)
- no check / checkmate / stalemate detection (`gameOver` is never set)
- no castling, en passant, or pawn promotion
- `redoMove()` does not clear the redo stack when a new move is played
- no best-move search — the `moveCount` bookkeeping in `ChessMain.cpp` also only
  increments on black's move, so numbering drifts if you undo
