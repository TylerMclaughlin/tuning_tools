from fractions import Fraction
import pandas as pd
import numpy as np
# pitches are represented as ratios, which can be converted
from itertools import combinations_with_replacement

from math import log2, pow
DEBUG = False

# a function modified from John D. Cook's code, via
# https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
A4 = 440
C0 = A4*pow(2, -4.75)
C4 = C0*2**4
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch_from_freq(freq):
    abs_note_num = 12*log2(freq/C0) 
    int_note_num = round(abs_note_num)
    cents = (abs_note_num - int_note_num)*100
    octave = int_note_num // 12
    n = int_note_num % 12
    return note_names[n], octave, cents


def get_edo_frame(n, root = C4):
    # default root is C4.
    edo_columns = ['frequency','pitch_class','octave','cents_from_12_tet']
    edo_index = range(0, n)
    edo_frame = pd.DataFrame(index=edo_index, columns=edo_columns)
    for x in edo_index:
        freq = root*2**float(x/n)
        pc, o, c = pitch_from_freq(freq)
        # populate dataframe
        edo_frame.loc[x,'frequency'] = freq 
        edo_frame.loc[x,'pitch_class'] = pc
        edo_frame.loc[x,'octave'] = o 
        edo_frame.loc[x,'cents_from_12_tet'] = c
    return edo_frame
    

def reduce(pitch_frac):
    # converts a note ratio into one between 1 and 2.
    reduced_frac = pitch_frac
    reduced = False
    while not reduced:
        if reduced_frac < 1: # below unit octave 
            reduced_frac *= 2
        elif reduced_frac >= 2: # above unit octave 
            reduced_frac /= 2
        else:
            reduced = True
    return reduced_frac 
       
def get_upper_triad_fracs(pitch_frac):
    mthird = pitch_frac*5
    pfifth = pitch_frac*3
    return reduce(pitch_frac), reduce(mthird), reduce(pfifth)

def get_lower_triad_fracs(pitch_frac):
    root = pitch_frac/3
    mthird = root*5
    pfifth = root*3
    return reduce(root), reduce(mthird), reduce(pfifth)

def get_just_diatonic_fracs():
    root = Fraction(1,1)
    tonic_triad = get_upper_triad_fracs(root)
    dominant_triad = get_upper_triad_fracs(tonic_triad[2])
    subdominant_triad = get_lower_triad_fracs(tonic_triad[0])
    return subdominant_triad, tonic_triad, dominant_triad

def basis_from_primes(primes_list):
    # Used to calculate tables for 3-limit and 5-limit tuning and generalizations.
    # Makes a basis or collection of orthogonal 'moves' to populate a tuning table.
    # Takes a list of primes, like [3,5,7]
    # and returns [ Fraction(1,1), Fraction(3,1), Fraction(1,3), Fraction(5,1), Fraction(1,5), Fraction(7,1), Fraction(1,7)]
    fracs = [Fraction(1,1)]
    for p in primes_list:
        fracs.append(Fraction(p,1))
        fracs.append(Fraction(1,p))
    return fracs
   
 

def get_n_limit_tuning(list_of_primes, n_steps):
    """
    Returns a list of fractions (notes) and a list of paths (each path is a list of fractions).
    """
    notes = []
    paths = []
    root = Fraction(1,1)
    primes_basis = basis_from_primes(list_of_primes)
    # iterate over all combinations of paths in tuning table.
    for path in combinations_with_replacement(primes_basis, n_steps):
        note = root
        for step in path:
            note *= step 
        notes.append(reduce(note))
        paths.append(path)
    return sorted(list(set(notes))), paths # paths is out of order for now.  use df or someting later

def tot_to_set(*tuples):
    output = []
    for x in tuples:
        for p in x:
            output += p 
    return set(output)

def get_fractions_frame(list_of_fractions, root = C4):
    # default root is C4.
    ff_frac = sorted(list_of_fractions) 
    ff_float = [float(f) for f in ff_frac]
     
    ff_columns = ['fraction','frequency','pitch_class','octave','cents_from_12_tet']
    ff_index = range(0, len(ff_frac))
    ff_frame = pd.DataFrame(index=ff_index, columns=ff_columns)
    for i in ff_index:
        freq = root*ff_float[i]
        pc, o, c = pitch_from_freq(freq)
        # populate dataframe
        ff_frame.loc[i,'fraction'] = ff_frac[i] 
        ff_frame.loc[i,'frequency'] = freq 
        ff_frame.loc[i,'pitch_class'] = pc
        ff_frame.loc[i,'octave'] = o 
        ff_frame.loc[i,'cents_from_12_tet'] = c
    return ff_frame

def just_diatonic_frame(root = C4):
    jdia_fracs =  list(tot_to_set(get_just_diatonic_fracs()))
    return get_fractions_frame(jdia_fracs, root = root)

def get_3_limit_tuning():
    # Pythagorean tuning.  Uses only 5ths, so root is multiplied or divided by 3.
    # Would be derived from vibrating strings if only up to the 3rd harmonic were audible.
    # returns two F#s, off by 23 cents, which is known as the Pythagorean comma.
    fracs, moves = get_n_limit_tuning([3],6)
    return get_fractions_frame(fracs)
    
def get_5_limit_tuning():
    # differs from 5-limit tuning table in wiki because it is diamond shaped (Manhattan distance of 2)
    # not a 3 by 5 rectangle, but missing the corners and extending vertically by one.
    # mine is biased in 3rds.  less like pythagorean tuning.
    fracs, moves = get_n_limit_tuning([3,5],2)
    return get_fractions_frame(fracs)


def get_extended_5_limit_tuning():
    # A superset of the 5-limit tuning table on wiki.
    # includes 1 more step in the fifths direction and 2 more steps in the thirds direction.
    fracs, moves = get_n_limit_tuning([3,5],3)
    return get_fractions_frame(fracs)

def get_frame_n_lim(frac_list, n_steps):
    return get_fractions_frame(get_n_limit_tuning(frac_list,n_steps)[0])

def freq_to_cents_diff(freq1, freq2):
    return 1200*log2(float(freq2)/ freq1)

def norm_freq_to_cents_diff(freq1, freq2):
    # normalize the frequency first so that everything is in the same octave
    # then make sure frequencies are in octave such that they are closest to each other.
    # may mean they are in different octaves
    f1 = reduce(freq1)
    f2 = reduce(freq2)
    # both are now between 1 and 2.
    if (f1 - f2) > 0.5: # if f1 close to 2 and f2 close to 1
       f2 *= 2 
    elif (f2 - f1) > 0.5:
       f1 *= 2 
    return 1200*log2(float(f2)/ f1)

def scale_dist(df1, df2, scale1_name, scale2_name, root_scale1_name):
    # if d2 is not the smaller scale, then correct it.
    if df2.shape[0] > df1.shape[0]:
        df3 = df1
        df1 = df2
        df2 = df3
    # find match for all elements in smaller df
    for i, df2_row in enumerate(df2.itertuples()):
        # set min as the maximum cents diff.
        min_cents = 1200. 
        min_index = None 
        for j, df1_row in enumerate(df1.itertuples()): 
           ij_cents = norm_freq_to_cents_diff(df2_row.frequency, df1_row.frequency) 
           if abs(ij_cents) < abs(min_cents):
               min_cents = ij_cents
               min_index = j
        df2.loc[i,'matched_pitch_class'] = df1.loc[min_index, 'pitch_class']
        df2.loc[i,'matched_frequency'] = df1.loc[min_index, 'frequency']
        if DEBUG:
            print('%'*88)
            print('smaller df:')
            print(df2.loc[i,'pitch_class'])
            print('min_index, ', min_index)
            print('min_cents, ', min_cents)
            print('larger df:')
            print(df1.loc[min_index, 'pitch_class'])
        df2.loc[i,'cents_diff'] = min_cents 

    merged = df1.merge(df2, left_on = 'frequency', right_on = 'matched_frequency', how = 'outer', suffixes = ('_larger', '_smaller'))
    # strategy 2
    #merged = df1.merge(df2, left_on = 'pitch_class', right_on = 'matched_pitch_class', how = 'outer', suffixes = ('_larger', '_smaller'))
    # failed strategy 1 
    #merged['cents_diff'] = merged['cents_x'] - merged['cents_y']
    merged['name_1'] = scale1_name
    merged['name_2'] = scale2_name
    merged['root_1'] = root_scale1_name
    return merged

def distance_edo_n_to_just(n_edo,  just_frame, just_scale_name):
    # iterate over transpositions of edo scale by choosing different 
    #edo root notes from the just scale
    distance_dfs = [] 
    roots = just_frame.frequency.unique()
    for i, edo_root in enumerate(roots): 
        root_scale1_name = just_frame[just_frame.frequency == edo_root].pitch_class.values[0]
        scale1_name = str(n_edo) + "_EDO"
        scale2_name = just_scale_name 
        edo_frame = get_edo_frame(n = n_edo, root = edo_root)
        edo_dist_df = scale_dist(edo_frame, just_frame, scale1_name = scale1_name, \
                  scale2_name = just_scale_name, root_scale1_name = root_scale1_name)
        distance_dfs.append(edo_dist_df) 
    return pd.concat(distance_dfs)

def just_vs_all_edos(min_n = 7, max_n = 20):
    jdia = just_diatonic_frame()
    edo_just_frames = []
    for n in range(min_n, max_n):
        edo_just_frame_n = distance_edo_n_to_just(n, jdia, just_scale_name = 'just diatonic')
        edo_just_frames.append(edo_just_frame_n)
    return pd.concat(edo_just_frames)

def tidy_just_edo_frame(just_edo_df):
    just_edo_df = just_edo_df[~just_edo_df.pitch_class_smaller.isna()]
    just_edo_df = just_edo_df[['name_1', 'name_2', 'root_1', 'pitch_class_smaller', 'cents_diff', 'matched_pitch_class']]
    n_edo = just_edo_df["name_1"].str.split("_", n = 1, expand = True)
    just_edo_df['n_edo'] = n_edo[0]
    just_edo_df.drop(columns =["name_1"], inplace = True) 
    #just_edo_df.to_csv('just_vs_edo_7_to_20.csv')
    just_edo_df.to_csv('data/just_vs_edo_7_to_42.csv')
    

def main():
    jd = just_vs_all_edos(max_n = 43)
    tidy_just_edo_frame(jd)


