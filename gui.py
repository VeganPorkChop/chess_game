import tkinter as tk
from chess import Board, Game, Piece, pawn, rook, knight, bishop, queen, king

SQUARE_SIZE = 80

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.selected = None
        self.legal_moves = []    

        self.canvas = tk.Canvas(root, width=8*SQUARE_SIZE, height=8*SQUARE_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def on_click(self, event):
        self.draw_board()
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        board_row = 7 - row
        piece = self.game.board.getloco((board_row, col))
        if isinstance(piece, Piece) and piece.isWhite == self.game.board.whiteTurn:
            self.selected = (board_row, col)
            self.legal_moves = self.game.board.getLegalMovesForPiece(piece)
            for move in self.legal_moves:
                screen_row = 7 - move[0]
                self.canvas.create_oval(
                    move[1]*SQUARE_SIZE + SQUARE_SIZE/2 - 5,
                    screen_row*SQUARE_SIZE + SQUARE_SIZE/2 - 5,
                    move[1]*SQUARE_SIZE + SQUARE_SIZE/2 + 5,
                    screen_row*SQUARE_SIZE + SQUARE_SIZE/2 + 5,
                    outline="black", fill="black")
        elif self.selected and (board_row, col) in self.legal_moves:
            piece = self.game.board.getloco(self.selected)
            
            if isinstance(piece, king) and abs(col - self.selected[1]) == 2:
                direction = (0, 1) if col > self.selected[1] else (0, -1)
                rook_col = 7 if col > self.selected[1] else 0
                rook_pos = (board_row, rook_col)
                rook_dest = (board_row, self.selected[1] + direction[1])
                self.game.board.switch(self.selected, (board_row, col))
                self.game.board.switch(rook_pos, rook_dest)
            elif isinstance(piece, pawn) and (board_row == 0 or board_row == 7):
                self.game.board.switch(self.selected, (board_row, col))
                self.promote_pawn(board_row, col)
            elif isinstance(piece, pawn) and self.game.board.getloco((board_row, col)) is None and col != self.selected[1]:
                self.game.board.switch(self.selected, (board_row, col))
                captured_pawn_row = board_row + (1 if piece.isWhite else -1)
                self.game.board.setloco((captured_pawn_row, col), None)
            else:
                self.game.board.switch(self.selected, (board_row, col))

            
            self.game.board.whiteTurn = not self.game.board.whiteTurn
            self.selected = None
            self.legal_moves = []
            self.draw_board()
            self.check_game_over()

    def check_game_over(self):
        current = self.game.board.whiteTurn
        if self.game.board.isCheckmate(current):
            winner = "Black" if current else "White"
            self.show_message(f"Checkmate! {winner} wins!")
        elif self.game.board.isStalemate(current):
            self.show_message("Stalemate! It's a draw.")
        elif self.game.board.isInCheck(current):
            self.show_message("Check!", temporary=True)

    def show_message(self, text, temporary=False):
        popup = tk.Toplevel(self.root)
        popup.title("")
        tk.Label(popup, text=text, font=("Arial", 24), padx=20, pady=20).pack()
        if temporary:
            popup.after(1500, popup.destroy)
        else:
            tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
    def promote_pawn(self, row, col):
        popup = tk.Toplevel(self.root)
        popup.title("Promote Pawn")
        tk.Label(popup, text="Promote to:", font=("Arial", 18), padx=20, pady=10).pack()

        def select_promotion(piece_type):
            self.game.board.promote((row, col), piece_type)
            popup.destroy()
            self.draw_board()
            self.check_game_over()

        for i in [queen, rook, bishop, knight]:
            button = tk.Button(popup, text=i.__name__, command=lambda piece=i: select_promotion(piece))
            button.pack()

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i+j) % 2 != 0 else "gray"
                self.canvas.create_rectangle(j*SQUARE_SIZE, i*SQUARE_SIZE, (j+1)*SQUARE_SIZE, (i+1)*SQUARE_SIZE, fill=color)
                piece = self.game.board.getloco((7 - i, j))
                if piece is not None:
                    text = piece.__str__()
                    self.canvas.create_text(j*SQUARE_SIZE + SQUARE_SIZE//2, i*SQUARE_SIZE + SQUARE_SIZE//2, text=text, font=("Arial", 40))
                
root = tk.Tk()
test = ChessGUI(root)
root.mainloop()