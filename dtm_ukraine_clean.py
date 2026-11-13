from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"             # data folder next to this script
df = pd.read_csv(DATA_DIR / "ukraine_admin1_raw.csv")           # read the raw table saved earlier

mask = df["operation"].str.contains("Registration")             # True where operation name contains "Registration"
reg = df[mask].copy()                                           # keep only registration rows (independent copy)
print("Registration rows:", len(reg), "of", len(df))            # how many rows we kept

reg["reportingDate"] = pd.to_datetime(reg["reportingDate"])     # text -> real dates
reg["reportingDate"] = reg["reportingDate"].dt.strftime("%Y-%m-%d")   # back to short text, nicer column names

long = reg.groupby(["admin1Name", "admin1Pcode", "reportingDate"],
                   as_index=False)["numPresentIdpInd"].sum()    # sum over all origin oblasts: one number per oblast and date

wide = long.pivot(index=["admin1Name", "admin1Pcode"],
                  columns="reportingDate",
                  values="numPresentIdpInd").reset_index()      # rows = oblasts, columns = dates
wide.columns.name = None                                        # remove the leftover "reportingDate" label

out_file = DATA_DIR / "ukraine_admin1_monthly.csv"
wide.to_csv(out_file, index=False)                              # save the clean table
print("Saved:", out_file)
print("Shape:", wide.shape)                                     # (oblasts, 2 label columns + dates)

totals = wide.iloc[:, 2:].sum()                                 # national total for every date column
print("\nNational total, last 5 dates:\n", totals.tail(5))      # should match the earlier registration series