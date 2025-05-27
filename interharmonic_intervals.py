from fractions import Fraction
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("dark_background")

def harm_to_cents(harm):
    return np.round(1200*np.log2(harm) % 1200, 2)

pow_two = [1, 2,4,8,16,32,64,128]

all_harmonics = list(range(1,64))
max_H = 64 
all_harmonics = list(range(1, max_H))
print(all_harmonics)

def reduce(harm):
    left = [p for p in pow_two if p <= harm]
    return Fraction(harm, max(left))


def get_unique_hseries():
    out = []
    for h in all_harmonics:
        rh = reduce(h)
        if rh not in out:
            out.append(rh)
    return out

unique_harms = get_unique_hseries()
unique_harms = [Fraction(1,1), Fraction(2,1)] + unique_harms[1:]
print(unique_harms)

def print_harm(frac):
    print(frac.numerator,'/', frac.denominator,' ', end = '')


viz_padding = 4
xrange = max_H*2 + viz_padding
yrange = max_H*1 + viz_padding

matrix_viz = np.zeros((xrange,yrange))
new_diff = []
for i in range(2,len(unique_harms)):
    print(unique_harms[i])
    new_iteration_intervals = []
    uh_combs = combinations(unique_harms[:i+1],2)
    for uhc in uh_combs:
        #print(uhc)
        diff = max(uhc) / min(uhc)
        if (diff not in unique_harms) and (diff not in new_diff):
            new_diff.append(diff)
            new_iteration_intervals.append(diff)
        # move the smaller one up an octave and divide by the previously biggest one!
        diff =  2*min(uhc) / max(uhc)
        if (diff not in unique_harms) and (diff not in new_diff):
            new_diff.append(diff)
            new_iteration_intervals.append(diff)
    #print([print_harm(nii) for nii in new_iteration_intervals])
    print(new_iteration_intervals)
    cents = [harm_to_cents(float(ii)) for ii in new_iteration_intervals]
    #plt.scatter(cents, [unique_harms[i].numerator]*len(new_iteration_intervals))
    for nii in new_iteration_intervals:
        matrix_viz[nii.numerator, nii.denominator] = unique_harms[i].numerator 



#sns.heatmap(np.flipud(matrix_viz))
sns.heatmap(matrix_viz)
xlab = np.arange(0,yrange,6)
ylab = np.arange(0,xrange,6)
plt.xticks(xlab, labels = xlab)
plt.yticks(ylab, labels = ylab)

plt.ylabel('numerator')
plt.xlabel('denominator')

plt.show()

#print('new difference intervals:')
#print(new_diff)
