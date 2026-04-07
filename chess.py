import random

class Piece:
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]
    def __init__(self, isWhite, row, col):
        self.isWhite = isWhite
        self.row = row
        self.col = col
        self.moves = 0

    def __str__(self) -> str:
        return "?"

    def getPosition(self):
        return (self.row, self.col)

    def getLegalMoves(self):
        return print("unassigned piece")
    
    def newpos(self, p, d):
        new_pos = p[0] + d[0], p[1] + d[1]
        return new_pos
    
    def getMovesInDirection(self, piece: "Piece", direction, board: "Board"):
        lst = []
        new_pos = self.newpos(piece.getPosition(), direction)
        while board.getloco(new_pos) != -1:
                loco = board.getloco(new_pos)
                if loco == None:
                    lst.append(new_pos)
                elif isinstance(loco, Piece):
                    if piece.isWhite == loco.isWhite:
                        break
                    elif piece.isWhite != loco.isWhite:
                        lst.append(new_pos)
                        break
                new_pos = self.newpos(new_pos, direction)
        return lst
    
class pawn(Piece):
    def __init__(self, isWhite, row, col):
        super().__init__(isWhite, row, col)
        self.canBeEnPassant = False

    def getLegalMoves(self, board):
        lst = []
        moving_down = (self.isWhite == board.userWhite)
        direction = (1, 0) if not moving_down else (-1, 0)
        take = [(1, 1), (1, -1)] if not moving_down else [(-1, 1), (-1, -1)]

        new_pos = self.newpos(self.getPosition(), direction)
        if board.getloco(new_pos) == None:
            lst.append(new_pos)
        new_pos2 = self.newpos(new_pos, direction)
        if board.getloco(new_pos2) == None and self.moves == 0:
            lst.append(new_pos2)

        for dir in take:
            diagonal = self.newpos(self.getPosition(), dir)
            beside = (self.row, diagonal[1])

            if isinstance(board.getloco(diagonal), Piece) and board.getloco(diagonal).isWhite != self.isWhite:
                lst.append(diagonal)

            beside_piece = board.getloco(beside)
            if (isinstance(beside_piece, pawn) and beside_piece.isWhite != self.isWhite and beside_piece.canBeEnPassant):
                lst.append(diagonal)

        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♙"
        return "♟"
    
class rook(Piece):
    def getLegalMoves(self, board): 
        lst = []
        for i in self.directions[0:4]:
            lst += self.getMovesInDirection(self, i, board)
        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♖"
        return "♜"
    
class knight(Piece):
    def getLegalMoves(self, board):
        lst = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for move in knight_moves:
            new_pos = self.newpos(self.getPosition(), move)
            loco = board.getloco(new_pos)
            if loco == None:
                    lst.append(new_pos)
            if isinstance(loco, Piece):
                if self.isWhite != loco.isWhite:
                    lst.append(new_pos)
                    
        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♘"
        return "♞"
    
class bishop(Piece):
    def getLegalMoves(self, board): 
        lst = []
        for i in self.directions[4:]:
            lst += self.getMovesInDirection(self, i, board)
        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♗"
        return "♝"
    
class queen(Piece):
    def getLegalMoves(self, board): 
        lst = []
        for i in self.directions:
            lst += self.getMovesInDirection(self, i, board)
        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♕"
        return "♛"
    
class king(Piece):
    def getLegalMoves(self, board):
        lst = []

        for i in self.directions:
            np = board.getloco(self.newpos(self.getPosition(), i))
            if isinstance(np, Piece) and np.isWhite != self.isWhite:
                    lst.append(self.newpos(self.getPosition(), i))
            if np == None:
                lst.append(self.newpos(self.getPosition(), i))
        
        for i in self.directions[2:4]:
            moves_in_dir = self.getMovesInDirection(self, i, board)
            if moves_in_dir:
                temp = self.newpos(moves_in_dir[-1], i)
                loco = board.getloco(temp)
                if isinstance(loco, rook) and loco.isWhite == self.isWhite and loco.moves == 0 and self.moves == 0:
                    lst.append(self.newpos(self.newpos(self.getPosition(), i), i))
        return lst
    
    def __str__(self) -> str:
        if self.isWhite:
            return "♔"
        return "♚"
    
class Board:
    def __init__(self, userWhite=True):
        self.userWhite = userWhite
        self.whiteTurn = True
        self.captured = []

        self.piece_map = {
            'R': rook, 'N': knight, 'B': bishop,
            'Q': queen, 'K': king, 'P': pawn
        }

        if userWhite:
            self.board = [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ]
        else:
            self.board = [
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ]

        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell:
                    self.board[row][col] = self.piece_map[cell.upper()](cell.isupper(), row, col)

    def __str__(self):
        for i in range(len(self.board)):
            print()
            for j in range(len(self.board[i])):
                if self.board[i][j] == None:
                    print("   ", end = "")
                    continue
                print(self.board[i][j], end = "  ")
            
        return ""
    
    def getloco(self, pos):
        x, y = pos
        if x >= 8 or y >= 8 or x < 0 or y < 0:
            return -1
        return self.board[x][y]

    def setloco(self, pos, piece):
        x, y = pos
        self.board[x][y] = piece

    def switch(self, p1: tuple, p2: tuple):
        p = self.getloco(p1)
        target = self.getloco(p2)

        if isinstance(target, Piece):
            self.captured.append(target)

        # clear old en passant vulnerability
        for i in range(8):
            for j in range(8):
                piece = self.getloco((i, j))
                if isinstance(piece, pawn):
                    piece.canBeEnPassant = False

        # set new en passant vulnerability only if this pawn moved 2 squares
        if isinstance(p, pawn) and abs(p2[0] - p1[0]) == 2:
            p.canBeEnPassant = True

        p.moves += 1
        p.row, p.col = p2[0], p2[1]
        self.board[p2[0]][p2[1]] = self.board[p1[0]][p1[1]]
        self.board[p1[0]][p1[1]] = None

    def isInCheck(self, isWhite):
        king_pos = None
        for i in range(8):
            for j in range(8):
                p = self.getloco((i, j))
                if isinstance(p, king) and p.isWhite == isWhite:
                    king_pos = (i, j)
                    break

        if king_pos is None:
            return False

        for i in range(8):
            for j in range(8):
                p = self.getloco((i, j))
                if isinstance(p, Piece) and p.isWhite != isWhite:
                    if king_pos in p.getLegalMoves(self):
                        return True
        return False

    def simulateMove(self, p1, p2):
        p = self.getloco(p1)
        target = self.getloco(p2)

        self.board[p2[0]][p2[1]] = p
        self.board[p1[0]][p1[1]] = None
        orig_row, orig_col = p.row, p.col
        p.row, p.col = p2[0], p2[1]

        in_check = self.isInCheck(p.isWhite)

        self.board[p1[0]][p1[1]] = p
        self.board[p2[0]][p2[1]] = target
        p.row, p.col = orig_row, orig_col

        return in_check

    def getAttackedSquares(self, isWhite):
        attacked = set()
        for i in range(8):
            for j in range(8):
                p = self.getloco((i, j))
                if isinstance(p, Piece) and p.isWhite == isWhite:
                    if isinstance(p, king):
                        for d in p.directions:
                            np = p.newpos(p.getPosition(), d)
                            if self.getloco(np) != -1:
                                attacked.add(np)
                    elif isinstance(p, pawn):
                        moving_down = (p.isWhite == self.userWhite)
                        take = [(1, 1), (1, -1)] if not moving_down else [(-1, 1), (-1, -1)]
                        for d in take:
                            attacked.add(p.newpos(p.getPosition(), d))
                    else:
                        for m in p.getLegalMoves(self):
                            attacked.add(m)
        return attacked

    def getLegalMovesForPiece(self, piece):
        raw_moves = piece.getLegalMoves(self)
        legal = []
        for m in raw_moves:
            if not self.simulateMove(piece.getPosition(), m):
                if isinstance(piece, king):
                    target = self.getloco(m)
                    self.board[m[0]][m[1]] = piece
                    self.board[piece.row][piece.col] = None
                    orig_row, orig_col = piece.row, piece.col
                    piece.row, piece.col = m[0], m[1]

                    attacked = self.getAttackedSquares(not piece.isWhite)
                    safe = m not in attacked

                    self.board[orig_row][orig_col] = piece
                    self.board[m[0]][m[1]] = target
                    piece.row, piece.col = orig_row, orig_col

                    if safe:
                        legal.append(m)
                else:
                    legal.append(m)
        return legal
    
    def hasAnyLegalMoves(self, isWhite):
        for i in range(8):
            for j in range(8):
                p = self.getloco((i, j))
                if isinstance(p, Piece) and p.isWhite == isWhite:
                    if self.getLegalMovesForPiece(p):
                        return True
        return False

    def isCheckmate(self, isWhite):
        return self.isInCheck(isWhite) and not self.hasAnyLegalMoves(isWhite)

    def isStalemate(self, isWhite):
        return not self.isInCheck(isWhite) and not self.hasAnyLegalMoves(isWhite)

    def promote(self, p1, new_piece_type):
        p = self.getloco(p1)
        self.board[p1[0]][p1[1]] = new_piece_type(p.isWhite, p1[0], p1[1])

class board960(Board):
    def __init__(self, userWhite=True):
        self.userWhite = userWhite
        self.whiteTurn = True
        self.captured = []
        self.piece_map = {
            'R': rook, 'N': knight, 'B': bishop,
            'Q': queen, 'K': king, 'P': pawn
        }

        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        while True:
            random.shuffle(pieces)
            if pieces.index('K') > pieces.index('R') and pieces.index('K') < pieces.index('R', pieces.index('K') + 1):
                break

        if userWhite:
            self.board = [
                [p.lower() for p in pieces],
                ['p']*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['P']*8,
                pieces,
            ]
        else:
            self.board = [
                pieces,
                ['P']*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['p']*8,
                [p.lower() for p in pieces],
            ]

        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell:
                    self.board[row][col] = self.piece_map[cell.upper()](cell.isupper(), row, col)

class twoArmiesBoard(Board):
    def __init__(self, userWhite=True):
        self.userWhite = userWhite
        self.whiteTurn = True
        self.captured = []

        self.piece_map = {
            'R': rook, 'N': knight, 'B': bishop,
            'Q': queen, 'K': king, 'P': pawn
        }

        if userWhite:
            self.board = [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r','r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p','p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P','P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R','R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ]
        else:
            self.board = [
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R','R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P','P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p','p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r','r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ]

        for row in range(8):
            for col in range(8):
                cell = self.board[row][col]
                if cell:
                    self.board[row][col] = self.piece_map[cell.upper()](cell.isupper(), row, col)


class Game():
    def __init__(self, userWhite=True, boardType=Board):
        self.userWhite = userWhite
        self.board = boardType(userWhite=userWhite)
        self.letToCol = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.piece_map = {'R': rook, 'N': knight, 'B': bishop, 'Q': queen, 'K': king, 'P': pawn}
        self.movesMade = []
    
    def getMove(self):
        move = input("Type your move here: ").strip()
        try:
            take = False
            ep = False
            promo = None
            if "".join(move) in ('0-0', '0-0-0'):
                queenside = "".join(move) == '0-0-0'
                direction = Piece.directions[3 if queenside else 2]

                king_piece = None
                for i in range(8):
                    for j in range(8):
                        p = self.board.getloco((i, j))
                        if isinstance(p, king) and p.isWhite == self.board.whiteTurn:
                            king_piece = p
                            break

                if king_piece is None or king_piece.moves != 0:
                    raise Exception("King has moved, cannot castle")

                king_pos = (king_piece.row, king_piece.col)

                temp = king_piece.newpos(king_pos, direction)
                while self.board.getloco(temp) == None:
                    temp = king_piece.newpos(temp, direction)

                loco = self.board.getloco(temp)
                if not (isinstance(loco, rook)
                        and loco.isWhite == self.board.whiteTurn
                        and loco.moves == 0):
                    raise Exception("Cannot castle: rook missing or has moved")

                rook_pos = temp
                king_dest = king_piece.newpos(king_piece.newpos(king_pos, direction), direction)
                rook_dest = king_piece.newpos(king_pos, direction)

                self.board.switch(king_pos, king_dest)
                self.board.switch(rook_pos, rook_dest)

            if move.endswith(' e.p.'):
                ep = True
                move = move[:-5]

            if '=' in move:
                promo = move[-1]
                move = move[:-2]

            finalCol = self.letToCol[move[-2]]
            finalRow = 8 - int(move[-1])
            move = move[:-2]

            if move.endswith('x'):
                take = True
                move = move[:-1]

            if move and move[0].isupper():
                pieceType = self.piece_map[move[0]]
                move = move[1:]
            else:
                pieceType = pawn

            restCol = None
            restRow = None
            for ch in move:
                if ch in self.letToCol:
                    restCol = self.letToCol[ch]
                elif ch.isdigit():
                    restRow = 8 - int(ch)

            lst = []
            for i in range(8):
                for j in range(8):
                    p = self.board.getloco((i, j))
                    if (isinstance(p, pieceType)
                            and p.isWhite == self.board.whiteTurn
                            and (finalRow, finalCol) in self.board.getLegalMovesForPiece(p)):
                        if restCol is not None and j != restCol:
                            continue
                        if restRow is not None and i != restRow:
                            continue
                        lst.append(p)

            if len(lst) == 0:
                raise Exception("No piece can make that move")
            if len(lst) > 1:
                raise Exception("Ambiguous move, add a file or rank to disambiguate")

            piece = lst[0]

            if ep:
                offset = 1 if self.board.whiteTurn else -1
                ep_piece = self.board.getloco((finalRow + offset, finalCol))
                if not isinstance(ep_piece, pawn) or ep_piece.isWhite == self.board.whiteTurn or ep_piece.moves != 1:
                    raise Exception("Invalid en passant")
                self.board.captured.append(ep_piece)
                self.board.switch((piece.row, piece.col), (finalRow, finalCol))
                self.board.board[ep_piece.row][ep_piece.col] = None

            elif promo:
                self.board.switch((piece.row, piece.col), (finalRow, finalCol))
                self.board.board[finalRow][finalCol] = self.piece_map[promo](self.board.whiteTurn, finalRow, finalCol)

            else:
                self.board.switch((piece.row, piece.col), (finalRow, finalCol))

        except Exception as e:
            print(f"Error: {e}")
            if input("Type 'oops' to try again: ") == 'oops':
                self.getMove()       

    def checkmate(self):
        return self.board.isCheckmate(self.board.whiteTurn)

def move(game: Game):
    print(game.board)
    if game.board.isInCheck(game.board.whiteTurn):
        print("Check!")
    game.getMove()
    game.board.whiteTurn = not game.board.whiteTurn

def main():
    game = Game()
    while True:
        move(game)
        if game.board.isCheckmate(game.board.whiteTurn):
            print(game.board)
            winner = "Black" if game.board.whiteTurn else "White"
            print(f"Checkmate! {winner} wins!")
            break
        if game.board.isStalemate(game.board.whiteTurn):
            print(game.board)
            print("Stalemate! It's a draw.")
            break

if __name__ == "__main__":
    main()