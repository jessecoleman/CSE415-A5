'''TestAgent1.py
Nobachess, implementation of an agent that can't play
Baroque Chess.

'''
import time
from datetime import datetime, timedelta

# GLOBAL VARIABLES
BEST_STATE = None
TIME_LIMIT_OFFSET = 0.01


def makeMove(currentState, currentRemark, timelimit):
    now = datetime.now()
    global BEST_STATE
    newMoveDesc = 'No move'
    newRemark = "I don't even know how to move!"
    
    # search for 10 seconds
    c_state = State(currentState.board, currentState.whose_move)
    best = iter_deep_search(c_state, now + timedelta(0,timelimit))

    return [[newMoveDesc, best], newRemark]


def nickname():
    return "Bobby F."


def introduce():
    return "I'm an android named Bobby."

def prepare(player2Nickname):
    pass


piece_vals = [0,0,-1,1,-2,2,-2,2,-3,3,-2,2,-10,10,2,2]

def static_eval(state):
    return sum([sum([piece_vals[j] for j in i]) for i in state.board])


def iter_deep_search(currentState, endTime):
    #return currentState
    depth = 0
    while datetime.now() < endTime:
        depth += 1
        # whether to minimize or maximize
        opt = -1 if currentState.whose_move == BLACK else 1

        best_state, best_eval = minimax(currentState, depth, opt, endTime)

        if best_state != None:
            best = best_state
        else:
            break

    return best


def is_over_time(endTime):
    global TIME_LIMIT_OFFSET
    now = datetime.now()
    return (now + timedelta(0, TIME_LIMIT_OFFSET)) >= endTime


def minimax(state, depth, opt, endTime):

    # Time check
    if is_over_time(endTime):
            return (None, 0)

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
        # Time check
        if is_over_time(endTime):
            return (None, 0)

        new_state, new_eval = minimax(c_state, depth-1, -opt, endTime)
        if best == None:
            best = new_state
            best_eval = new_eval
        elif new_eval > opt*best_eval:
            best_eval = new_eval
            best = c_state

    return (best, best_eval)



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

def king_search(board):
    wKingPiece = None
    bKingPiece = None
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == INIT_TO_CODE['K']:
                wKingPiece = (i, j)
            elif board[i][j] == INIT_TO_CODE['k']:
                bKingPiece = (i, j)
    return [wKingPiece, bKingPiece]

def freezer_search(board, whose_move):
    frozen = [[],[]]
    for x in range(0, len(board)):
        for y in range(0, len(board[x])):
            if board[x][y] - who(board[x][y]) == INIT_TO_CODE['f']:
                for i, j in vec:
                    if x+i >= 0 and y+j >= 0 and x+i <= 7 and y+j <= 7:
                        frozen[whose_move].append((x+i, y+j))
    return frozen

class State:
    def __init__(self, old_board=INITIAL, whose_move=WHITE, kingPos=[], frozen=[]):
        self.whose_move = whose_move;
        self.board = [r[:] for r in old_board]
        if len(kingPos) == 0: self.kingPos = king_search(old_board)
        else: self.kingPos = [(k[0], k[1]) for k in kingPos]
        if len(frozen) == 0: self.frozen = freezer_search(old_board, whose_move)
        else:
            self.frozen = []
            self.frozen.append([(f[0], f[1]) for f in frozen[0]])
            self.frozen.append([(f[0], f[1]) for f in frozen[1]])

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
        new_state = State(self.board, self.whose_move,
            self.kingPos, self.frozen)
        return new_state

    def __eq__(self, other):
        if isinstance(other, State):
            for i in range(0, len(self.board)):
                if self.board[i] != other.board[i]: return False
            return True
        return False

vec = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def move(state, xPos, yPos):
    # if piece is frozen by opponent's freezer
    if (xPos, yPos) in state.frozen[1-state.whose_move]: return []
    child_states = []
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
                and state.board[x+i][y+j] == 0:
            x += i
            y += j
            # non-aggressive move
            defense = state.__copy__()
            defense.whose_move = 1 - defense.whose_move
            # pick up piece for move
            defense.board[xPos][yPos] = 0
            defense.board[x][y] = piece
            # aggressive move
            off = defense.__copy__()
            if piece_t == INIT_TO_CODE['p']:
                child_states.append(pincher_capture(off, x, y))
            # if piece is coordinator
            elif piece_t == INIT_TO_CODE['c']:
                child_states.append(coordinator_capture(off, x, y))
            # if piece is freezer
            elif piece_t == INIT_TO_CODE['f']:
                child_states.append(freezer_capture(off, x, y))
            # if piece is leaper
            elif piece_t == INIT_TO_CODE['l']:
                child_states.append(leaper_capture(off, x, y, i, j))
            # if piece is imitator
            elif piece_t == INIT_TO_CODE['i']:
                child_states.append(imitator_capture(off,x,y,xPos,yPos,i,j))
            # if piece is withdrawer
            elif piece_t == INIT_TO_CODE['w']:
                child_states.append(withdrawer_capture(off, xPos-i, yPos-i))
            # if piece is king
            elif piece_t == INIT_TO_CODE['k']:
                child_states.append(king_capture(off, x, y, x+i, y+i))
            if not child_states[-1].__eq__(defense): child_states.append(defense)
    for i in child_states:
        print(i)
        time.sleep(1)
    return child_states

def pincher_capture(state, x, y):
    piece = state.board[x][y]
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

def freezer_capture(state, x, y):
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


if __name__ == "__main__":
    print("Main Method called")
    state = State()
    print(state)

    now = datetime.now()
    new_state = iter_deep_search(state, now + timedelta(0, 10))

    print(new_state)
