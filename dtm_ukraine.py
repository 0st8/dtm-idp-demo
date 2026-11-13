from pathlib import Path
from dtmapi import DTMApi

DATA_DIR = Path(__file__).resolve().parent / "data" # Path to our fo`lder where we will save the data
DATA_DIR.mkdir(exist_ok=True)

api = DTMApi(api_version="v3") #Conects to the DTM API
df = api.get_idp_admin1_data(CountryName="Ukraine") # Loads a table of displaced persons by region (admin1) for all years.

print("Shape:", df.shape) # this block prints the shape of the dataframe, the column names, the range of dates in the data, and the first few rows of the dataframe.
print(df.columns.tolist())
print("Dates:", df["reportingDate"].min(), "->", df["reportingDate"].max())
print(df.head())

df.to_csv(DATA_DIR / "ukraine_admin1_raw.csv", index=False) # Saves the raw data to a CSV file in the data folder
print("Saved raw CSV")

