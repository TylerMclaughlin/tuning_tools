"""
Plots the output of 'find_harmonic_chords.py' 
Showing all varieties of Major Thirds, Minor Thirds, etc.
R. Tyler McLaughlin
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fractions import Fraction
plt.style.use("dark_background")


def normalize_fraction(frac):
    while frac < 1:
        frac = frac * 2
    while frac > 2:
        frac = frac / 2
    return frac


def plot_vals(sub_df, xlim, title, color = 'red'):
    # eg:  cents = [267.3, 312.8, 445.2, 389.1, 523.7, 298.4]
    sub_df.sort_values(by = 'harm_cents_match_deg', inplace = True)
    cents = sub_df['harm_cents_match_deg'].values
    #cents = sorted(cents)
    num = sub_df['harm_num_match_deg']
    denom = sub_df['tonic']
    fracts = [Fraction(m,n) for m,n in zip(num,denom)]
    fracts = [normalize_fraction(f) for f in fracts]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Plot points on a horizontal line (y=0 for all points)
    y_pos = [0] * len(cents)
    ax.scatter(cents, y_pos, s=100, c=color, zorder=3)
    
    # Add labels for each point
    for i, num in enumerate(cents):
        ax.annotate(f'{num:.1f}', 
                    (num, 0), 
                    textcoords="offset points", 
                    xytext=(0, 15 + (i % 3) * 15), 
                    ha='center',
                    fontsize=10)
    for i, frac in enumerate(fracts):
        ax.annotate(f'{frac.numerator} / {frac.denominator}', 
                    (cents[i],0),
                    textcoords = "offset points",
                    xytext=(0, -54 + (i % 3) * 15), 
                    ha='center', fontsize = 10)
    
    # Draw the line segment
    ax.axhline(y=0, color='white', linewidth=2, alpha=0.7)
    
    # Set axis limits and labels
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Cents')
    plot_name = f'{title} harmonic series intervals'
    plot_filename = plot_name.replace(' ', '_')
    plot_filename += '.png'
    ax.set_title(plot_name)
    
    # Remove y-axis ticks and labels since we only care about x-values
    ax.set_yticks([])
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('harmonic_degrees/' + plot_filename)
    plt.show()

DEGREE_NAMES = ['Minor Second', 'Major Second', 'Minor Third', 'Major Third',
                'Perfect Fourth', 'Tritone','Perfect Fifth','Minor Sixth',
                'Major Sixth', 'Minor Seventh', 'Major Seventh']

def plot_intervals(data_df, query_degree, color = 'red'):
    plot_min = query_degree*100 - 50
    plot_max = query_degree*100 + 50
    plot_vals(data_df[data_df.deg == query_degree], (plot_min,plot_max),
              DEGREE_NAMES[query_degree - 1], color)


if __name__ == '__main__':
    data = pd.read_csv('harmonic_degrees/harmonic_intervals.csv')
    data = data.query("`harm_num_match_deg` <= 32 and `tonic` <= 32")
    # minor 2rd
    plot_intervals(data, 1, 'green')
    # major 2rd
    plot_intervals(data, 2, 'white')
    # minor 3rd
    plot_intervals(data, 3, 'gray')
    # major 3rd
    plot_intervals(data, 4, 'cyan')

    # perfect 4th 
    plot_intervals(data, 5, 'white')

    # tritone 
    plot_intervals(data, 6, 'purple')

    # perfect 5th
    plot_intervals(data, 7, 'yellow')

    # minor 6th
    plot_intervals(data, 8, 'pink')

    # major 6th
    plot_intervals(data, 9)

    # minor 7th
    plot_intervals(data, 10)

    # major 7th
    plot_intervals(data, 11, 'pink')

