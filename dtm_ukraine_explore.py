from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
df = pd.read_csv(DATA_DIR / "ukraine_admin1_raw.csv") # Loads the raw data from the CSV file

print("Shape:", df.shape)
print("\nOperation:\n", df["operation"].value_counts())
print("\nAssessment type:\n", df["assessmentType"].value_counts())
print("\nDisplacement reason:\n", df["displacementReason"].value_counts(dropna=False))
print("\nRounds:\n", df["roundNumber"].value_counts().sort_index())

print("\nEmpty cells per column:\n", df.isna().sum())

by_date = df.groupby("reportingDate")["numPresentIdpInd"].agg(["count", "sum"]) # Groups the data by reporting date and calculates the count of rows and the total number of IDPs for each date
print("\nRows and total IDPs per reporting date:\n", by_date)

