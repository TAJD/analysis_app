"""Analyse routing results contained in text files.

Thomas Dickson
thomas.dickson@soton.ac.uk
15/03/2019
"""

from os import listdir
import datetime, re, dash
import dash_core_components as dcc
import dash_html_components as html
from os.path import isfile, join
import numpy as np, pandas as pd


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


def return_df_stats(i, df):
    """Return a dataframe of the mean and std of a dataframe"""
    dates = df.index
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    df = pd.concat([mean, std], axis=1)
    df.columns = [str(i)+ "_mean", str(i)+ "_std"]
    return df


if __name__ == "__main__":
    dfs = load_data(data_folder_path)
    dfs_processed = [return_df_stats(i, df) for i, df in enumerate(dfs)]
    print(dfs_processed)
    good_indices = [1]
    property_asel = [dfs_processed[i] for i in good_indices]
    print(property_asel)

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