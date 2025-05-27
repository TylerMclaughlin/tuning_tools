"""
These are considered binary scales,
a relatively new concept from the xenharmonic alliance server
"""

import pandas as pd
import numpy as np
import itertools
from collections import Counter
from sympy.solvers.diophantine.diophantine import diop_linear
from sympy.abc import x, y, z


def is_same_pitch_class(scale1, scale2, z_edo):
    scale1 = sorted([d % z_edo for d in scale1])
    for i in range(0, z_edo):
        scale2_transposed = sorted([(d + i) % z_edo for d in scale2])
        if scale2_transposed == scale1:
            return True
    return False

def solve_diophantine(a, b, z_edo):
    """
    finds solutions (x,y) to
    xa + yb = z_edo.  
    equivalent to diophantine equation
    xa + yb - z_edo = 0.
    """
    assert a > b
    solution = diop_linear(a*x + b*y - z_edo) 
    return solution 


def eval_solns(sympy_solution, min_bound = -500, max_bound = 500):
    solns = []
    for t in range(min_bound,max_bound):
        x_eqn = str(sympy_solution[0]).replace('t_0',str(t))
        x_soln = eval(x_eqn)
        y_eqn = str(sympy_solution[1]).replace('t_0',str(t))
        y_soln = eval(y_eqn)
        if (x_soln > 0) and (y_soln >0):
            solns.append((x_soln, y_soln))
    return solns


def get_permutations(a,x,b,y):
    # interval permutations
    i_permutations_ = []
    for x in itertools.permutations([a]*x + [b]*y):
        i_permutations_.append(x)
    i_permutations = list(set(i_permutations_))
    return i_permutations

def get_unique_pitch_classes(permutations, z_edo):
    """
    permutations is a list of tuples like
    [(3,5,3,3,3,5,3,3,3),(3,3,5,3,3,5,3,3,3), ...]
    """
    unique_pitch_classes = []
    unique_intervals = []
    # lower triangular matrix iteration
    for i, p1 in enumerate(permutations):
        s1 = np.cumsum(p1)
        is_duplicate = False
        for j in range(i+1, len(permutations)):
            p2 = permutations[j]
            s2 = np.cumsum(p2)
            b = is_same_pitch_class(s1, s2, z_edo)
            # if a duplicate is encountered, skip it.
            # we'll see it again in i aka p1
            if b:
                is_duplicate = True
                break
        if not is_duplicate:
            s1_sorted = sorted([d % z_edo for d in s1])
            unique_pitch_classes.append(s1_sorted)
            unique_intervals.append(p1)
    return unique_pitch_classes, unique_intervals


def extract_solns(a,b,z_edo): 
    ds = solve_diophantine(a,b,z_edo)
    print(ds)
    d_solns = eval_solns(ds)
    print(d_solns)
    unique_scales = [] 
    unique_intervals = [] 
    for s in d_solns: 
        perms = get_permutations(a,s[0],b,s[1])
        print(f'Evaluating uniqueness in {len(perms)} pitch class sets')
        u_pitch_classes, u_intervals = get_unique_pitch_classes(perms, z_edo) 
        unique_scales += u_pitch_classes
        unique_intervals += u_intervals
    print(f'Found {len(unique_scales)} unique pitch classes (scales)')
    return unique_scales, unique_intervals

#upcs, uis = extract_solns(5,3,31)
#upcs, uis = extract_solns(8,3,34)
#upcs, uis = extract_solns(8,3,46)
#upcs = extract_solns(3,2,19)
# hit 'em subdivisions!
upcs, uis = extract_solns(3,2,20)

for i, x in enumerate(upcs):
    #print("Scale: "," ".join([str(xi) for xi in x]))
    #print("Intervals: ", " ".join([str(x) for x in uis[i]]))
    #print(sorted([f'{k} : {v}' for k,v in Counter(uis[i]).items()]))
    print( " ".join([str(x) for x in uis[i]]))
    


