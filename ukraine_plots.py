from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

DATA_DIR = Path(__file__).resolve().parent / "data"             # data folder next to this script
DATE = "2026-09-30"                                             # latest DTM reporting date used in the tables

host = pd.read_csv(DATA_DIR / "ukraine_share_hosted.csv")       # table A: IDPs living in each oblast
origin = pd.read_csv(DATA_DIR / "ukraine_share_origin.csv")     # table B: IDPs coming from each oblast

BLUE = "#2a78d6"                                                # bars with 2022 population base
ORANGE = "#eb6834"                                              # bars with 2014 population base (Crimea, Sevastopol)
INK = "#0b0b0b"                                                 # main text colour
MUTED = "#52514e"                                               # secondary text colour
GRID = "#e4e3df"                                                # light grid lines


def draw(ax, df, value_col, title, xlabel):
    d = df.dropna(subset=[value_col])                           # drop rows without a share (no population)
    d = d.sort_values(value_col, ascending=False).head(15)      # 15 biggest shares
    d = d.iloc[::-1]                                            # reverse: barh draws the first row at the bottom
    colors = [ORANGE if y == 2014 else BLUE for y in d["population_year"]]   # colour by population base year
    bars = ax.barh(d["admin1Name"], d[value_col], color=colors, height=0.6)  # horizontal bars
    for bar, v in zip(bars, d[value_col]):                      # write the value at the end of every bar
        ax.text(v + d[value_col].max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{v:.1f}%", va="center", fontsize=9, color=INK)
    ax.set_xlim(0, d[value_col].max() * 1.15)                   # leave room for the labels
    ax.set_title(title, loc="left", fontsize=12, color=INK)     # panel title
    ax.set_xlabel(xlabel, color=MUTED)                          # x axis label
    ax.xaxis.grid(True, color=GRID)                             # light vertical grid
    ax.set_axisbelow(True)                                      # grid behind the bars
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)                      # remove unneeded frame lines
    ax.tick_params(colors=MUTED, length=0)                      # quiet tick labels


def make_figure(host_col, host_title, host_xlabel, origin_col, origin_title, origin_xlabel, suptitle, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))       # one figure, two panels side by side
    draw(ax1, host, host_col, host_title, host_xlabel)          # left panel: where IDPs live
    draw(ax2, origin, origin_col, origin_title, origin_xlabel)  # right panel: where IDPs come from
    ax2.legend(handles=[Patch(color=BLUE, label="Population base: 1 Jan 2022"),
                        Patch(color=ORANGE, label="Population base: 1 Jan 2014")],
               frameon=False, loc="lower right")                # legend for the two colours
    fig.suptitle(suptitle, x=0.01, ha="left", fontsize=14, color=INK)   # figure title
    fig.text(0.01, 0.01, "Sources: IOM DTM (registration data); State Statistics Service of Ukraine. "
             "Population is pre-war (2022; 2014 for Crimea and Sevastopol).",
             fontsize=9, color=MUTED)                           # source note
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))                   # leave space for title and note
    fig.savefig(DATA_DIR.parent / filename, dpi=150)            # save the picture next to the scripts
    print("Saved", filename)


# Figure 1: ALL registered IDPs (including people who moved inside their own oblast)
make_figure("hosted_pct_of_pop",
            "A. All IDPs living in the oblast",
            "IDPs living in the oblast, % of its population",
            "displaced_pct_of_pop",
            "B. All IDPs who came from the oblast",
            "IDPs from the oblast, % of its population",
            f"Ukraine: all registered IDPs relative to population (DTM, {DATE})",
            "ukraine_shares_all.png")

# Figure 2: only IDPs who moved to ANOTHER oblast
make_figure("from_other_pct_of_pop",
            "A. IDPs from other oblasts living in the oblast",
            "IDPs from other oblasts, % of the oblast's population",
            "left_oblast_pct_of_pop",
            "B. IDPs who left the oblast for another oblast",
            "IDPs who left, % of the oblast's population",
            f"Ukraine: registered IDPs who moved between oblasts, relative to population (DTM, {DATE})",
            "ukraine_shares_moved.png")

plt.show()                                                      # open both windows (close them to finish)