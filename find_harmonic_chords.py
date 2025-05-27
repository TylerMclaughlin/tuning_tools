import numpy as np
from zeal import harmonic_to_cents, harmonic_vector
import pandas as pd


def within_degree(input_cents, cents_target):
    if (input_cents <= (cents_target + 50)) and (input_cents >= (cents_target - 50)):
        return True
    else:
        return False


if __name__ == '__main__':
    import os

    hn, hc = harmonic_vector(64)
    degs = list(range(12)) 

    data = []
    for hr_idx, _ in enumerate(hc):
        tonic_hn = hn[hr_idx]
        # tether to the tonic
        new_hc = [(h - hc[hr_idx]) % 1200 for h in hc]
        for di, d in enumerate(degs[1:]):
            deg_cents = d*100 % 1200
            for hi, h in enumerate(new_hc):
                if within_degree(h, deg_cents):
                    data_point = {'tonic' : tonic_hn, 
                                  f'deg' : d,
                                  f'harm_num_match_deg' : hn[hi],
                                  f'harm_cents_match_deg' : np.round(h,4) }
                    data.append(data_point)
    
    df = pd.DataFrame(data)
    
    df.drop_duplicates(subset = 'harm_cents_match_deg',
                       keep = 'first', inplace = True)
    
    if not os.path.exists('harmonic_degrees'):
        os.mkdir('harmonic_degrees')
    df.to_csv('harmonic_degrees/harmonic_intervals.csv', index = False)
    
