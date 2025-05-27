import numpy as np
from scipy.special import jn_zeros 

def fr_to_cents(freq_ratio):
    return 1200*np.log2(freq_ratio) % 1200

fr_cents_vec = np.vectorize(fr_to_cents)

dim = 3
J_freq = np.zeros((dim,dim))

for i in range(0,dim):
    J_freq[i,:dim] = jn_zeros(i,dim)

cents_matrix = fr_cents_vec(J_freq)
print(cents_matrix)

fl_cm = cents_matrix.flatten()

d = np.diff(fl_cm)
print(d)

for i in range(dim):
    for j in range(dim):
       weight = i*j 

