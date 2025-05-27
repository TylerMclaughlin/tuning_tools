import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.ndimage import gaussian_filter

def get_edo(z : int):
    return np.array([1200/z*i for i in range(0, z)])

def harmonic_to_cents(harmonic : int):
    return 1200*np.log2(harmonic) % 1200 

def harmonic_vector(max_harmonic = 64 ):
    # it's sufficient to keep only odd harmonics.
    h_id = [h for h in range(1, max_harmonic + 1) if (h % 2) != 0]
    h_c = [harmonic_to_cents(h) for h in h_id]
    return np.array(h_id), np.array(h_c) 

def edo_harmonic_difference(edo_vector, harmonic_vector):
    # compute difference matrix with numpy broadcasting
    diff_matrix = edo_vector[:, np.newaxis] - harmonic_vector

    # make all results between -600 and +600 cents 
    diff_matrix[diff_matrix > 600] -= 1200
    return diff_matrix
   
def rotate(z_edo, max_h, nsamples = 10, jnd_threshold = 2.5): 
    e_cents = get_edo(z_edo)
    h_ids, hv = harmonic_vector(max_h)
    print(h_ids)

    e_cents_diff = e_cents[1] - e_cents[0]
    r_vec = np.linspace(0,e_cents_diff, nsamples)
    data = []
    r_index = 0
    for r in r_vec[:-1]:
        rotated = (e_cents + r) % 1200
        m = edo_harmonic_difference(rotated, hv)
        for e_step in range(m.shape[0]):
            for unique_h in range(m.shape[1]): 
                ij_dist = m[e_step, unique_h]
                if np.abs(ij_dist) <= jnd_threshold:
                    harmonic_num = h_ids[unique_h]
                    h_cents = hv[unique_h]
                    data_row = {'edo_step' : e_step, 'harmonic' : harmonic_num,
                                'harmonic_cents' : h_cents, 'dist' : ij_dist,
                                'rotation' : r, 'r_index' : r_index}
                    data.append(data_row)
        r_index += 1
    return pd.DataFrame(data)

def pivot_zeal(zeal_df):        
    """
    gives a binary matrix for each harmonic
    """
    mat = zeal_df.pivot_table(values = 'dist', index=  'harmonic', columns = 'r_index', aggfunc='count').fillna(0)
    return mat


def test_harmonics(max_harmonic = 64):
    h_ids, hv = harmonic_vector(max_harmonic)
    plt.plot(hv,'--bo')
    plt.show()

def test_difference_matrix():
    h_ids, hv = harmonic_vector(16)
    e = get_edo(19)
    m = edo_harmonic_difference(e, hv)
    print(m)

def print_steps(r_index_list, zeal_df):
    """
    Automate the degree-finding part.
    """
    unique_harms = []
    for i in r_index_list:
        cluster_df = zeal_df[zeal_df.r_index == i]
        #print(cluster_df)
        cluster_df = cluster_df.sort_values(by = 'edo_step')
        print(cluster_df.edo_step.values)
        harms = list(cluster_df.harmonic.values) 
        print('harmonics: ', harms)
        unique_harms += harms 
        #print(sorted(edo_steps.values))
    print(Counter(unique_harms))


def main():
    z31 = rotate(31,64, 400)
    z31 = rotate(53,64, 400)
    z31 = rotate(38,64, 400)
    #m = pivot_zeal(z31)
    #z34 = rotate(19,64, 400)
    #z21 = rotate(21,64, 400)
    m = pivot_zeal(z31)
    m = gaussian_filter(m, sigma=4, axes = 1, mode = 'wrap')
    c = sns.clustermap(m, col_cluster= False)
    c.cax.set_visible(False)
    #c.ax_heatmap.set_title('Clustering the rotational alignment of 31-EDO with the first 64 harmonics')
    #c.ax_heatmap.set_title('Clustering the rotational alignment of 19-EDO with the first 64 harmonics')
    plt.show()
    
    #print_steps([8,86,218, 255, 334], z31 )
    # 53
    #print_steps([60, 160, 245, 339, 393], z31 )
    # 38 
    print_steps([30,90,140,180,240,270,340,393], z31 )

if __name__ == '__main__':
    main()

