from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent / "data"             # data folder next to this script
BOUNDARY_FILE = DATA_DIR / "ukraine_admin1.geojson"             # oblast boundaries downloaded from HDX
DATE = "2026-09-30"                                             # latest DTM reporting date used in the tables

raw = pd.read_csv(DATA_DIR / "ukraine_admin1_raw.csv")          # raw table: has oblast names AND codes
host = pd.read_csv(DATA_DIR / "ukraine_share_hosted.csv")       # table A (by oblast name)
origin = pd.read_csv(DATA_DIR / "ukraine_share_origin.csv")     # table B (by oblast name)

# the share tables have names only, the map needs codes (Pcode): take name -> code pairs from the raw table
host_codes = raw[["admin1Name", "admin1Pcode"]].drop_duplicates()
origin_codes = raw[["idpOriginAdmin1Name", "idpOriginAdmin1Pcode"]].drop_duplicates()
origin_codes = origin_codes.rename(columns={"idpOriginAdmin1Name": "admin1Name",
                                            "idpOriginAdmin1Pcode": "admin1Pcode"})   # same column names as host
host = host.merge(host_codes, on="admin1Name", how="left")      # add the code to table A
origin = origin.merge(origin_codes, on="admin1Name", how="left")  # add the code to table B

gdf = gpd.read_file(BOUNDARY_FILE)                              # boundaries: one polygon per oblast
codes = [c for c in gdf.columns if c.lower() == "adm1_pcode"]   # find the code column whatever its letter case
if not codes:
    raise SystemExit(f"No ADM1_PCODE column. Columns are: {list(gdf.columns)}")
code_col = codes[0]
print("Boundary polygons:", len(gdf))

host_cols = ["admin1Pcode", "hosted_pct_of_pop", "from_other_pct_of_pop"]
origin_cols = ["admin1Pcode", "displaced_pct_of_pop", "left_oblast_pct_of_pop"]
gdf = gdf.merge(host[host_cols], left_on=code_col, right_on="admin1Pcode",
                how="left", validate="many_to_one")             # attach table A to polygons
gdf = gdf.drop(columns="admin1Pcode")                           # drop the duplicate code column before the second merge
gdf = gdf.merge(origin[origin_cols], left_on=code_col, right_on="admin1Pcode",
                how="left", validate="many_to_one")             # attach table B to polygons
print("Polygons with table A:", gdf["hosted_pct_of_pop"].notna().sum())
print("Polygons with table B:", gdf["displaced_pct_of_pop"].notna().sum())


def make_map_figure(left_col, left_title, right_col, right_title, suptitle, filename):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))             # two maps side by side
    for ax, col, title in [(axes[0], left_col, left_title), (axes[1], right_col, right_title)]:
        gdf.plot(column=col, cmap="OrRd", linewidth=0.4, edgecolor="white", legend=True,
                 missing_kwds={"color": "lightgrey", "label": "No data"},
                 legend_kwds={"shrink": 0.6, "label": "% of population"}, ax=ax)   # colour each oblast by its share
        ax.set_title(title, fontsize=12)                        # map title
        ax.set_axis_off()                                       # no lat/lon axes
    fig.suptitle(suptitle, fontsize=14)                         # figure title
    fig.text(0.01, 0.01, "Grey = no data. Population base: 1 Jan 2022 (2014 for Crimea and Sevastopol). "
             "Sources: IOM DTM, State Statistics Service of Ukraine.", fontsize=9)   # source note
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))


print("Polygons with table B:", gdf["displaced_pct_of_pop"].notna().sum())


def make_map_figure(left_col, left_title, right_col, right_title, suptitle, filename):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))             # two maps side by side
    for ax, col, title in [(axes[0], left_col, left_title), (axes[1], right_col, right_title)]:
        gdf.plot(column=col, cmap="OrRd", linewidth=0.4, edgecolor="white", legend=True,
                 missing_kwds={"color": "lightgrey", "label": "No data"},
                 legend_kwds={"shrink": 0.6, "label": "% of population"}, ax=ax)   # colour each oblast by its share
        ax.set_title(title, fontsize=12)                        # map title
        ax.set_axis_off()                                       # no lat/lon axes
    fig.suptitle(suptitle, fontsize=14)                         # figure title
    fig.text(0.01, 0.01, "Grey = no data. Population base: 1 Jan 2022 (2014 for Crimea and Sevastopol). "
             "Sources: IOM DTM, State Statistics Service of Ukraine.", fontsize=9)   # source note
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(DATA_DIR.parent / filename, dpi=150)            # save the picture
    print("Saved", filename)


# Map 1: ALL registered IDPs (including people who moved inside their own oblast)
make_map_figure("hosted_pct_of_pop", "A. All IDPs living in the oblast",
                "displaced_pct_of_pop", "B. All IDPs who came from the oblast",
                f"Ukraine: all registered IDPs relative to population (DTM, {DATE})",
                "ukraine_map_all.png")

# Map 2: only IDPs who moved to ANOTHER oblast
make_map_figure("from_other_pct_of_pop", "A. IDPs from other oblasts living in the oblast",
                "left_oblast_pct_of_pop", "B. IDPs who left the oblast for another oblast",
                f"Ukraine: registered IDPs who moved between oblasts (DTM, {DATE})",
                "ukraine_map_moved.png")

plt.show()                                                      # open both windows (close them to finish)