import tkinter as tk
from chess import Board, Game, Piece, board960, pawn, rook, knight, bishop, queen, king, twoArmiesBoard

SQUARE_SIZE = 80

class ChessGUI:
    def __init__(self, root, gameType=Board, userWhite=True):
        self.root = root
        self.game = Game(userWhite=userWhite, boardType=gameType)
        self.selected = None
        self.legal_moves = []    
        self.canvas = tk.Canvas(root, width=8*SQUARE_SIZE, height=8*SQUARE_SIZE)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_click)

        self.moves_frame = tk.Frame(root, width=150, height=8*SQUARE_SIZE)
        self.moves_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.moves_label = tk.Label(self.moves_frame, text="Moves:", font=("Arial", 12, "bold"))
        self.moves_label.pack()
        
        self.moves_text = tk.Text(self.moves_frame, height=30, width=20, font=("Arial", 10))
        self.moves_text.pack(fill=tk.BOTH, expand=True)
        self.moves_text.config(state=tk.DISABLED)

        self.draw_board()

        self.recent_promo = ''
        self.move_number = 1
        self.current_move_line = ''

    def on_click(self, event):
        self.draw_board()
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        board_row = row
        piece = self.game.board.getloco((board_row, col))
        if isinstance(piece, Piece) and piece.isWhite == self.game.board.whiteTurn:
            self.selected = (board_row, col)
            self.legal_moves = self.game.board.getLegalMovesForPiece(piece)
            print(self.legal_moves)
            for move in self.legal_moves:
                self.canvas.create_oval(
                    move[1]*SQUARE_SIZE + SQUARE_SIZE/2 - 5,
                    move[0]*SQUARE_SIZE + SQUARE_SIZE/2 - 5,
                    move[1]*SQUARE_SIZE + SQUARE_SIZE/2 + 5,
                    move[0]*SQUARE_SIZE + SQUARE_SIZE/2 + 5,
                    outline="black", fill="black")
        elif self.selected and (board_row, col) in self.legal_moves:
            piece = self.game.board.getloco(self.selected)
            dest_piece = self.game.board.getloco((board_row, col))
            pieceTaken = isinstance(dest_piece, Piece)
            castling = False
            promotion = False
            enpassant = False
            if isinstance(piece, king) and abs(col - self.selected[1]) == 2:
                direction = (0, 1) if col > self.selected[1] else (0, -1)
                rook_col = 7 if col > self.selected[1] else 0
                rook_pos = (board_row, rook_col)
                rook_dest = (board_row, self.selected[1] + direction[1])
                self.game.board.switch(self.selected, (board_row, col))
                self.game.board.switch(rook_pos, rook_dest)
                castling = True
            elif isinstance(piece, pawn) and (board_row == 0 or board_row == 7):
                self.game.board.switch(self.selected, (board_row, col))
                promoted_piece = self.promote_pawn(board_row, col)
                if promoted_piece is None:
                    promoted_piece = queen
                self.game.board.promote((board_row, col), promoted_piece)
                self.recent_promo = promoted_piece
                promotion = True
            elif isinstance(piece, pawn) and dest_piece is None and col != self.selected[1]:
                self.game.board.switch(self.selected, (board_row, col))
                captured_pawn_row = board_row + (-1 if not piece.isWhite == self.game.board.userWhite else 1)
                print(f"En passant capture at {(captured_pawn_row, col)}")
                self.game.board.setloco((captured_pawn_row, col), None)
                pieceTaken = True
                enpassant = True
            else:
                if isinstance(self.game.board.getloco((board_row, col)), Piece):
                    pieceTaken = True
                self.game.board.switch(self.selected, (board_row, col))

            def get_move_notation(start, end, pieceTaken=False, promotion=False, castling=False, enpassant=False):
                colToLet = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
                if castling:
                    return "O-O" if end[1] > start[1] else "O-O-O"

                start_file = colToLet[start[1]]
                start_rank = 8 - start[0]
                end_file = colToLet[end[1]]
                end_rank = 8 - end[0]

                if isinstance(piece, pawn):
                    if pieceTaken:
                        move = f"{start_file}x{end_file}{end_rank}"
                    else:
                        move = f"{end_file}{end_rank}"
                    if promotion:
                        promo_char = 'N' if self.recent_promo == knight else self.recent_promo.__name__[0].upper()
                        move += f"={promo_char}"
                    if enpassant:
                        move += ' e.p.'
                    return move

                piece_char = 'N' if isinstance(piece, knight) else piece.__class__.__name__[0].upper()

                same_sources = []
                for i in range(8):
                    for j in range(8):
                        p = self.game.board.getloco((i, j))
                        if p is not None and isinstance(p, piece.__class__) and p.isWhite == piece.isWhite:
                            if (end[0], end[1]) in self.game.board.getLegalMovesForPiece(p):
                                same_sources.append((i, j))

                disamb = ''
                if len(same_sources) > 1:
                    same_files = {colToLet[s[1]] for s in same_sources}
                    same_ranks = {8 - s[0] for s in same_sources}
                    if len(same_files) > 1 and len(same_ranks) > 1:
                        if start_file not in {colToLet[s[1]] for s in same_sources if s != start}:
                            disamb = start_file
                        elif str(start_rank) not in {str(8 - s[0]) for s in same_sources if s != start}:
                            disamb = str(start_rank)
                        else:
                            disamb = f"{start_file}{start_rank}"
                    elif len(same_files) > 1:
                        disamb = start_file
                    elif len(same_ranks) > 1:
                        disamb = str(start_rank)

                take_mark = 'x' if pieceTaken else ''
                move = f"{piece_char}{disamb}{take_mark}{end_file}{end_rank}"
                if promotion:
                    promo_char = 'N' if self.recent_promo == knight else self.recent_promo.__name__[0].upper()
                    move += f"={promo_char}"
                if enpassant:
                    move += ' e.p.'
                return move
                
                      
            
            self.draw_board()
            move_notation = get_move_notation(self.selected, (board_row, col), pieceTaken=pieceTaken, castling = castling, promotion = promotion, enpassant = enpassant)
            
            opponent_in_checkmate = self.game.board.isCheckmate(not self.game.board.whiteTurn)
            opponent_in_check = self.game.board.isInCheck(not self.game.board.whiteTurn)
            
            if opponent_in_checkmate:
                move_notation += '#'
            elif opponent_in_check:
                move_notation += '+'
            
            if self.game.board.whiteTurn:
                self.current_move_line = f"{self.move_number}. {move_notation}"
            else:
                self.current_move_line += f" {move_notation}"
                self.game.movesMade.insert(0, self.current_move_line)
            
            if not self.game.board.whiteTurn:
                self.move_number += 1
            
            self.game.board.whiteTurn = not self.game.board.whiteTurn
            self.update_move_display()
            self.selected = None
            self.legal_moves = []
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

    def update_move_display(self):
        self.moves_text.config(state=tk.NORMAL)
        self.moves_text.delete(1.0, tk.END) 
        
        for move in self.game.movesMade:
            self.moves_text.insert(tk.END, move + "\n")
            print(self.moves_text)
        
        self.moves_text.config(state=tk.DISABLED)

    def promote_pawn(self, row, col):
        popup = tk.Toplevel(self.root)
        popup.title("Promote Pawn")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text="Promote to:", font=("Arial", 18), padx=20, pady=10).pack()

        selected_piece = [None]

        def select_promotion(piece_type):
            selected_piece[0] = piece_type
            popup.destroy()

        for i in [queen, rook, bishop, knight]:
            button = tk.Button(popup, text=i.__name__, command=lambda piece=i: select_promotion(piece))
            button.pack()

        self.root.wait_window(popup)
        return selected_piece[0]
            

        

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                color = "white" if (i+j) % 2 != 0 else "gray"
                self.canvas.create_rectangle(j*SQUARE_SIZE, i*SQUARE_SIZE, (j+1)*SQUARE_SIZE, (i+1)*SQUARE_SIZE, fill=color)
                piece = self.game.board.getloco((i, j))
                if piece is not None:
                    text = piece.__str__()
                    self.canvas.create_text(j*SQUARE_SIZE + SQUARE_SIZE//2, i*SQUARE_SIZE + SQUARE_SIZE//2, text=text, font=("Arial", 40))
        for i in self.game.movesMade[:10]:
            self.canvas.create_rectangle(8*SQUARE_SIZE, 0, 8*SQUARE_SIZE + 150, 8*SQUARE_SIZE, fill="white")
            self.canvas.create_text(8*SQUARE_SIZE + 75, 20 + self.game.movesMade.index(i)*20, text=i, font=("Arial", 12), anchor="w")



class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess")
        self.root.geometry("420x350")

        self.settings = {
            "Play as": ["White", "Black"],
            "Mode": ["Standard", "Chess960", "Two Armies"]
        }

        self.setting_order = list(self.settings.keys())
        self.setting_index = {key: 0 for key in self.settings}

        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        title = tk.Label(self.main_frame, text="Chess", font=("Arial", 28, "bold"))
        title.pack(pady=20)

        self.play_button = tk.Button(
            self.main_frame,
            text="Play",
            font=("Arial", 16),
            width=14,
            command=self.start_game
        )
        self.play_button.pack(pady=10)

        self.settings_button = tk.Button(
            self.main_frame,
            text="Settings",
            font=("Arial", 16),
            width=14,
            command=self.open_settings
        )
        self.settings_button.pack(pady=10)

    def open_settings(self):
        popup = tk.Toplevel(self.root)
        popup.title("Settings")
        popup.geometry("350x250")

        tk.Label(popup, text="Settings", font=("Arial", 20, "bold")).pack(pady=10)

        container = tk.Frame(popup)
        container.pack(fill="both", expand=True, padx=15, pady=10)

        for setting_name in self.setting_order:
            row = tk.Frame(container)
            row.pack(fill="x", pady=8)

            tk.Label(row, text=setting_name + ":", font=("Arial", 12), width=12, anchor="w").pack(side="left")

            value_label = tk.Label(
                row,
                text=self.get_setting_value(setting_name),
                font=("Arial", 12, "bold"),
                width=12
            )
            value_label.pack(side="left", padx=5)

            tk.Button(
                row,
                text="Cycle",
                command=lambda s=setting_name, lbl=value_label: self.cycle_setting(s, lbl)
            ).pack(side="right")

    def get_setting_value(self, setting_name):
        idx = self.setting_index[setting_name]
        return self.settings[setting_name][idx]

    def cycle_setting(self, setting_name, label):
        options = self.settings[setting_name]
        self.setting_index[setting_name] = (self.setting_index[setting_name] + 1) % len(options)
        label.config(text=self.get_setting_value(setting_name))

    def start_game(self):
        userWhite = self.get_setting_value("Play as") == "White"
        boardType = Board if self.get_setting_value("Mode") == "Standard" else board960 if self.get_setting_value("Mode") == "Chess960" else twoArmiesBoard

        self.root.geometry(f"{8*80 + 150}x{8*80}")

        self.main_frame.destroy()
        ChessGUI(self.root, userWhite=userWhite, gameType=boardType)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()