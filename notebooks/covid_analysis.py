import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Loading- Loading all the data into Python using Pandas
try:
    confirmed = pd.read_csv("data/covid_19_confirmed.csv")
    deaths = pd.read_csv("data/covid_19_deaths.csv", header=1)
    recovered = pd.read_csv("data/covid_19_recovered.csv", header=1)
    print("Your csv files were successfully loaded")
except Exception as e:
    print(f"Error loading csv files: {e}")


# 2. Data Exploration
# 2.1 - Check the structure of each dataset in terms of rows, columns and data types
def explore_dataset(df, name):
    print(f"--- {name} Dataset ---")
    print("Shape of the Dataset", df.shape)
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nData info")
    print(df.info())
    print("\nData types:")
    print(df.dtypes)
    # some extra info
    print("\nMissing values (count per column):")
    print(df.isnull().sum())
    print("\nPreview of dataset:")
    print(df.head())


explore_dataset(confirmed, "Confirmed Cases")
explore_dataset(deaths, "Deaths Occured")
explore_dataset(recovered, "Recovered Cases")


# Question- 2.2
# Drop unnecessary columns and sum across all dates for individual countries.
confirmed_totals = confirmed.drop(columns=["Province/State", "Lat", "Long"])
confirmed_totals = confirmed_totals.groupby("Country/Region").sum()

# Add a column with total cases
confirmed_totals["Total"] = confirmed_totals.sum(axis=1)

# now sort the data in desc order of total cases and take top 5 countries
top5_countries = (
    confirmed_totals["Total"].sort_values(ascending=False).head(5).index.tolist()
)

# strip the country column for proper functioning of loc() while searching
confirmed["Country/Region"] = confirmed["Country/Region"].str.strip()
# top 5 countries data extracted in new variable and index resetted
top_data = confirmed_totals.loc[top5_countries].reset_index()


# melt the data to get single row per country-date combination - dropping the "total" column
top_data_melted = pd.melt(
    top_data.drop(columns=["Total"]),
    id_vars=["Country/Region"],
    var_name="Date",
    value_name="Confirmed",
)


# convert to datetime for proper formatting
top_data_melted["Date"] = pd.to_datetime(top_data_melted["Date"])

# now plot the graph and save
plt.figure(figsize=(14, 6))
sns.lineplot(data=top_data_melted, x="Date", y="Confirmed", hue="Country/Region")
plt.title("COVID-19 Confirmed Cases Over Time - Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")
plt.grid(True)
plt.tight_layout()
plt.savefig("visuals/top5_covid_trends.png")
plt.show()
plt.close()


# question 2.3- plots of confirmed cases over time for china
cases_china = confirmed_totals.loc[["China"]].reset_index()
cases_china_melted = pd.melt(
    cases_china.drop(columns=["Total"]),
    id_vars="Country/Region",
    var_name="Date",
    value_name="Confirmed",
)

# convert to date-time
cases_china_melted["Date"] = pd.to_datetime(
    cases_china_melted["Date"], format="%m/%d/%y"
)

# Plot the data now
plt.figure(figsize=(12, 5))
sns.lineplot(data=cases_china_melted, x="Date", y="Confirmed", color="red")

plt.title("COVID-19 Confirmed Cases Over Time - China")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")
plt.grid(True)
plt.tight_layout()
plt.savefig("visuals/china_covid_trend.png", dpi=300)
plt.show()
plt.close()


# handling missing data
# for confirmed dataset
def Handle_missing(df, name):
    print(f"\n{name} dataset being processed for missing values")
    df["Province/State"] = df["Province/State"].fillna("All Provinces")
    df = df.dropna(subset=["Lat", "Long"])
    print("\nAfter processing")
    print(df.isnull().sum())


Handle_missing(confirmed, "Confirmed Cases")
Handle_missing(deaths, "Deaths")
Handle_missing(recovered, "Recovered Cases")
