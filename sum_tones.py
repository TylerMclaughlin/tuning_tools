import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns

"""
Conclusion:  basically the same as difference tones experiment
harder to visualize though!
"""


def cents_to_hz(cents, root = 100):
    freq_ratio = 2**(cents/1200.)
    top_freq = freq_ratio*root
    return top_freq


root = 100

def get_sum(freq_a, freq_b):
    freq_sum = freq_b + freq_a
    return freq_sum


def differences(new_tones, old_tones):
    new_freq_diffs = []
    for n in new_tones:
        for o in old_tones:
            fd = get_sum(n,o)
            new_freq_diffs.append(fd)
    for p in combinations(new_tones, 2):
        fd = get_sum(p[0],p[1])
        new_freq_diffs.append(fd)
    return new_freq_diffs


root_freq = 100

#all_freqs = np.zeros((17, 1200))
all_freqs = np.zeros((2279, 1200))
#all_freqs = np.zeros((2598061, 1200))


for i in range(1,1200):
    base_freq = cents_to_hz(i)
    first_diff = base_freq + root_freq  
    first_three = [first_diff, base_freq, root_freq]
    n2 = differences([first_diff], [root_freq, base_freq])
    n3 = differences(n2, first_three)
    n4 = differences(n3, n2 +  first_three)
    n5 = differences(n4, n3 + n2 +  first_three)
    #n6 = differences(n5, n4 + n3 + n2 +  first_three)
    #print(len([root_freq, base_freq, first_diff] + n2 ))
    all_freqs[:,i] = n5 + n4 + n3 + n2 + [first_diff, base_freq]
    #all_freqs[:,i] = n6 + n5 + n4 + n3 + n2 + [first_diff, base_freq]

# drop duplicate rows!
print('dropping_duplicates')
all_freqs = np.unique(all_freqs, axis=0)
print(all_freqs.shape)


#m = np.mean(all_freqs,axis = 1)
#plt.hist(m, bins = 300)
for r in range(all_freqs.shape[0]):
    plt.plot(all_freqs[r,:])

#int_freqs = all_freqs.astype(int)
##
#us = np.zeros((1200))
#for r in range(int_freqs.shape[1]):
#    u, c = np.unique(int_freqs[:,r], return_counts = True)
#    dup = u[c > 1]
#    n_dups = len(dup) 
#    us[r] = n_dups
#
#plt.plot(us)
#si = np.argsort(us)[:50]
#si = list(range(1200))[]
#print(si)



#print(np.unique(all_freqs[:,1]))

#sns.heatmap(all_freqs)
#sns.clustermap(all_freqs, col_cluster = False)

plt.show()


