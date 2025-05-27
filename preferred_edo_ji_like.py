import pandas as pd

def get_edo(z):
    return [1200/z*i for i in range(0,z)]

# standard config, yields 46
preferred_ranges = [(300, 316), (384, 400), (698, 708)]

# for the r-loop track
preferred_ranges = [(300, 316), (384, 400), (677, 700)]

# C E F G A yields 34 then 39, 51
preferred_ranges = [(386, 398), (492, 502), (698, 708), (884,900)]

# 3rd harmonic (5th), 7th,  11th, 15th harmonic, yields 53 edo  
preferred_ranges = [ (697,707), (967,980), (549, 560), (1086,1096)]

# 3rd harmonic (5th), 11th, 15th harmonic  
preferred_ranges = [ (697,707), (549, 560), (1086,1096)]

# double harmonic scale C Db E F G Ab B
# taken as 17/16, 5/4, 4/3, 3/2, 8/5, 15/8 
preferred_ranges = [ (109,114), (386, 398), (492, 502), (698, 708), (811,816), (1085, 1091)]

# 16/15, the distance between 15th harmonic and unison.
# 111.7 cents
preferred_ranges = [ (110,114), (299,301)]


edo_stats = []
for z in range(7, 100):
    e = get_edo(z)
    edo_score = 0
    for i, (l,r) in enumerate(preferred_ranges):
        match = [interval for interval in e if ((interval < r) and (interval > l))]
        if len(match) > 0:
            edo_score += 1
    edo_stats.append({'edo' : z, 'score' : edo_score})

es_df = pd.DataFrame(edo_stats)

es_df.sort_values(by = ['score','edo'], inplace = True, ascending = False)

print(es_df[es_df.score >= 3])
print(es_df[es_df.score >= 2])
