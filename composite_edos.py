from itertools import combinations_with_replacement
import pandas as pd
import numpy as np

primes = [2,3,5,7,11]

data_rows = []
for l in range(1,5):
    cwr = combinations_with_replacement(primes,l)
    for c in cwr:
        #print(c)
        edo = np.product(c)
        print(f'edo: {edo}' )
        steps = []
        for e in c:
            steps.append(int(edo/e))
            steps.append(e)
        atoms = sorted(list(set(steps)))
        print(atoms)
        data_rows.append({'edo' : edo, 'atoms' : str(atoms)})
df = pd.DataFrame(data_rows)

print(df[df.edo < 128].sort_values(by = 'edo'))

