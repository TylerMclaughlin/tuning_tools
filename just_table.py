import pandas as pd
import numpy as np

def get_cents(interval):
    """
    Takes an interval like 3/2, 8/5, or 19/11 that must be between 1 and 2. 
    Returns the cents (position in octave on a log scale)
    """
    cents = 1200*np.log2(interval)

    return cents
