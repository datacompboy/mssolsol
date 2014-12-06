# solve 3peaks
Game = """
   7     2     A     
  A 7   4 9   J 6    
 J 0 Q K 3 A A 5 8   
9 3 7 Q 5 0 9 3 9 0

246K557JKK828J44068Q6Q32
"""
#[25, -1, 22, -1, 20, -1, 21, -1, -1, -1, -1, 27, 26, 23, 24, 17, 18, -1, 15, -1,
# 14, -1, -1, 19, -1, -1, 11, 9, 10, -1, 16, 8, 4, -1, 13, -1, 7, -1, -1, 6, -1,
# 12, 3, -1, 0, -1, -1, 5, -1, 2, 1]

Game = """
   K     5     6
  J 5   7 8   9 K
 K 6 0 0 4 2 3 6 8
A 7 2 3 8 9 0 9 A 0

QJA98QJ2A2634J5QQ44753K7
"""
#[-1, 27, 25, 24, 23, 22, 19, -1, 20, 26, 14, 21, 13, 15, -1, 17, -1, -1, -1, 12,
# -1, 18, 9, -1, -1, -1, 5, 10, -1, -1, -1, 11, 3, -1, 16, 4, -1, 8, -1, 0, -1,
# -1, -1, 6, 7, -1, 2, 1]

Game = """
   0     6     2
  0 8   K J   8 0
 9 9 6 3 A 2 7 8 4
A A 4 4 7 5 3 A 3 6

J78QJ79592K526KQ05J4KQQ3
"""
#[-1, 27, 23, 21, 26, 20, 24, 17, -1, -1, -1, -1, 11, -1, -1, -1, -1, 25, 14, 19,
# -1, 18, -1, -1, -1, 22, 16, 15, 7, 10, 8, 9, 4, -1, 13, 2, 12, -1, 5, -1, 6,
#  3, -1, 1, -1, 0]

Game = """
   2     9     7
  5 K   J 0   9 4
 K Q Q K 5 9 2 7 9
3 0 A 8 8 7 6 6 J 0

4AAAJ5488KQ3732QJ6465302
"""
#[18, -1, -1, -1, -1, 27, 26, 19, 17, 22, 23, 25, 16, 24, 13, 8, -1, -1, -1, 14,
# 21, -1, -1, 20, 15, -1, 12, 11, 9, 10, 5, 6, 7, -1, -1, -1, -1, -1, 4, -1, -1,
#  3, -1, -1, 2, -1, -1, 0, -1, 1]


#      0        1         2
#    3   4     5  6     7  8    
#  9  10  11 12 13 14 15 16 17
#18 19  20  21 22 23 24 25 26 27

child = [3,5,7,
         9,10, 12,13, 15,16,
         18,19,20, 21,22,23, 24,25,26,
         28,28,28,28,28,28,28,28,28,28]
neigh = {"2":"A3","3":"24","4":"35","5":"46","6":"57","7":"68","8":"79",
         "9":"80","0":"9J","J":"0Q","Q":"JK","K":"QA","A":"K2"}

class State(object):
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
    def move(self,move):
        s=self.state
        new=s[:move]+"x"+s[move+1:31]+s[move]+s[32:]
        return State(new)
    def moves(self,top,avail=None):
        if avail is None:
            avail = self.avail()
        res = []
        for move in avail:
            if self.state[move] in neigh[top]:
                res.append(move)
        return res
    def shift(self):
        return State(self.state[:31]+self.state[33]+"|"+self.state[34:])
    def loose(self):
        return len(self.state)<34
    def top(self):
        return self.state[31]
    def win(self):
        return self.state[0:3]=="xxx"

def readGame(gameStr=""):
    g="".join(gameStr.split())
    pos = g.find("|")
    if pos>=0:
        return State(g)
    else:
        return State(g[:28]+"xx|"+g[28]+"|"+g[29:])

def solveGame(game):
    known = {}
    def solver(game,path):
        if str(game) in known:
            if len(known[str(game)]) <= len(path):
                return
        known[str(game)]=path
        if game.win():
            return path
        for move in game.moves(game.top()):
            res = solver(game.move(move), path+[move])
            if res:
                return res
        if not game.loose():
            res = solver(game.shift(), path+[-1])
            if res:
                return res
        return False
    return solver(game,[])

a = readGame(Game)
#print(str(a))
#print(a.top())
#print(a.avail())
print(a.shift())
#print(a.moves(a.top(),a.avail()))
#print(a.win())
print(solveGame(a))
