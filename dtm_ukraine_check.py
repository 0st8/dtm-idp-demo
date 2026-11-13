from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"       # path to the data folder next to the script
df = pd.read_csv(DATA_DIR / "ukraine_admin1_raw.csv")     # read the saved raw table

df["source"] = "other"                                    # first assign the label "other" to all rows
mask = df["operation"].str.contains("Registration")       # True where the operation name contains the word Registration
df.loc[mask, "source"] = "registration"                   # update the label for these rows to "registration"

tbl = df.pivot_table(index="reportingDate", columns="source",
                     values="numPresentIdpInd", aggfunc="sum")   # sum IDP: rows = dates, columns = sources
print(tbl[tbl["other"].notna()])                          # keep only dates where the second source exists

reg = df[df["source"] == "registration"]                  # only registration rows
monthly = reg.groupby("reportingDate")["numPresentIdpInd"].sum()   # sum by date without duplication
print(monthly.tail(12))                                   # last 12 dates