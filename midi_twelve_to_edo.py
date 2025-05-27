import mido
import mido
import random

twelve_tone_note_names = 'C C# D Eb E F F# G Ab A Bb B'.split()


def test_e31():
    e31dia = [0,5,10,13,18,23,28]
    for i in range(-7,8):
        cycled = [((n + 18*i) % 31) for n in e31dia]
        inters = set(e31dia).intersection(set(cycled)) 
        print(i, len(inters), inters)

test_e31()

# copied from jazz autoreharm code

# MIDI functions

def read_midi(midi_path):
    return mido.MidiFile(midi_path)

def get_unique_notes(midi):
    """
    not pitch classes here, just pure midi notes.
    """
    all_notes = []
    for msg in midi.tracks[0]:
        if msg.type == 'note_on': 
            all_notes.append(msg.note)
    return list(set(all_notes))

def get_all_reharm_options(midi_file, universe, atoms, z = 12):
    midi = read_midi(midi_file) 
    unique_notes = get_unique_notes(midi)
    print(unique_notes)

def get_voiced_reharm_options(midi_file, universe, atoms, match_degree = -1, z = 12):
    """
    Very general given a set of scales, atomic chords, and EDO.
    Only assumes each note (not pitch class) is identified with the same tranposed chord throughout.
    """
    midi = read_midi(midi_file) 
    unique_notes = get_unique_notes(midi)
    reharm_option_dict = {}
    for unique_note in unique_notes:
        reharm_option_dict[unique_note] = match_melody_note(unique_note, universe, atoms, match_degree = match_degree, z = z)
    return reharm_option_dict

def add_chord_on_to_midi_track(track, chord_list, time):
    for note_num in chord_list:
        track.append(mido.Message('note_on', note=note_num, velocity=64, time=32))
    return track



def reharm(input_midi, one_to_one_reharm_dict, atoms, output_midi = 'asdf.mid', z = 12):
    print(one_to_one_reharm_dict)
    in_midi = read_midi(input_midi) 
    out_midi = mido.MidiFile()
    out_midi.ticks_per_beat = in_midi.ticks_per_beat
    track = mido.MidiTrack()
    
    for msg in in_midi.tracks[0]:
        print(f'input_message {msg}')
        if msg.type == 'set_tempo':
            print('Tempo set to', msg.tempo)
        elif msg.type in ['note_on','note_off']: 
            print(msg.note)
            reharm_chord_ = one_to_one_reharm_dict[msg.note]
            print(f'reharm_chord: {reharm_chord_}')
            out_chord_ = get_chord_from_tuple(atoms, reharm_chord_)
            print(f'chord from tuple: {out_chord_}')
            # two octaves down
            # to do:  ensure it doesn't go below 0!  Not sure how to handle that.
            out_chord = [msg.note + n - 1*z for n in out_chord_]
            print(f'final transposed chord: {out_chord}')
            for i, note in enumerate(out_chord):
                # i do this because you only want the first note appended at same time to 
                # have real midi duraation.
                if i == 0: # if first note
                    out_time = msg.time
                else:
                    out_time = 0
                out_message = mido.Message(msg.type,  channel = msg.channel, note=note,\
                                     velocity=msg.velocity,  time = out_time)
                #print(out_message)                     
                track.append(out_message)
        else: # if msg.type not in ['note_on','note_off']: 
            track.append(msg)
    out_midi.tracks.append(track)
    out_midi.save(output_midi)

#('min7', '- 1')

# TO DO: weight probability by the number of scales compatible? 
def random_reharm(input_midi, universe, atoms, output_midi = 'asdf.mid', z = 12):
    all_options = get_all_reharm_options(input_midi, universe, atoms, z)
    print(all_options)
    # randomly choose a reharm for each note in the unique notes reharm options dict.
    chosen_dict = {k : random.choice(list(v.keys())) for k,v in all_options.items()}
    print(chosen_dict)
    reharm(input_midi = input_midi, one_to_one_reharm_dict = chosen_dict, atoms = atoms,\
                        output_midi = output_midi, z = z)


def random_voiced_reharm(input_midi, universe, atoms, output_midi = 'asdf.mid', match_degree = 0, z = 12):
    """
    Makes sure the melody voice matches one of the notes in the atom exactly.  
    Voice number is the degree of the atoms.  Can be negative to index backwards.
    """
    all_voiced_options = get_voiced_reharm_options(input_midi, universe = universe, atoms = atoms, 
                                                   match_degree = match_degree, z = z)
    # randomly choose a reharm for each note in the unique notes reharm options dict.
    chosen_dict = {k : random.choice(list(v.keys())) for k,v in all_voiced_options.items()}
    print(chosen_dict)
    reharm(input_midi = input_midi, one_to_one_reharm_dict = chosen_dict, atoms = atoms,\
                        output_midi = output_midi, z = z)



