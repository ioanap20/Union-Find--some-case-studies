# -*- coding: utf-8 -*-

try:
    from uf import Rank_UF
except:
    pass

import random

class Hex:
    def __init__(self, N):
        # size of the board (counting extra rows / columns)
        self.size = N+2
        # initialisation of the board (all hexagons are free)
        self.board = [[0 for j in range(self.size)] for i in range(self.size)]

        # initialisation of the Union-Find object
        nelem = self.size**2
        self.uf = Rank_UF(nelem)

        # first player to play is player 1
        self.player = 1


        l = self.size-1
        # union of sides of each player
        # player 1 is affected to the extra rows, player 2 extra columns
        for i in range(1,self.size-1):
            self.board[0][i] = 1
            self.board[l][i] = 1
            self.board[i][0] = 2
            self.board[i][l] = 2


            if i > 0:
                self.uf.union(self.hex_to_int(1,0), self.hex_to_int(i,0))
                self.uf.union(self.hex_to_int(1,l), self.hex_to_int(i,l))

                self.uf.union(self.hex_to_int(0,1), self.hex_to_int(0,i))
                self.uf.union(self.hex_to_int(l,1), self.hex_to_int(l,i))

        # get the indices in UF of the bottom and top sides of each player
        self.bot = [-1, self.hex_to_int(0,1), self.hex_to_int(1,0)]
        self.top = [-1, self.hex_to_int(l,1), self.hex_to_int(1,l)]

    def hex_to_int(self, i, j):
        return i*(self.size) +j

    def print_board(self):
        for i in range(1, self.size-1):
            print(' '*(i-1),end='')
            for j in range(1, self.size-1):
                if self.board[i][j] == 0:
                    print('_', end='')
                if self.board[i][j] == 1:
                    print('X', end='')
                if self.board[i][j] == 2:
                    print('O', end='')
            print()


    def neighbours(self, i, j):
        directions = [(1, 0),(-1, 0),(0, 1),(0, -1),(1, -1),(-1, 1)]
        neighbors = []
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:  # Check bounds
                if self.board[ni][nj] == self.player:
                    neighbors.append((ni, nj))
        
        return neighbors

    def is_game_over(self):
        if self.uf.is_connected(self.bot[self.player], self.top[self.player]):
            return True
        return False
        
        
    def random_turn(self):
        
        i = random.randint(1, self.size - 2)
        j = random.randint(1, self.size - 2)
        
        #check if the hexagon is free
        while self.board[i][j] != 0:
            i = random.randint(1, self.size-2)
            j = random.randint(1, self.size-2)
        
        self.board[i][j] = self.player
        current_pos = self.hex_to_int(i, j)
        
        for ni, nj in self.neighbours(i, j):
            neighbor_pos = self.hex_to_int(ni, nj)
            self.uf.union(current_pos, neighbor_pos)

        self.player = 3 - self.player

    def random_play(self):
        
        non_free_hex = 0
        
        while not self.is_game_over():
            self.random_turn()
            non_free_hex += 1
        
        return non_free_hex / (self.size - 2)**2
            
        
