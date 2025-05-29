import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from plot_harmonic_chords import normalize_fraction

plt.style.use('dark_background')

df = pd.read_csv('harmonic_degrees/harmonic_intervals.csv')
#df = df[df.tonic <= 32] 
#df = df[df.harm_num_match_deg <= 32]

df.sort_values(by = 'harm_cents_match_deg', inplace = True)

"""
Get the spacing (in cents) between neighboring interharmonic intervals.  
This method uses reverse diffs
"""

# deprecated, fairly hacky way that's quick but possibly slightly incorrect.
def get_diff_rev():
    diff_forward = df.harm_cents_match_deg.diff()
    diff_rev_rev = df.harm_cents_match_deg[::-1].diff()[::-1]
    
    mean_diff = (np.abs(diff_forward) + np.abs(diff_rev_rev))/2
    df['mean_neighbor_diff'] = mean_diff

"""
Get the spacing (in cents) between neighboring interharmonic intervals.  
If first element, just compute forward difference.  
If last element, compute the backward difference
Otherwise, take both diffs and compute the mean. 
"""

# more explicit approach.
cents_array = df.harm_cents_match_deg.values
spacing_array = np.zeros_like(cents_array)
for i, c in enumerate(cents_array):
    if i == (len(cents_array) - 1):
        spacing_array[i] = cents_array[i] - cents_array[i-1]
    elif (i == 0):
        forward_diff = cents_array[i + 1] - cents_array[i] 
        spacing_array[i] = forward_diff
    else:
        forward_diff = cents_array[i + 1] - cents_array[i] 
        backward_diff = cents_array[i] - cents_array[i-1]
        spacing_array[i] =  (forward_diff + backward_diff)/2 


df['mean_neighbor_diff'] = spacing_array 




plt.xlabel('Cents')
plt.ylabel('Distance to neighbor')
# deprecated
#plt.plot(df.harm_cents_match_deg, mean_diff)

plt.plot(cents_array, spacing_array)
plt.title('Distance between inter-harmonic intervals')
plt.savefig('harmonic_degrees/interharmonic_interval_distance.png')
plt.show()


sorted_by_spacing = df.sort_values(by = 'mean_neighbor_diff', ascending = False)
#print(out)

f_list = []
for (n,d) in zip(sorted_by_spacing.harm_num_match_deg, sorted_by_spacing.tonic):
    F = normalize_fraction(Fraction(n,d))
    print(F)
    f_list.append(F)

sorted_by_spacing['fraction'] = f_list
sorted_by_spacing.rename(columns = {'harm_cents_match_deg' : 'cents'}, inplace = True)
sbs = sorted_by_spacing[['fraction', 'cents', 'mean_neighbor_diff']]
sbs.to_csv('harmonic_degrees/interharmonic_intervals_quotient_entropy.csv')
sbs = sbs[sbs.cents < 600]
print(sbs.iloc[:30,:])

