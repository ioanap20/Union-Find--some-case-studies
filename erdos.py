# -*- coding: utf-8 -*-

try:
    from uf import Rank_UF
except:
    pass

import random
import math
 
def Erdos_Renyi(N):
    G = Rank_UF(N)
    
    nb_gen_edges = 0
    
    while G.get_count() > 1:
        (p, q) = (random.randint(0, N-1), random.randint(0, N-1))
        
        if p == q:
            continue
        
        if not G.is_connected(p, q):
            G.union(p, q)
        
        nb_gen_edges += 1
    
    return nb_gen_edges