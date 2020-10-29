import copy
import random

class checker:
    def __init__(self, side, coords):
        self.side = side
        self.value = 1
        self.coords = coords
        self.possible_moves = []
        
    def moves(self, side, op_side):
        if self.side == "p1":
            x = 1
        else:
            x = -1
            
        #Indiscriminate moveset
        
        possible_moves = [[self.coords[0]-1, self.coords[1]+x], 
                          [self.coords[0]+1, self.coords[1]+x]]
        if self.value == 2:
            possible_moves += [[self.coords[0]-1, self.coords[1]-x], 
                               [self.coords[0]+1, self.coords[1]-x]]
        
        #captures
        
        for i in possible_moves[:]:
            if any(i==x.coords for x in op_side.checkers):
                if not [self.coords[0]+2*(i[0]-self.coords[0]), self.coords[1]+x*2*abs(self.coords[1]-i[1])] in [x.coords for x in op_side.checkers]:
                    possible_moves.remove(i)
                    possible_moves.append([self.coords[0]+2*(i[0]-self.coords[0]), 
                                           self.coords[1]+x*2*abs(self.coords[1]-i[1])])
                else:
                    possible_moves.remove(i)
        
        #remove moves blocked by other same-sided checkers
        
        possible_moves = [i for i in possible_moves if not any(i==x.coords for x in side.checkers)]
        
        #Out of bounds
        
        for i in possible_moves[:]:
            if any(x==9 or x==0 for x in i):
                possible_moves.remove(i)
        
        self.possible_moves = [[self.coords, x] for x in possible_moves]
        
    def moves2(self, side, op_side):
        self.moves(side, op_side)
        dcs = dc_moves(self, side, op_side)
        if dcs != None:
            self.possible_moves += dcs
        A = []
        [A.append(x) for x in self.possible_moves if not x in A]
        self.possible_moves = A
        
        
            
    
                
class player:
    def __init__(self, side):
        self.side = side
        self.checkers = []
        a = [[1, 1], [1, 3], [2, 2], [3, 1], [3, 3], [4, 2], 
             [5, 1], [5, 3], [6, 2], [7, 1], [7, 3], [8, 2]]
        b = [[1, 7], [2, 6], [2, 8], [3, 7], [4, 6], [4, 8], 
             [5, 7], [6, 6], [6, 8], [7, 7], [8, 6], [8, 8]]
        if side == "p1":
            self.checkers = [checker(side, i) for i in a]
        else:
            self.checkers = [checker(side, i) for i in b] 

    def remove_checkers(self, chkr, move):
    
        #works
    
        chkr.coords = move[-1]
        
        if self.side == "p1" and chkr.coords[1] == 8:
            chkr.value = 2
        elif self.side == "ai" and chkr.coords[1] == 1:
            chkr.value = 2
        
        if abs(move[0][0]-move[1][0]) != 1:
            for i in range(len(move)-1):
                for u in self.checkers[:]:
                    if [move[i][0]-(move[i][0]-move[i+1][0])/2, move[i][1]-(move[i][1]-move[i+1][1])/2] == u.coords:
                        self.checkers.remove(u)
    
        
        
a = player("ai")
b = player("p1")
a.checkers = [checker("ai", [5, 1])]
b.checkers = [checker("p1", [6, 2])]

a.checkers[0].moves(a, b)
b.remove_checkers(a.checkers[0], [[5, 1], [7, 3]])

def score(c1, c2):
    
    c1_score = 0
    c2_score = 0

    for i in [c1, c2]:
        for u in i.checkers:
            if i == c1:
                c1_score+=u.value
            else:
                c2_score+=u.value

    return c1_score/c2_score 
        
                

#recursive
#functions for dc

def dc(chkr, c1, c2):
    dcs = []
    chkr.moves(c1, c2)
    capt = [x for x in chkr.possible_moves if abs(x[0][0]-x[1][0]) != 1]
    if capt != None:
        for i in capt:
            c1_copy = player(c1.side)
            c1_copy.checkers = copy.deepcopy([x if x != i[0] else i[1] for x in c1.checkers])
            c2_copy = player(c2.side)
            c2_copy.checkers = copy.deepcopy(c2.checkers)
            c2_copy.checkers.remove([x for x in c2_copy.checkers if [i[0][0]-(i[0][0]-i[1][0])/2, i[0][1]-(i[0][1]-i[1][1])/2] == x.coords][0])
            new_checker = checker(chkr.side, i[1])
            new_checker.moves(c1_copy, c2_copy)
            if [x for x in new_checker.possible_moves if abs(x[0][0]-x[1][0]) != 1] != []:
                dcs+=([i[1]] + [dc(new_checker, c1_copy, c2_copy)])
            else:
                dcs.append(i[1])
    return dcs


def dc_translate(phrase, checker=None):
    
    #should make a list of all possible dcs
    #if next elm is a new list, its a continuation, otherwise it's another option
    
    dcs = []
    
    if checker != None:
        phrase = [checker.coords]+[phrase]
    
    for num, i in enumerate(phrase):
        if num+1 != len(phrase):
            if isinstance(phrase[num+1][0], list):
                for u in dc_translate(phrase[num+1]):
                    dcs.append([i, u])
            else:
                dcs.append(i)
                
        elif isinstance(i[0], int):
            dcs.append(i)
    
    return dcs


def dc_moves(chkr, c1, c2):
    
    x = dc(chkr, c1, c2)
    
    if x != []:
        x = dc_translate(x, chkr)
        dcs = []

        for i in x:
            dcs.append(dc_trtr1(i))

        for i in dcs[:]:
            for u in range(3, len(i)):
                if i[:u] not in dcs:
                    dcs.append(i[:u])

        return dcs
    
    return None

def dc_trtr1(phrase):
    
    dcs = []
    
    for i in phrase:
        if isinstance(i[0], int):
            dcs.append(i)
        else:
            dcs+=dc_trtr1(i)
    
    return dcs


#works


r2d2 = player("ai")
jack = player("p1")
r2d2.checkers = [checker("ai", [5, 3]), checker("ai", [7, 1]), checker("ai", [7, 5])]
jack.checkers = [checker("p1", [2, 6]), checker("p1", [4, 8]), checker("p1", [4, 4]), checker("p1", [4, 6])]

def ts(elm):
    return elm[1]

def choose(ai, p1, lvl=3):
    
    all_results = []
    if ai.checkers != []:
        for i in ai.checkers[:]:
            i.moves2(ai, p1)
            if i.possible_moves != []:
                for u in i.possible_moves[:]:
                    ai_copy = player("ai")
                    ai_copy.checkers = copy.deepcopy(ai.checkers)
                    p1_copy = player("p1")
                    p1_copy.checkers = copy.deepcopy(p1.checkers)
                    p1_copy.remove_checkers([x for x in ai_copy.checkers if x.coords == u[0]][0], u)
                    
                    results = []

                    if p1_copy.checkers == []:
                        return [u, 5000]
                    else:
                        for x in p1_copy.checkers:
                            x.moves2(p1_copy, ai_copy)
                        if not any(x.possible_moves != [] for x in p1_copy.checkers):
                            return [u, 5000]    

                    if p1_copy.checkers != []:
                        for a in p1_copy.checkers[:]:
                            a.moves2(p1, ai)
                            if a.possible_moves != []:
                                for b in a.possible_moves[:]:
                                    ai_copy1 = player("ai")
                                    ai_copy1.checkers = copy.deepcopy(ai_copy.checkers)
                                    p1_copy1 = player("p1")
                                    p1_copy1.checkers = copy.deepcopy(p1_copy.checkers)
                                    ai_copy1.remove_checkers([x for x in p1_copy1.checkers if x.coords == b[0]][0], b)
                                    results.append([u, (score(ai_copy1, p1_copy1) if lvl == 1 else choose(ai_copy1, p1_copy1, lvl-1)[1])])
                                    if ai_copy1.checkers == []:
                                        return [u, 0.00005]
                                    else:
                                        for x in ai_copy1.checkers:
                                            x.moves2(ai_copy1, p1_copy1)
                                        if not any(x.possible_moves != [] for x in ai_copy1.checkers):
                                            return [u, 0.00005]
                    else:
                        return [u, 5000]
                    results = sorted(results, key=ts)
                    
                    if results != []:
                        all_results.append([u, results[0][1]])
                    
    all_results = sorted(all_results, key=ts)
    if all_results != []:
        return all_results[-1]
    
    
def correct_move(ai, p1, move) -> bool:
    if not move[0] in [x.coords for x in p1.checkers]:
        return False

    for i in move[1:]:
        for checker1 in ai.checkers:
            for checker2 in p1.checkers:
                if i == checker1.coords or i == checker2:
                    return False
    return True


        
        
r2d2 = player("ai")
jack = player("p1")
r2d2.checkers = [checker("ai", [4, 4])]
jack.checkers = [checker("p1", [3, 3])]

#Implement breaks

def game():
    p1 = player("p1")
    ai = player("ai")
    
    while True:
        
        p1_move = list(input("Your move:"))
        p1_move = [int(x) for x in p1_move if x.isnumeric()]
        p1_move = [[p1_move[x], p1_move[x+1]] for x in range(len(p1_move)) if x%2==0]

        if correct_move(ai, p1, p1_move):
            chkr1 = [x for x in p1.checkers if x.coords == p1_move[0]][0]
            ai.remove_checkers(chkr1, p1_move)
            
            if ai.checkers != []:
                for i in ai.checkers:
                    i.moves2(ai, p1)
                if all(x.possible_moves == [] for x in ai.checkers):
                    print("P1 wins. Good game.")
                    break
            else:
                print("P1 wins. Good game.")
                break
            
            ai_move = choose(ai, p1)[0]
            chkr2 = [x for x in ai.checkers if x.coords == ai_move[0]][0]
            p1.remove_checkers(chkr2, ai_move)
            
            if p1.checkers != []:
                for i in p1.checkers:
                    i.moves2(ai, p1)
                if all(x.possible_moves == [] for x in p1.checkers):
                    print(str(ai_move)+" \nComputer wins. Good game.")
                    break
            else:
                print(str(ai_move)+" \nComputer wins. Good game.")
                break
            
            print(ai_move)
        else:
            print("Not a valid move! Input a new one.")
            continue
    if bool(input("Play again? (1 for yes, 2 for no):")-1):
        game()
    else:
        return "Goodbye."
    

print(game())
