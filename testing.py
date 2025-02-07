# -*- coding: utf-8 -*-

from uf import UF_base, Rank_UF
import random
import math

skip_msg = " not implemented, skipping."

### union find

def simple_find(A,p):
    if A[p] == p:
        return p
    else:
        return simple_find(A,A[p])

def check_cycle(A,p):
    try:
        simple_find(A,p)
        return True
    except RecursionError:
        return False
    
def check_cycles(A):
    for p in range(len(A)):
        if not check_cycle(A,p):
            return False
    return True

def check_not_flat(A):
    N = len(A)
    for i in range(N):
        if A[i] not in [i, A[A[i]]]:
            return True
    return False

def rand_tree(A,R):
    N = len(A)
    for _ in range(R):
        i,j = random.randint(0,N-1),random.randint(0,N-1)
        if A[j] == j:
            A[j] = i
        elif A[i] == i:
            A[i] = j

def test_find_aux(N,R):
    count = 0
    print(f"Testing find() with N={N} and {R} repetitions...")
    uf = Rank_UF(N)

    if uf.find(0) is None:
        print(skip_msg)
        return

    rand_tree(uf.A,R)
    while not (check_cycles(uf.A) and check_not_flat(uf.A)):
        count += 1
        uf.A = [i for i in range(N)]
        rand_tree(uf.A,R)

    seq = uf.A

    for i in range(N):
        if simple_find(uf.A, i) != uf.find(i):
            print(f"Fail. find({i}) expected to be {simple_find(uf.A, i)} but {uf.find(i)} returned")
            print("Sequence used for testing: ", [[i,seq[i]] for i in range(N)])
            return count

    for i in range(N):
        if uf.A[i] not in [i, uf.A[uf.A[i]]]:
            print("Fail. Path compression not implemented or wrong")
            return count

    print("Success")
    return count

def test_find (N):
    return test_find_aux(N,17)

def test_random_union():
    N = 100
    print(f"Testing union() with N={N}...")
    uf1 = UF_base(N)
    uf2 = Rank_UF(N)
    uf2.union(0,1)
    if uf2.A[0] == 0 and uf2.A[1] == 1:
        print(skip_msg)
        return
    uf2 = Rank_UF(N)

    pairs_union = []
    for _ in range(10):
        i,j = random.randint(0,N-1),random.randint(0,N-1)
        uf1.union(i,j)
        uf2.union(i,j)
        pairs_union.append([i,j])

    for p in range(N-1):
        for q in range(p+1, N):
            if not (uf1.is_connected(p,q) == uf2.is_connected(p,q)):
                print("Fail")
                print("Sequence of unions: ", pairs_union )
                word = "" if (uf1.is_connected(p,q)) else " not"
                print(f"{p} and {q} must{word} be in the same class")
                print(uf2.A)
                return

    print("Success")


def test_rank_uf():
    print("Testing tutorial example with Rank_UF...")
    N = 12
    uf = Rank_UF(N)
    uf.union(0,1)
    if uf.A[0] == 0 and uf.A[1] == 1:
        print(skip_msg)
        return
    uf = Rank_UF(N)

    uf.union(0,3)
    uf.union(6,3)
    uf.union(9,6)

    uf.union(1,4)
    uf.union(7,1)
    uf.union(10,4)

    uf.union(2,5)
    uf.union(8,2)
    uf.union(11,2)

    expA =  [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    if not uf.A  == expA:
        print('Fail. Expected A=', expA, " gives A=", uf.A)
        return

    expR = [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    if not uf.rank  == expR:
        print('Fail. Expected rank=', expR, " gives rank=", uf.rank)
        return 
    
    print('Success')

### percolation Erdos

import erdos as erdos

have_plt = True
try: 
    import matplotlib.pyplot as plt
except:
    have_plt = False

def test_erdos(R):
    print(f"Testing Erdos_Renyi with {R} repetitions...")
    if erdos.Erdos_Renyi(10) is None:
        print(skip_msg)
        return
    
    global have_plt
    x = range(10, 1000, 10)
    y = []
    for i in x:
        cnt = 0
        for _ in range(R):
            cnt += erdos.Erdos_Renyi(i)
        y.append(cnt/float(R))

    if have_plt:
        plt.plot(x,y, color='red', label='experimental')
        plt.plot(x,[(math.log(N))*(N-1)/2 for N in x], color='blue', label='model')

        plt.legend(loc='upper left')

        plt.xlabel('N')
        plt.ylabel('#Edges')
        plt.title('Erdos-Renyi: number of edges for being connected')
        plt.show()

### percolation
import perco as perco

def test_get_neighbors():
    print('Testing get_vacant_neighbors...')
    N = 6
    G = [[False for _ in range(N)] for _ in range(N)]

    G[2][2] = True


    R = []
    L = perco.get_vacant_neighbors(G, N, 2, 2)
    if L is None:
        print(skip_msg)
        return 
    
    if not R == L:
        print('Fail. Expected ', R, ', got ', L)
        return


    G[3][2] = True
    G[2][3] = True
    G[1][2] = True
    G[2][1] = True
    G[3][3] = True
    R = [[1,2], [2, 1], [3, 2], [2, 3]]
    L = perco.get_vacant_neighbors(G, N, 2, 2)
    for p in L:
        if not p in R:
            print('Fail. Expected ', R, ', got ', L)
            return

    for p in R:
        if not p in L:
            print('Fail. Expected ', R, ', got ', L)
            return

    print('Success')



def test_make_vacant():
    print('Testing make_vacant...')
    N = 6
    G = [[False for _ in range(N)] for _ in range(N)]

    G[2][2] = True
    uf = Rank_UF(N*(N+2))

    perco.make_vacant(uf, G, N, 2, 2)
    if not G[2][2]:
        print('Fail. Grid at position (2,2) is not vacant')
        return

    perco.make_vacant(uf, G, N, 3, 2)
    if not G[3][2] or not uf.is_connected(perco.pos_to_int(N,2,2),perco.pos_to_int(N,3,2)):
        print('Fail. Grid at position (3,2) is not vacant or not joined to (2,2)')
        return

    perco.make_vacant(uf, G, N, 4, 3)
    if not G[4][3] or uf.is_connected(perco.pos_to_int(N,3,2),perco.pos_to_int(N,4,3)):
        print('Fail. Grid at position (4,3) is not vacant or joined to (3,2)')
        return

    print('Success')


### Hex

from Hex import Hex

def test_hex_neighbors():
    print('Testing Hex.neighbours...')

    N = 6
    h = Hex(N)

    h.board[2][2] = 1
    h.board[2][3] = 2
    L = h.neighbours(2,2)
    if L is None:
        print(skip_msg)
        return
    
    E = []
    if L != E:
        print('Fail. Expects ', E,', gets ',L)
        return

    E = [[1,2], [2,1], [3,2], [1,3], [3,1]]
    for p in E:
        h.board[p[0]][p[1]] = 1
    L = h.neighbours(2,2)

    for p in L:
        if p not in E:
            print('Fail. Expects ', E,', gets ',L)
            return

    for p in E:
        if p not in L:
            print('Fail. Expects ', E,', gets ',L)
            return

    print('Success')

def test_hex_winning():
    print('Testing Hex.is_game_over...')

    N = 6
    h = Hex(N)


    L = [[2,2],[1,2],[2,3],[3,3],[4,3],[5,3],[6,3]]
    if h.neighbours(2,2) is None:
        print(skip_msg)
        return
    
    for p in L:
        h.board[p[0]][p[1]] = 1
        for n in h.neighbours(p[0],p[1]):
            h.uf.union(h.hex_to_int(p[0],p[1]), h.hex_to_int(n[0],n[1]))

    if not h.is_game_over():
        print('Fail. Player 1 has won')
        h.print_board()
        return

    h = Hex(N)

    h.player= 2
    for p in L:
        h.board[p[0]][p[1]] = 1
        for n in h.neighbours(p[0],p[1]):
            h.uf.union(h.hex_to_int(p[0],p[1]), h.hex_to_int(n[0],n[1]))


    if h.is_game_over():
        print('Fail. Player 2 has not won')
        h.print_board()
        return

    print('Success')


''' CALLS TO THE TESTING FUNCTIONS '''

''' Union Find '''
print("Question 1")
test_find(100)

print("\nQuestion 2")
# for _ in range(5): test_random_union()
test_random_union()
test_rank_uf()

''' Erdos-Renyi '''
print("\nQuestion 3")
test_erdos(10)

''' Percolation '''
print("\nQuestion 4")
test_get_neighbors()

print("\nQuestion 5")
test_make_vacant()
#N = 500; print("N =",N,", ratio to percolate =", perco.ratio_to_percolate(N))

''' Hex game '''
print("\nQuestion 7")
test_hex_neighbors()

print("\nQuestion 8")
test_hex_winning()


