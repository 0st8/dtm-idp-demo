from pathlib import Path
import pandas as pd

pd.set_option("display.width", 200)                             # wider output so columns are not cut with ...
pd.set_option("display.max_columns", None)                      # show all columns

DATA_DIR = Path(__file__).resolve().parent / "data"             # data folder next to this script
raw = pd.read_csv(DATA_DIR / "ukraine_admin1_raw.csv")          # raw DTM table (all rows)
pop = pd.read_csv(DATA_DIR / "ukraine_population.csv")          # population by oblast (2022 or 2014)

reg = raw[raw["operation"].str.contains("Registration")].copy() # registration rows only
reg["reportingDate"] = pd.to_datetime(reg["reportingDate"])     # text -> real dates
latest = reg["reportingDate"].max()                             # newest reporting date
print("Latest date:", latest.date())
now = reg[reg["reportingDate"] == latest]                       # rows of the newest date only

same = now["admin1Name"] == now["idpOriginAdmin1Name"]          # True where people live in the oblast they came from
moved = now[~same]                                              # only people who moved to ANOTHER oblast

# A) HOST: IDPs living in the oblast / its population
host = now.groupby("admin1Name")["numPresentIdpInd"].sum().reset_index(name="idps_hosted")        # all IDPs living here
other = moved.groupby("admin1Name")["numPresentIdpInd"].sum().reset_index(name="idps_from_other_oblasts")  # only those from other oblasts
host = host.merge(other, on="admin1Name", how="left")           # put both numbers in one table
host = host.merge(pop, on="admin1Name", how="left")             # attach population (NaN if no match)
host["hosted_pct_of_pop"] = (host["idps_hosted"] / host["population"] * 100).round(2)                   # all IDPs living here
host["from_other_pct_of_pop"] = (host["idps_from_other_oblasts"] / host["population"] * 100).round(2)   # only from other oblasts
host = host.sort_values("from_other_pct_of_pop", ascending=False)
print("\nA) IDPs living in the oblast, % of its population:\n", host)

# B) ORIGIN: IDPs who came FROM the oblast / its population
origin = now.groupby("idpOriginAdmin1Name")["numPresentIdpInd"].sum().reset_index(name="idps_from_here")   # all IDPs from here
left = moved.groupby("idpOriginAdmin1Name")["numPresentIdpInd"].sum().reset_index(name="idps_left_oblast") # only those who left the oblast
origin = origin.merge(left, on="idpOriginAdmin1Name", how="left")
origin = origin.rename(columns={"idpOriginAdmin1Name": "admin1Name"})   # same key name as in pop
origin = origin.merge(pop, on="admin1Name", how="left")
origin["displaced_pct_of_pop"] = (origin["idps_from_here"] / origin["population"] * 100).round(2)       # all IDPs from here
origin["left_oblast_pct_of_pop"] = (origin["idps_left_oblast"] / origin["population"] * 100).round(2)   # only those who left the oblast
origin = origin.sort_values("left_oblast_pct_of_pop", ascending=False)
print("\nB) IDPs from the oblast, % of its population:\n", origin)

host.to_csv(DATA_DIR / "ukraine_share_hosted.csv", index=False)      # save both tables
origin.to_csv(DATA_DIR / "ukraine_share_origin.csv", index=False)
print("\nSaved two CSV files")