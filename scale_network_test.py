# min11 scale networks in 31-EDO

min11 = [0,5,8,13,18,26]

def transp(chord, amt, z = 31):
   out = [(x + amt )% z for x in chord]
   return out

for t in range(31):
    t_scale = transp(min11, t , z= 31)
    common_tones = set(min11).intersection(set(t_scale))
    if common_tones:
        print(t, common_tones)


min11_12edo = [0,2,3,5,7,10]
for t in range(12):
    t_scale = transp(min11_12edo, t , z= 12)
    common_tones = set(min11_12edo).intersection(set(t_scale))
    if common_tones:
        print(t, common_tones)
