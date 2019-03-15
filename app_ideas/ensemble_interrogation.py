"""Dash application to analyse routing results contained in text files.

Thomas Dickson
thomas.dickson@soton.ac.uk
15/03/2019
"""

from mpl_toolkits.basemap import Basemap
from os import listdir
import datetime
from os.path import isfile, join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

data_folder_path = "/home/thomas/iridis/sail_route_old/development/polynesian/ensemble_testing/sample_folder/"


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(l):
    return sorted(l, key=alphanum_key)


def load_data(data_path):
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    sort_nicely(onlyfiles)
    dfs = [pd.read_csv(data_path+file, index_col=0) for file in onlyfiles]
    return dfs

