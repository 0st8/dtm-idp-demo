from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"             # data folder next to this script

# Population on 1 January 2022, State Statistics Service of Ukraine
# (values taken from the Wikipedia table "List of Ukrainian oblasts and territories by population").
# Keys are oblast names spelled the way DTM spells them (column admin1Name).
population_2022 = {
    "Donetska": 4059372,
    "Dnipropetrovska": 3096485,
    "Kyiv": 2952301,                                            # Kyiv city
    "Kharkivska": 2598961,
    "Lvivska": 2478133,
    "Odeska": 2351392,
    "Luhanska": 2102921,
    "Zaporizka": 1638462,
    "Kyivska": 1795079,                                         # Kyiv oblast (not the city)
    "Vinnytska": 1509515,
    "Poltavska": 1352283,
    "Ivano-Frankivska": 1351822,
    "Khmelnytska": 1228829,
    "Zakarpatska": 1244476,
    "Zhytomyrska": 1179032,
    "Cherkaska": 1160744,
    "Rivnenska": 1141784,
    "Mykolaivska": 1091821,
    "Sumska": 1035772,
    "Ternopilska": 1021713,
    "Khersonska": 1001598,
    "Chernihivska": 959315,
    "Volynska": 1021356,
    "Kirovohradska": 903712,
    "Chernivetska": 890457,
}

# Population on 1 January 2014 (just before the annexation), State Statistics Service,
# table "Resident population". The source gives thousands of persons:
# Crimea 1958.5, Sevastopol agglomeration 383.9.
population_2014 = {
    "Autonomous Republic of Crimea": 1958500,
    "Sevastopol": 383900,
}

pop_2022 = pd.DataFrame({"admin1Name": list(population_2022.keys()),
                         "population": list(population_2022.values())})   # dict -> table
pop_2022["population_year"] = 2022                                         # which year the number is from
pop_2014 = pd.DataFrame({"admin1Name": list(population_2014.keys()),
                         "population": list(population_2014.values())})
pop_2014["population_year"] = 2014
pop = pd.concat([pop_2022, pop_2014], ignore_index=True)                   # stack both tables
pop.to_csv(DATA_DIR / "ukraine_population.csv", index=False)               # save for the next step
print("Rows:", len(pop))
print(pop.groupby("population_year")["population"].sum())                  # totals per year (not comparable to each other)

monthly = pd.read_csv(DATA_DIR / "ukraine_admin1_monthly.csv")  # our clean DTM table
dtm_names = set(monthly["admin1Name"])                          # oblast names in DTM
pop_names = set(pop["admin1Name"])                              # oblast names in the population table
print("In DTM but not in population:", sorted(dtm_names - pop_names))     # names to fix
print("In population but not in DTM:", sorted(pop_names - dtm_names))     # names to fix