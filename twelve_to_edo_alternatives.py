import pandas as pd
import numpy as np
import mido

def get_edo_cents(z_edo):
    step = 1200/z_edo
    return [round(step*s,3) for s in range(z_edo)]

def match_twelve_tone_pc(twelve_tone_target, edo_steps, precision = None):
    """
    twelve_tone_target:  a twelve-tone pitch class int,
    with 0 being the root corresponding to 0 or 1200 cents.
    precision -- cents amount. 
    if not provided, defaults to one half an edo step
    Example:
    t = get_edo_cents(31)
    match_twelve_tone_pc(3, t)
    [(7, 270.968), (8, 309.677), (9, 348.387)]
    """
    if precision is None:
        precision = 1200./(edo_steps[1] - edo_steps[0])/2
    # 100 cents for each chromatic step, +/- 50 cents for upper and lower bounds.
    # we make the comparison with 12 tone pc 
    # but keep the octave-restored version
    octave, twelve_tone_target_pc = divmod(twelve_tone_target, 12)
    twelve_tone_cents = twelve_tone_target_pc*100 
    upper = twelve_tone_cents + precision 
    lower = twelve_tone_cents - precision 
    matches = []
    for i in range(len(edo_steps)):
        if (edo_steps[i] > lower) and (edo_steps[i] < upper):
            abs_cents_diff = abs(twelve_tone_cents - edo_steps[i])
            # restore the octave of the 12-tone pitch class
            data = (i + (len(edo_steps)*octave),
                    edo_steps[i], abs_cents_diff)
            matches.append(data)
    return matches

def test():
    t = get_edo_cents(31)
    print(t)
    r3 = match_twelve_tone_pc(3, t)
    print(r3)

def edo_alternatives(twelve_tone_chord, z_edo, keep_one = True):
    """
    returns a dataframe with columns 
    z_edo, twelve_tet_target,
    edo_alt_option, and cents.
    """
    ec = get_edo_cents(z_edo)
    # iterate over pitch classes
    dfs = [] 
    for p in twelve_tone_chord:
        print(p)
        matches = match_twelve_tone_pc(p, ec)
        df_rows = []
        for m in matches:
            print(m)
            row = {'z_edo' : int(z_edo), 'twelve_tet_target' : p,
                   'edo_alt_option' : m[0], 'cents' : m [1],
                   'abs_diff' : m[2]}
            df_rows.append(row)
        tt_analog_df = pd.DataFrame(df_rows)
        print(tt_analog_df)
        if keep_one:
            tt_analog_df = tt_analog_df.sort_values(by = ['abs_diff','cents']).iloc[0,:]
        dfs.append(tt_analog_df)
    if keep_one:
        return pd.concat(dfs, axis = 1).T.reset_index(drop = True)
    else:
        return pd.concat(dfs)


def result_df_to_midi(result_df,offset = 20):
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)
    
    for n in result_df.edo_alt_option:
        track.append(mido.Message('note_on', channel=1,
                                  note = int (n + offset), 
                                  velocity=100, 
                                  time=0))
    for i, n in enumerate(result_df.edo_alt_option):
        if i == 0:
            stop_time = 960*2
        else:
            stop_time = 0
        track.append(mido.Message('note_off', channel=1, 
                                  note = int(n + offset),
                                  velocity=100, time=stop_time))
    
    track.append(mido.MetaMessage('end_of_track'))
    return midi

if __name__ == '__main__':
    import sys
    import os
    edo12_chord = eval(sys.argv[1])
    print(edo12_chord)
    z_edo = int(sys.argv[2])
    result = edo_alternatives(edo12_chord, z_edo, keep_one = True)
    result['edo_alt_option'] = result['edo_alt_option'].astype(int) 
    result['twelve_tet_target'] = result['twelve_tet_target'].astype(int)
    print(result)
    midi = result_df_to_midi(result)
    out_dir = f'edo_midi_pack/{z_edo}/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_name = "_".join([str(n) for n in edo12_chord])
    midi.save(f"{out_dir}{out_name}.mid")

# example:  python3 twelve_to_edo_alternatives.py '[12, 11, 7, 4]' 38
