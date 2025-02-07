# -*- coding: utf-8 -*-

try:
    from uf import Rank_UF
except:
    pass

import random

def draw_grid(grid, N):
    for ii in range(N):
        i = ii+1
        for j in range(N):
            if not grid[i][j]:
                print('X', end='')
            else:
                print(' ', end='')
        print()

def pos_to_int(N, i, j):
    int = i * N + j
    return int


def get_vacant_neighbors(G,N,i,j):
    
    positions = []
    
    if i > 0 and G[i-1][j]:
        positions.append([i-1, j])
    if i < N + 1 and G[i+1][j]:
        positions.append([i+1, j])
    if j > 0 and G[i][j-1]:
        positions.append([i, j-1])
    if j < N - 1 and G[i][j+1]:
        positions.append([i, j+1])
    
    return positions


def make_vacant(UF, G, N, i, j):
    neighbors = get_vacant_neighbors(G, N, i, j)
    G[i][j] = True
    current_pos = pos_to_int(N, i, j)
    for ni, nj in neighbors:
        neighbor_pos = pos_to_int(N, ni, nj)
        UF.union(current_pos, neighbor_pos)


def ratio_to_percolate(N):

    G = [[False for _ in range(N)] for _ in range(N + 2)]
    
    for j in range(N):
        G[0][j] = True
        G[N + 1][j] = True

    uf = Rank_UF((N + 2) * N)
    
    for j in range(N - 1):
        uf.union(pos_to_int(N, 0, j), pos_to_int(N, 0, j + 1))  
        uf.union(pos_to_int(N, N + 1, j), pos_to_int(N, N + 1, j + 1)) 


    vacant_count = 0

    while not uf.is_connected(pos_to_int(N, 0, 0), pos_to_int(N, N + 1, 0)):

        i = random.randint(1, N)
        j = random.randint(0, N - 1)  
        
        if not G[i][j]:  
            make_vacant(uf, G, N, i, j)  
            vacant_count += 1  


    return vacant_count / (N*N)


#print(ratio_to_percolate(50))