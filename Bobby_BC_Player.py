'''TestAgent1.py
Nobachess, implementation of an agent that can't play
Baroque Chess.

'''
from datetime import datetime, timedelta

# GLOBAL VARIABLES
BEST_STATE = None

def makeMove(currentState, currentRemark, timelimit):
    now = datetime.now()
    global BEST_STATE
    newMoveDesc = 'No move'
    newRemark = "I don't even know how to move!"
    
    # search for 10 seconds
    iter_deep_search(currentState, now + timedelta(0,10))

    best = BEST_STATE
    BEST_STATE = None
    return [[newMoveDesc, best], newRemark]



def nickname():
    return "Bobby F."


def introduce():
    return "I'm an android named Bobby."


def prepare(player2Nickname):
    pass

piece_vals = [0,0,-1,1,-2,2,-2,2,-3,3,-2,2,-10,10,2,2]

def static_eval(state):
    return sum([[piece_vals[j] for j in state.board[i]] for i in state.board])

def out_of_time():
    # TODO: implement
    return False

def iter_deep_search(currentState, endTime):
    #return currentState
    depth = 0
    while datetime.now() < endTime:
        depth += 1
        # whether to minimize or maximize
        opt = -1 if currentState.whose_move == BLACK else 1
        best_state, best_eval = minimax(currentState, depth, opt)
        BEST_STATE = best_state

def minimax(state, depth, opt):
    # base case
    if depth == 0:
        return (state, static_eval(state))

    board = state.board
    child_states = []
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            # Get current piece number
            piece = board[x][y]
            # if current player is the same color as the piece get all child states
            if piece != 0 and who(piece) == state.whose_move:
                child_states += move(state, x, y)

    best_eval = 0
    best = None
    for c_state in child_states:
        new_state, new_eval = minimax(c_state, depth-1, -opt)
        if best == None:
            best = new_state
            best_eval = new_eval
        elif new_eval > opt*best_eval:
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

from copy import deepcopy

class BC_state:
    def __init__(self, old_board=INITIAL, whose_move=WHITE, frozen=[],
            kingPos=[[0,4], [7,4]]):
        self.whose_move = whose_move;
        self.board = [r[:] for r in old_board]
        self.frozen = [(f[0], f[1]) for f in frozen]
        self.kingPos = [p[:] for p in kingPos]

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

    def __copy__(self):
        new_state = BC_state.__init__(self.board, self.whose_move, self.frozen,
            self.kingPos)
        return new_state

def king_search(board):
    wKingPiece = None
    bKingPiece = None
    for i in board:
        for j in board[i]:
            if board[i][j] == INIT_TO_CODE('K'):
                wKingPiece = (i, j)
            elif board[i][j] == INIT_TO_CODE('k'):
                bKingPiece = (i, j)
    return (wKingPiece, bKingPiece)

vec = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def move(state, xPos, yPos):
    # if piece is frozen by opponent's freezer
    if (xPos, yPos) in state.frozen[1-state.whose_move]: return []
    future_states = []
    # get current piece
    piece = state.board[xPos][yPos]
    piece_t = piece - who(piece)
    # loop through directions
    directions = vec[0:4] if piece_t == INIT_TO_CODE['p'] else vec
    for i, j in directions:
        x = xPos
        y = yPos
        # don't move pieces off the board or into another piece
        while x+i >= 0 and y+j >= 0 and x+i <= 7 and y+j <= 7 \
                and new_state.board[x+i][y+j] == 0:
            x += i
            y += j
            # non-aggressive move
            defense = state.__copy__()
            # pick up piece for move
            defense.board[xPos][yPos] = 0
            defense.board[x][y] = piece
            future_state.append(defense)
            # aggressive move
            off = defense.__copy__()
            if piece_t == INIT_TO_CODE['p']:
                future_states.append(pincher_capture(off, x, y))
            # if piece is coordinator
            elif piece_t == INIT_TO_CODE['c']:
                future_states.append(coordinator_capture(off, x, y))
            # if piece is freezer
            elif piece_t == INIT_TO_CODE['f']:
                future_states.append(freezer_capture(off, x, y))
            # if piece is leaper
            elif piece_t == INIT_TO_CODE['l']:
                future_states.append(leaper_capture(off, x, y, i, j))
            # if piece is imitator
            elif piece_t == INIT_TO_CODE['i']:
                future_states.append(imitator_captures(off,x,y,xPos,yPos,i,j))
            # if piece is withdrawer
            elif piece_t == INIT_TO_CODE['w']:
                future_states.append(withdrawer_capture(off, xPos-i, yPos-i))
            # if piece is king
            elif piece_t == INIT_TO_CODE['k']:
                future_states.append(king_capture(off, x, y, x+i, y+i))
    return future_states

def pincher_capture(state, x, y):
    # search surrounding spaces to look for a capture
    for i, j in vec[0:4]:
        try:
            if who(state.board[x+i][y+j]) != who(piece) \
                    and state.board[x+2*i][y+2*j] == piece:
                state.board[x+i][y+j] = 0
        except(IndexError): pass
    return state

def coordinator_capture(state, x, y):
    kx, ky = state.kingPos[state.whose_move]
    # try to coordinate with king to capture
    try:
        if who(state.board[x][ky]) != state.whose_move:
            state.board[x][ky] = 0
        if who(state.board[kx][y]) != state.whose_move:
            state.board[kx][y] = 0
    except(IndexError): pass
    return state

def freezer_capture(state, x, y, x0, y0):
    state.frozen[state.whose_move] = []
    for i, j in vec:
        if x+i >= 0 and y+j >= 0 and x+i <= 7 and y+j <= 7:
            state.frozen[state.whose_move].append((x+i,y+j))
    return state

def leaper_capture(state, x, y, i, j):
    try:
        state.board[x+2*i][y+2*j] = state.board[x][y]
        state.board[x][y] = 0
        state.board[x+i][y+j] = 0
    except(IndexError): pass
    return state   

def imitator_capture(state, x, y, x0, y0, i, j):
    captures = [state.__copy__()]
    # imitate withdrawer
    try:
        if state.board[x0-i][y0-j] + state.whose_move == INIT_TO_CODE['W']:
            state.board[x0-i][y0-j] = 0
    except(IndexError): pass
    kx, ky = state.kingPos[state.whose_move]
    # imitate coordinator
    try:
        if who(state.board[x][ky]) != state.whose_move:
            state.board[x][ky] = 0
        if who(state.board[kx][y]) != state.whose_move:
            state.board[kx][y] = 0
    except(IndexError): pass
    try:
        state.board[x][y] == None
    except: pass
    return state

def withdrawer_capture(state, x, y):
    try: state.board[x][y] = 0
    except: pass
    return state

def king_capture(state, x, y, x1, y1):
    try:
        state.board[x1][y1] = state.board[x][y]
        state.board[x][y] = 0
        state.kingPos[state.whose_move] = (x1, y1)
    except: pass
    return state
