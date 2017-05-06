'''TestAgent1.py
Nobachess, implementation of an agent that can't play
Baroque Chess.

'''
import multiprocessing
import time


# Global Variables
BEST_FOUND_STATE = None

def makeMove(currentState, currentRemark, timelimit):
    global BEST_FOUND_STATE
    newMoveDesc = 'No move'
    newRemark = "I don't even know how to move!"

    p = multiprocessing.Process(target=iter_deep_search, name="Iterative Deepening", args=(currentState))
    p.start()

    time.sleep(timelimit - 1)

    p.terminate()
    p.join()

    best = BEST_FOUND_STATE
    BEST_FOUND_STATE = None
    return [[newMoveDesc, best], newRemark]



def nickname():
    return "Nobachess"


def introduce():
    return "I'm Nobachess, I don't play baroque chess at this time."


def prepare(player2Nickname):
    pass

def static_eval(state):
    return 0


def out_of_time():
    # TODO: implement
    return False

def iter_deep_search(currentState):
    return currentState
    global BEST_FOUND_STATE
    depth = 0
    while True:
        depth += 1
        best, best_eval = minimax(currentState, depth)
        BEST_FOUND_STATE = best



def minimax(state, depth):
    if depth == 0:
        return (state, static_eval(state))
    else:
        board = state.board
        child_states = []
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                # Get current piece number
                p_code = board[row][col]
                # if current player is the same color as the piece get all child states
                if who(p_code) == state.whose_move:
                    child_states += PIECE_MOVEMENTS[p_code](state, row, col)

        best_eval = 0
        best = None
        for c_state in child_states:
            new_state, new_eval = minimax(c_state, depth-1)
            if best == None:
                best = new_state
                best_eval = new_eval
            elif state.whose_move == WHITE:
                if new_eval > best_eval:
                    best_eval = new_eval
                    best = c_state
            else:
                if new_eval < best_eval:
                    best_eval = new_eval
                    best = c_state

        return (best, best_eval)



def max(state):
    return

def min(state):
    return

BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p': 2, 'P': 3, 'c': 4, 'C': 5, 'l': 6, 'L': 7, 'i': 8, 'I': 9,
                'w': 10, 'W': 11, 'k': 12, 'K': 13, 'f': 14, 'F': 15, '-': 0}

CODE_TO_INIT = {0: '-', 2: 'p', 3: 'P', 4: 'c', 5: 'C', 6: 'l', 7: 'L', 8: 'i', 9: 'I',
                10: 'w', 11: 'W', 12: 'k', 13: 'K', 14: 'f', 15: 'F'}


def who(piece): return piece % 2

def parse(bs): # bs is board string
    '''Translate a board string into the list of lists representation.'''
    b = [[0,0,0,0,0,0,0,0] for r in range(8)]
    rs9 = bs.split("\n")
    rs8 = rs9[1:] # eliminate the empty first item.
    for iy in range(8):
        rss = rs8[iy].split(' ');
        for jx in range(8):
            b[iy][jx] = INIT_TO_CODE[rss[jx]]
    return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

class BC_state:
    def __init__(self, old_board=INITIAL, whose_move=WHITE):
        new_board = [r[:] for r in old_board]
        self.wKingPiece, self.bKingPiece = king_search(new_board)
        self.board = new_board
        self.whose_move = whose_move;

    def __repr__(self):
        s = ''
        for r in range(8):
            for c in range(8):
                s += CODE_TO_INIT[self.board[r][c]] + " "
            s += "\n"
        if self.whose_move==WHITE: s += "WHITE's move"
        else: s += "BLACK's move"
        s += "\n"
        return s

<<<<<<< HEAD
    def __copy__(self):
        new_state = BC_state.__init__(self.board, self.whose_move)
        return 

def king_search(board):
    wKingPiece = None
    bKingPiece = None
    for i in board:
        for j in board[i]:
            if board[i][j] == INIT_TO_CODE('K'):
                pos[WHITE] = (i, j)
            elif board[i][j] == INIT_TO_CODE('k'):
                pos[BLACK] = (i, j)
    return (wKingPiece, bKingPiece)

vec = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def pincher_moves(state, xPos, yPos):
    future_states = []
    new_state = state.__copy__()
    # pick up piece from board
    piece = new_state.board[xPos][yPos]
    new_state.board[xPos][yPos] = 0
    # search in all four directions
    for i, j in vec[0:4]:
        x = xPos
        y = yPos
        while new_state.board[x][y] == 0:
            x += i
            y += j
            # don't move pieces off the board
            if x < 0 or y < 0 or x > 7 or y > 7: break
            s = new_state.__copy__()
            s.board[x][y] = piece
            # search surrounding spaces to look for a capture
            for ii, jj in vec[0:4]:
                try:
                    if who(s.board[x+ii][y+jj]) != who(piece) \
                            and s.board[x+2*ii][y+2*jj] == piece:
                        s.board[x+ii][y+jj] = 0
                except(IndexError): pass
            future_states.append(s)
    return future_states

def other_moves(state, xPos, yPos):
    future_states = []
        new_state = state.__copy__()
        piece = new_state.board[xPos][yPos]
        new_state.board[xPos][yPos] = 0
        for i, j in vec:
            x = xPos + i
            y = yPos + j
            while new_state.board[x][y] = 0:
                x += i
                y += j
                if x < 0 or y < 0 or x > 7 or y > 7: break
                s = new_state.__copy__()
                s.board[x][y] = piece
                future_states.extend(PIECE_MOVEMENTS[piece](state, x, y))
    return future_states

def coordinator_moves(state, xPos, yPos):
    kx, ky = s.kingPos
    # try to coordinate with king to capture
    try:
        if who(s.board[x][ky]) != who(piece):
            s.board[x][ky] = 0
        if who(s.board[kx][y]) != who(piece):
            s.board[kx][y] = 0
    future_states.append(s)
    return future_states

def freezer_moves(state, x, y):
    return board

def leaper_moves(state, x, y):
    return board

def imitator_moves(state, x, y):
    return board

def withdrawer_moves(state, x, y):
    return state

def king_moves(board, x, y):
    return board

PIECE_MOVEMENTS = {2: lambda x, y, z: print(x, y, z)}
