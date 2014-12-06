Game = """
       5
      6 3
     7 2 8
    A K 4 J
   0 K 0 4 0
  6 9 5 J Q K
 8 3 Q J 8 A 5

3082K5249Q79634769J72AQA"""

Game = """
       3
      4 4
     7 Q 2
    3 8 5 Q
   7 2 8 5 A
  Q 0 K 6 A 8
 9 0 J K 0 9 3

4075K6J269J9Q2K6AJ384A57"""

neigh = {"2":"J","3":"0","4":"9","5":"8","6":"7","7":"6","8":"5",
         "9":"4","0":"3","J":"2","Q":"A","K":"","A":"Q","x":"","*":""}
child = [ 1,
          3, 4,
          6, 7, 8,
          10, 11, 12, 13,
          15, 16, 17, 18, 19,
          21, 22, 23, 24, 25, 26,
          28, 28, 28, 28, 28, 28, 28]
idx = [ "00",
        "10", "11",
        "20", "21", "22",
        "30", "31", "32", "33",
        "40", "41", "42", "43", "44",
        "50", "51", "52", "53", "54", "55",
        "60", "61", "62", "63", "64", "65", "66",
        "__", "__", "__",
        "70", "71" ]

class PyramidState(object):
    def __init__(self, s):
        self.state = s
    def __repr__(self):
        return self.state
    def avail(self):
        res = []
        for k in reversed(range(28)):
            ch = child[k]
            if self.state[k]!="x" and self.state[ch:ch+2]=="xx":
                res.append(k)
        return res
    def move(self,movepairs):
        if movepairs[0]==-1:
            return self.shift()[1]
        s=self.state
        for move,_ in movepairs:
            if move<28:
                s=s[:move]+"x"+s[move+1:]
            else:
                s=s[:move]+s[move+1:]
        return PyramidState(s)
    def moves(self,top,avail=None):
        if avail is None:
            avail = self.avail()
        res = []
        topm = list(range(31,37))[0:len(top)]
        for move in avail:
            for pair in avail+topm:
                if self.state[move] in neigh[self.state[pair]]:
                    res.append([(move,self.state[move]),
                                (pair,self.state[pair])])
        return res
    def shift(self):
        thr = self.state[31]
        shifted = self.state[32:]+self.state[31]
        if self.state[32]=="*":
            shifted=shifted[1:]
            while shifted[0] in ["*","x"]:
                shifted = shifted[1:]+shifted[0]
        elif self.state[32]=="x":
            shifted = ""
        newState = PyramidState(self.state[:31]+shifted)
        return (thr, newState)
    def loose(self):
        return len(self.state)<34
    def top(self):
        return self.state[31:33]
    def win(self):
        return self.state[0:3]=="xxx"
    def printMove(self, move):
        if move[0]==-1:
            return "shift*"+str(move[1])
        else:
            return "%s(%s)+%s(%s)" % (idx[move[0][0]], move[0][1],
                                      idx[move[1][0]], move[1][1])

def readPyramidGame(gameStr=""):
    g="".join(gameStr.split())
    pos = g.find("|")
    if pos>=0:
        return PyramidState(g)
    else:
        m = g[:28].replace("K", "x")
        s = g[28:].replace("K", "")+"**x"
        return PyramidState(m+"xx|"+s[0:])

def solveGame(game):
    known = {}
    def solver(game,path):
        if str(game) in known:
            if len(known[str(game)]) <= len(path):
                return
        known[str(game)]=path
        if game.win():
            print(str(game))
            return path
        for move in game.moves(game.top()):
            res = solver(game.move(move), path+[move])
            if res:
                return res
        if not game.loose():
            (shift,newGame) = game.shift()
            res = solver(newGame, path+[(-1,shift)])
            if res:
                return res
        return False
    return solver(game,[])

def printSolve(game,solve):
    print("%12s  %s" % ("", game))
    for move in solve:
        pmove = game.printMove(move)
        game = game.move(move)
        print("%12s  %s" % (pmove, game))

a = readPyramidGame(Game)
print(str(a))
printSolve(a,solveGame(a))
