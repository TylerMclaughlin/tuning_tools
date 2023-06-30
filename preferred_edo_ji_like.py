import pandas as pd

def get_edo(z):
    return [1200/z*i for i in range(0,z)]

preferred_ranges = [(300, 318), (384, 400), (700, 704)]

edo_stats = []
for z in range(7, 200):
    e = get_edo(z)
    edo_score = 0
    for i, (l,r) in enumerate(preferred_ranges):
        match = [interval for interval in e if ((interval < r) and (interval > l))]
        if len(match) > 0:
            edo_score += 1
    edo_stats.append({'edo' : z, 'score' : edo_score})

es_df = pd.DataFrame(edo_stats)

es_df.sort_values(by = 'score', inplace = True, ascending = False)

print(es_df[es_df.score == 3])
