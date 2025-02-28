import numpy as np
from matplotlib import pyplot as plt
import itertools
from pathlib import Path
import csv
import pandas as pd
from scipy.stats import shapiro, ttest_ind

GRAPH_COLORS = ["#00ff41","#FE53BB","#F5D300","#08F7FE"]

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

def read_summary_csv(filename):
    with open(filename) as f:
        f.readline()
        power = list(map(float, f.readline().split(",")))
        duration = list(map(float, f.readline().split(",")))
        return power, duration

def get_column_from_csv(dict_list, col_name):
    all_cols = []
    for i in range(len(dict_list)):

        y = list(map(lambda x: x[col_name], dict_list[i]))
        all_cols.append(y)
        x = np.array(range(len(y)))*0.1
        
    return np.array(list(itertools.zip_longest(*all_cols, fillvalue=np.nan)))

def get_timestamps_from_results(results):
    timestamps = get_column_from_csv(results, "Time").T
    longest_timestamps = (~np.isnan(timestamps)).cumsum(1).argmax(1).argmax(0)
    t = (timestamps[longest_timestamps] - timestamps[longest_timestamps][0])
    return t.astype(int).tolist()

def reject_outliers(data, m = 3.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def create_watt_plot(watts_arr, timestamps):
    watts_mean = np.nanmean(watts_arr, axis=1)
    watts_min = np.nanmin(watts_arr, axis=1)
    watts_max = np.nanmax(watts_arr, axis=1)
    watts_std = np.nanstd(watts_arr, axis=1)

    plt.style.use("dark_background")
    for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
        plt.rcParams[param] = "0.2"
    for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
        plt.rcParams[param] = "#fff"
    
    df = pd.DataFrame({"Mean": watts_mean, "Min": watts_min, "Max": watts_max}, index=timestamps)
    fig, ax = plt.subplots()
    df.plot(color=GRAPH_COLORS, ax=ax, linewidth=2.0)
    
    # Glow effect
    n_shades = 10
    diff_linewidth = 1.07
    alpha_value = 0.6 / n_shades
    for n in range(1, n_shades+1):
        df.plot(linewidth=2+(diff_linewidth*n),
            alpha=alpha_value,
            legend=False,
            ax=ax,
            color=GRAPH_COLORS)
    
    # Color the areas below the lines:
    # for column, color in zip(df, colors):
    #     ax.fill_between(x=df.index,
    #                     y1=df[column].values,
    #                     y2=[0] * len(df),
    #                     color=color,
    #                     alpha=0.1)
    
    # Fill area of std deviation
    plt.fill_between(df.index, watts_mean - watts_std, watts_mean + watts_std, alpha=0.2, color=GRAPH_COLORS[0])
    
    ax.grid(color="#eee")
    ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
    ax.set_ylim(0)
    
    plt.ylabel("Power consumption (W)")
    plt.xlabel("Time (ms)")

def create_violin_plot(energy_list, labels):
    plt.style.use("dark_background")
    for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
        plt.rcParams[param] = "0.2"
    for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
        plt.rcParams[param] = "#fff"
    
    fig, ax = plt.subplots()


    vplot = plt.violinplot([app_power, browser_power], showmeans=False, showmedians=False, showextrema=False)
    for i, pc in enumerate((vplot["bodies"])):
        pc.set_facecolor(GRAPH_COLORS[i])
        pc.set_edgecolor(GRAPH_COLORS[i])
        pc.set_linewidth(2)
        pc.set_alpha(0.4)
    
    linecolor = "#333"
    bplot = plt.boxplot(energy_list, tick_labels=labels,
        boxprops={"color": linecolor, "linewidth": 2},
        whiskerprops={"color": linecolor},
        medianprops={"color": linecolor},
        capprops={"color": linecolor},
        flierprops={"markeredgecolor": linecolor})
    
    # bplot_items = [bplot[i] for i in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']]
    # bplot_items = [list(row) for row in zip(*bplot_items)]

    # for (i, pcs) in enumerate(bplot_items):
    #     box, whisker, flier, median, cap = pcs
    #     box.set_color("#000")
    #     whisker.set_color("#000")
    #     flier.set_color("#000")
    #     median.set_color("#000")
    #     cap.set_color("#000")

    # Glow effect
    n_shades = 10
    diff_linewidth = 1.07
    alpha_value = 0.6 / n_shades
    for n in range(1, n_shades+1):
        vplot = plt.violinplot([app_power, browser_power], showmeans=False, showmedians=False, showextrema=False)
        for i, pc in enumerate((vplot["bodies"])):
            pc.set_facecolor("none")
            pc.set_edgecolor(GRAPH_COLORS[i])
            pc.set_linewidth(2+(diff_linewidth*n))
            pc.set_alpha(alpha_value)
    
    plt.ylabel("Energy Consumption (J)")

if __name__ == "__main__":
    print("Reading graph data")
    app_results = read_csvs_with_name("results_app_")
    browser_results = read_csvs_with_name("results_browser_")

    app_watts_arr = get_column_from_csv(app_results, "SYSTEM_POWER (Watts)")
    create_watt_plot(app_watts_arr, get_timestamps_from_results(app_results))
    plt.title("Power draw on app (Watts)")
    plt.savefig("app_watts.png", dpi=300)
    plt.show(block=False)

    browser_watts_arr = get_column_from_csv(browser_results, "SYSTEM_POWER (Watts)")
    create_watt_plot(browser_watts_arr, get_timestamps_from_results(browser_results))
    plt.title("Power draw on browser (Watts)")
    plt.savefig("browser_watts.png", dpi=300)
    plt.show(block=False)
    
    app_power, app_duration = read_summary_csv("data/results_app_summary.csv")
    browser_power, browser_duration = read_summary_csv("data/results_browser_summary.csv")
    app_power = reject_outliers(np.array(app_power))
    browser_power = reject_outliers(np.array(browser_power))

    app_normal_test = shapiro(app_power)
    browser_normal_test = shapiro(browser_power)
    print("Shapiro-Wilk test for app:", app_normal_test)
    print("Shapiro-Wilk test for browser:", browser_normal_test)

    power_ttest = ttest_ind(browser_power, app_power, equal_var=False, alternative='two-sided')
    print("Welch's t-test", power_ttest)

    create_violin_plot([app_power, browser_power], ["App", "Browser"])
    plt.title("Energy consumption distribution")
    plt.savefig("distribution.png", dpi=300)
    plt.show(block=False)
