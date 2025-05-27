import pandas as pd
import numpy as np

def get_edo_cents(z_edo):
    step = 1200/z_edo
    return [round(step*s,3) for s in range(z_edo)]

def match_twelve_tone_pc(twelve_tone_target, edo_steps):
    """
    twelve_tone_target:  a twelve-tone pitch class int,
    with 0 being the root corresponding to 0 or 1200 cents.
    Example:
    t = get_edo_cents(31)
    match_twelve_tone_pc(3, t)
    [(7, 270.968), (8, 309.677), (9, 348.387)]
    """
    # 100 cents for each chromatic step, +/- 50 cents for upper and lower bounds.
    twelve_tone_target = (twelve_tone_target % 12)
    upper = twelve_tone_target*100 + 50 
    lower = twelve_tone_target*100 - 50 
    matches = [(i, edo_steps[i]) for i in \
            range(len(edo_steps)) if (edo_steps[i] > lower) \
            and (edo_steps[i] < upper)]
    return matches

def test():
    t = get_edo_cents(31)
    print(t)
    r3 = match_twelve_tone_pc(3, t)
    print(r3)

def edo_alternatives(twelve_tone_chord, z_edo):
    """
    returns a dataframe with columns 
    z_edo, twelve_tet_target,
    edo_alt_option, and cents.
    """
    ec = get_edo_cents(z_edo)
    # iterate over pitch classes
    df_rows = [] 
    for pc in twelve_tone_chord:
        matches = match_twelve_tone_pc(pc, ec)
        for m in matches:
            row = {'z_edo' : z_edo, 'twelve_tet_target' : pc,
                    'edo_alt_option' : m[0], 'cents' : m [1]}
            df_rows.append(row)
    return pd.DataFrame(df_rows)

if __name__ == '__main__':
    import sys
    edo12_chord = eval(sys.argv[1])
    z_edo = int(sys.argv[2])
    result = edo_alternatives(edo12_chord, z_edo)
    print(result)
