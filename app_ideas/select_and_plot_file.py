from os import listdir
import re, dash, h5py, glob
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from os.path import isfile, join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dash.dependencies import Input, Output
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from tkinter import Tk
from tkinter.filedialog import askopenfilename

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()
monthsFmt = mdates.DateFormatter('%M')

def return_data_arrays(h5_file):
    et_results = np.array(h5_file['et_results'])
    journey_times = np.array(h5_file['journey_times'])
    unix_times = np.array(h5_file['start_times'])
    start_times = np.array([datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ') for t in unix_times])
    start_times = np.array([datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ') for t in start_times])
    x_locations = np.array(h5_file['x_locations'])
    y_locations = np.array(h5_file['y_locations'])
    x_results = np.array(h5_file['x_results'])
    y_results = np.array(h5_file['y_results'])
    journey_times[journey_times==0] = np.nan
    return et_results, start_times, journey_times, x_results, y_results, x_locations, y_locations


def load_file():
    """Manually select file to inspect."""
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename
    # f = h5py.File(filename, 'r')
    # return f


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
    files = [h5py.File(data_path+file, 'r') for file in onlyfiles]
    return files


def plot_single_route(start_times, journey_times):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(days)
    ax.set_xlim(start_times.min(), start_times.max())
    
    for i in range(journey_times.shape[0]):
        ax.plot(start_times, journey_times[i, :], label="Perf {0}".format(i))
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
    plt.legend()
    plt.show()


def plot_single_file():
    h5_file = load_file()
    h5_file = h5py.File(h5_file, 'r') 
    et_results, start_times, journey_times, x_results, y_results, x_locations, y_locations = return_data_arrays(h5_file)
    plot_single_route(start_times, journey_times)




def plot_ensemble():
    selected_file = load_file()
    fname = selected_file[0:-9]+"*"+selected_file[-8:]
    sorted_files = sort_nicely(glob.glob(fname))
    h5_files = [h5py.File(f, 'r') for f in sorted_files] 
    et_results, start_times, journey_times, x_results, y_results, x_locations, y_locations = return_data_arrays(h5_files[0])
    journey_times_ensemble = np.array([np.array(f["journey_times"]) for f in h5_files])
    mean_perfs = np.mean(journey_times_ensemble, axis=1)
    mean_start_times = np.mean(mean_perfs, axis=0)
    std_start_times = np.std(mean_perfs, axis=0)
    print(mean_start_times, std_start_times)
    # mean_jts = [np.mean(f[i, :]) for i in range(journey_times_ensemble.shape[0])]
    # print(mean_jts)


if __name__ == '__main__':
    plot_ensemble()