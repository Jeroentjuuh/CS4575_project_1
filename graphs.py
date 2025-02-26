import numpy as np
from matplotlib import pyplot as plt
import itertools
from pathlib import Path
import csv
import pandas as pd

def read_csvs_with_name(name):
    folder_path = Path("./data")
    file_number = 1
    results = []

    while folder_path.joinpath(name + str(file_number) + ".csv").exists():
        file_path = str(folder_path.joinpath(name + str(file_number) + ".csv").absolute())
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            results.append([dict(zip(headers, list(map(float, i)))) for i in reader])
        file_number += 1
    return results

def get_column_from_csv(dict_list, col_name):
    all_cols = []
    for i in range(len(dict_list)):

        y = list(map(lambda x: x[col_name], dict_list[i]))
        all_cols.append(y)
        x = np.array(range(len(y)))*0.1
        
        # plt.plot(x, y)
    return np.array(list(itertools.zip_longest(*all_cols, fillvalue=np.nan)))

def create_watt_plot(watts_arr):
    watts_mean = np.nanmean(watts_arr, axis=1)
    watts_min = np.nanmax(watts_arr, axis=1)
    watts_max = np.nanmin(watts_arr, axis=1)
    watts_std = np.nanstd(watts_arr, axis=1)

    colors = ["#00ff41","#FE53BB","#F5D300","#08F7FE"]
    plt.style.use("dark_background")
    for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
        plt.rcParams[param] = "0.2"
    for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
        plt.rcParams[param] = "#fff"  # bluish dark grey
    
    df = pd.DataFrame({"Mean": watts_mean, "Min": watts_min, "Max": watts_max})
    fig, ax = plt.subplots()
    df.plot(color=colors, ax=ax, linewidth=2.0)
    
    # Redraw the data with low alpha and slighty increased linewidth:
    n_shades = 10
    diff_linewidth = 1.07
    alpha_value = 0.6 / n_shades
    for n in range(1, n_shades+1):
        df.plot(linewidth=2+(diff_linewidth*n),
            alpha=alpha_value,
            legend=False,
            ax=ax,
            color=colors)
    
    # Color the areas below the lines:
    # for column, color in zip(df, colors):
    #     ax.fill_between(x=df.index,
    #                     y1=df[column].values,
    #                     y2=[0] * len(df),
    #                     color=color,
    #                     alpha=0.1)
    
    # Fill area of std deviation
    plt.fill_between(df.index, watts_mean - watts_std, watts_mean + watts_std, alpha=0.2, color=colors[0])
    
    ax.grid(color="#eee")
    ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
    ax.set_ylim(0)
    # 



if __name__ == "__main__":
    print("Reading graph data")
    app_results = read_csvs_with_name("results_app_")
    browser_results = read_csvs_with_name("results_browser_")

    app_watts_arr = get_column_from_csv(app_results, "SYSTEM_POWER (Watts)")
    create_watt_plot(app_watts_arr)
    plt.title("Power draw on app (Watts)")
    plt.show(block=False)

    browser_watts_arr = get_column_from_csv(browser_results, "SYSTEM_POWER (Watts)")
    create_watt_plot(browser_watts_arr)
    plt.title("Power draw on browser (Watts)")
    plt.show()



    



    