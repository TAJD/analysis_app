"""Analyse routing results contained in text files.

Thomas Dickson
thomas.dickson@soton.ac.uk
15/03/2019
"""

from mpl_toolkits.basemap import Basemap
from os import listdir
import datetime, re, dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
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
    """Load each txt file in a specified directory as a dataframe."""
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    sort_nicely(onlyfiles)
    dfs = [pd.read_csv(data_path+file, index_col=0) for file in onlyfiles]
    return dfs


def process_ensemble_results(dfs):
    """Return a dataframe which contains the mean and standard deviation of each ensemble for each performance."""
    dates = dfs[0].index
    no_ensembles = len(list(dfs[0]))
    means = np.empty((len(dates), no_ensembles))
    print(means)
    for i, d in enumerate(dfs):
        times = d.values
        for j in d.index:
            means[j, i] = np.mean(times[j, :])
        # print(np.mean(d.values))
    print(means)


if __name__ == "__main__":
    dfs = load_data(data_folder_path)
    dates = dfs[0].index
    vals = dfs[0].values
    dfs_0_mean = dfs[0].mean(axis=1)
    dfs_0_std = dfs[0].std(axis=1)
    print(dfs_0_std)

    # no_ensembles = len(list(dfs[0]))
    # means = np.empty((len(dates), no_ensembles))
    # print(means)
    # for i, d in enumerate(dfs):
    #     times = d.values
    #     for j in d.index:
    #         means[j, i] = np.mean(times[j, :])
    #     # print(np.mean(d.values))
    # print(means)
    # process_ensemble_results(dfs)
    # app.run_server(debug=True)