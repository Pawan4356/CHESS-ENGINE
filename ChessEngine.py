class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bK", "bB", "bQ", "bK", "bB", "bK", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wK", "wB", "wQ", "wK", "wB", "wK", "wR"]
        ]
        self.WhiteToMove = True
        self.MoveLog = []
        self.GameOver = False