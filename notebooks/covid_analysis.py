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


# Ques 3 and 4 - handling missing data
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



# Question 5.1 - Analyze the peak number if daily new cases in Germany, France and Italy . 
# Which country experienced highest single day surge and when?
filtered_data = confirmed[confirmed["Country/Region"].isin(["Germany", "France", "Italy"])]
filtered_data = filtered_data.drop(columns=["Province/State", "Lat", "Long"])

# Group by country and sum (in case of multiple provinces)
country_data = filtered_data.groupby("Country/Region").sum()
daily_new_cases = country_data.diff(axis=1).reset_index()  # difference between columns (dates)
print(daily_new_cases)
daily_melted = pd.melt(
    daily_new_cases,
    id_vars="Country/Region",
    var_name="Date",
    value_name="NewCases"
)

daily_melted["Date"] = pd.to_datetime(daily_melted["Date"], format="%m/%d/%y")
maxvalue_row=daily_melted.loc[daily_melted['NewCases'].idxmax()]
country = maxvalue_row["Country/Region"]  
date = maxvalue_row["Date"].strftime("%d-%m-%Y")  
cases = int(maxvalue_row["NewCases"]) 
print(f"\nThe highest single-day surge was in {country} on {date} with {cases} new cases.")



plt.figure(figsize=(14, 6))
sns.lineplot(data=daily_melted, x="Date", y="NewCases", hue="Country/Region")

plt.title("Daily New COVID-19 Cases: Germany, France, Italy")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.grid(True)
plt.tight_layout()
plt.savefig("visuals/daily_new_cases_three_countries", dpi=300)
plt.show()
plt.close()

# Question 5.2 - comparison of recovery/confirmed ratio between canada and australia as of DEc 31 ,2020. 
date_col = "12/31/20"
countries = ["Canada", "Australia"]
confirmed_totals = confirmed[confirmed["Country/Region"].isin(countries)].drop(columns=["Province/State", "Lat", "Long"]).groupby("Country/Region").sum()
recovered_totals = recovered[recovered["Country/Region"].isin(countries)].drop(columns=["Province/State", "Lat", "Long"]).groupby("Country/Region").sum()
confirmed_dec31 = confirmed_totals[date_col]
recovered_dec31 = recovered_totals[date_col]
print("Confirmed cases on 31 Dec 2020:\n", confirmed_dec31)
print("\nRecovered cases on 31 Dec 2020:\n", recovered_dec31)
# Calculate ratio
recovery_ratio = recovered_dec31 / confirmed_dec31

# plot bar graph
print("\nRecovery / Confirmed ratio on 31 Dec 2020:")
print(recovery_ratio.reset_index())
recovery_df = recovery_ratio.reset_index()
recovery_df.columns = ["Country", "RecoveryRatio"]

# Create bar plot
plt.figure(figsize=(8, 5))
sns.barplot(data=recovery_df, x="Country", y="RecoveryRatio",hue="Country")
plt.title("Recovery to Confirmed Ratio (as of Dec 31, 2020)")
plt.ylabel("Recovery Ratio")
plt.ylim(0,1)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("visuals/recovery_ratio_comparison.png")
plt.show()
plt.close()


# Question 5.3 - distribution of death rates (deaths/confirmed cases) among provinces in Canada.Identify the province with the highest and lowest death rate as of the latest data point.
# target - table with date province death ratio.
latest_date = confirmed.columns[-1]
confirmed_canada = confirmed.loc[confirmed["Country/Region"] == "Canada", ["Province/State", latest_date]].set_index("Province/State")
deaths_canada = deaths.loc[deaths["Country/Region"] == "Canada", ["Province/State", latest_date]].set_index("Province/State")
death_rate = deaths_canada[latest_date] / confirmed_canada[latest_date]
death_rate = death_rate[confirmed_canada[latest_date] > 0]
death_rate_df = death_rate.reset_index().rename(columns={latest_date: "DeathRate"})

# plot the data
plt.figure(figsize=(10, 6))
sns.barplot(data=death_rate_df, x="DeathRate", y="Province/State", hue="Province/State")
plt.title(f"Death Rate among Canadian Provinces (as of {latest_date})")
plt.xlabel("Death Rate")
plt.ylabel("Province")
plt.tight_layout()
plt.savefig("visuals/canada_provinces_death_rate.svg")
plt.show()
max_province = death_rate.idxmax()
min_province = death_rate.idxmin()
print(f"Highest death rate: {max_province} with {death_rate[max_province]:.2%}")
print(f"Lowest death rate: {min_province} with {death_rate[min_province]:.2%}")

# Question 6 - Data Transformation
# Ques 6.1 - Melt the deaths dataset
deaths_metled_data=pd.melt(deaths,id_vars=['Province/State','Country/Region','Lat','Long'],var_name="Date",value_name='Deaths')
print(deaths_metled_data.head(10))

# Ques 6.2 - Total deaths reported per country up to current date
latest_date = confirmed.columns[-1]
sum_deaths_per_country = deaths_metled_data[deaths_metled_data['Date'] == latest_date].groupby('Country/Region')['Deaths'].sum()
print('\nPer country deaths ')
print(sum_deaths_per_country)

# plot the data
top_deaths = sum_deaths_per_country.sort_values(ascending=False).head(10).reset_index()
top_deaths.columns = ['Country', 'TotalDeaths']

plt.figure(figsize=(10, 6))
sns.barplot(data=top_deaths, x='Country', y='TotalDeaths', hue='Country')
plt.title(f"Top 10 Countries by COVID-19 Deaths as of {latest_date}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/top10_deaths_by_country.png")
plt.show()
plt.close()

# Ques 6.3 - Top 5 countries with highest average daily deaths
temp = deaths.drop(columns=['Province/State','Lat','Long'])
grouped = temp.groupby("Country/Region").sum()
daily_new_deaths = grouped.diff(axis=1)
# print(f"\n Daily new deaths table : \n{daily_new_deaths}")
print(daily_new_deaths)

# Calculate average daily deaths for each country
average_daily_deaths = daily_new_deaths.mean(axis=1)

# Sort in descending order and get top 5 countries
top5_avg_deaths = average_daily_deaths.sort_values(ascending=False).head(5)

# Display results
print("Top 5 countries with highest average daily deaths:\n")
print(top5_avg_deaths)
top5_avg_deaths_df = top5_avg_deaths.reset_index()
top5_avg_deaths_df.columns = ['Country', 'AverageDailyDeaths']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=top5_avg_deaths_df, x='AverageDailyDeaths', y='Country', hue='Country')

# Add title and labels
plt.title('Top 5 Countries by Average Daily COVID-19 Deaths')
plt.xlabel('Average Daily Deaths')
plt.ylabel('Country')

plt.tight_layout()
plt.savefig("visuals/Top_5_Countries_by_Average_Daily_COVID-19_Deaths.png")
plt.show()
plt.close()

# ques 6.4 - Total Deaths Variation over time in the US
# Step 1: Filter US rows
US_deaths = deaths[deaths['Country/Region'] == 'US']

# Step 2: Drop non-date columns and sum all US states/provinces by date
US_deaths_sum = US_deaths.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long']).sum()

# Step 3: Reset index to turn Series into DataFrame for melting
US_deaths_df = US_deaths_sum.reset_index()
US_deaths_df.columns = ['Date', 'Deaths']

print(US_deaths_df)
US_deaths_df['Date']=pd.to_datetime(US_deaths_df['Date'])
# Plot line graph
plt.figure(figsize=(12, 6))
sns.lineplot(data=US_deaths_df, x='Date', y='Deaths')
plt.title('Daily COVID-19 Deaths in the US Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Deaths')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/US_death_trend.png")
plt.show()
plt.close()

# ques 7.1 - Data Merging
confirmed_long = pd.melt(
    confirmed,
    id_vars=["Province/State", "Country/Region", "Lat", "Long"],
    var_name="Date",
    value_name="Confirmed"
)

# Melt deaths
deaths_long = pd.melt(
    deaths,
    id_vars=["Province/State", "Country/Region", "Lat", "Long"],
    var_name="Date",
    value_name="Deaths"
)

# Melt recovered
recovered_long = pd.melt(
    recovered,
    id_vars=["Province/State", "Country/Region", "Lat", "Long"],
    var_name="Date",
    value_name="Recovered"
)

# Convert 'Date' column to datetime for all three
for df in [confirmed_long, deaths_long, recovered_long]:
    df['Date'] = pd.to_datetime(df['Date'])
merged_df = pd.merge(
    confirmed_long,
    deaths_long,
    on=["Province/State", "Country/Region", "Lat", "Long", "Date"],
    how="outer"
)

# Merge the result with recovered
merged_df = pd.merge(
    merged_df,
    recovered_long,
    on=["Province/State", "Country/Region", "Lat", "Long", "Date"],
    how="outer"
)
print(merged_df.head())

# ques 7.2 - monthly analysis
# Step 1: Create 'MonthEnd' column (last date of the month)
merged_df['MonthEnd'] = merged_df['Date'] + pd.offsets.MonthEnd(0)

# Step 2: Group by Country/Region and MonthEnd, summing over provinces
monthly_cumulative = merged_df.groupby(['Country/Region', 'MonthEnd'])[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()

# Step 3: Sort values to prepare for monthly differences
monthly_cumulative = monthly_cumulative.sort_values(by=['Country/Region', 'MonthEnd'])

# Step 4: Calculate monthly new cases (confirmed, deaths, recovered) using .diff() grouped by country
monthly_cumulative['MonthlyConfirmed'] = monthly_cumulative.groupby('Country/Region')['Confirmed'].diff()
monthly_cumulative['MonthlyDeaths'] = monthly_cumulative.groupby('Country/Region')['Deaths'].diff()
monthly_cumulative['MonthlyRecovered'] = monthly_cumulative.groupby('Country/Region')['Recovered'].diff()

# Step 5: Final DataFrame with selected columns
monthly_data = monthly_cumulative[['Country/Region', 'MonthEnd', 'MonthlyConfirmed', 'MonthlyDeaths', 'MonthlyRecovered']]

# Display first few rows
print('\nmonthly')
print(monthly_data.head(10))

# ques 7.3 - same analysis for US', 'Italy', 'Brazil
select_analysis = monthly_data[monthly_data['Country/Region'].isin(['US', 'Italy', 'Brazil'])]
print(select_analysis)


# ques 8.1-average death rate
# Filter data for 2020 only
df_2020 = merged_df[merged_df['Date'].dt.year == 2020]

# Avoid division by zero and nulls
df_2020 = df_2020[df_2020['Confirmed'] > 0]
df_2020 = df_2020.dropna(subset=['Confirmed', 'Deaths'])

# Calculate death rate
df_2020['DeathRate'] = df_2020['Deaths'] / df_2020['Confirmed']

# Group by country and calculate average death rate
avg_death_rates = df_2020.groupby('Country/Region')['DeathRate'].mean().sort_values(ascending=False)

# Get top 3 countries
top3_death_rates = avg_death_rates.head(3)

print("Top 3 Countries with Highest Average Death Rates in 2020:")
print(top3_death_rates.apply(lambda x: f"{x:.2%}"))

# ques 8.2 - using the merged dataset , compare the total recoveries to total deaths in south africa .
# Filter merged data for South Africa
south_africa_data = merged_df[merged_df["Country/Region"] == "South Africa"]

# Get the latest date from the dataset
latest_date = south_africa_data["Date"].max()

# Filter for the latest date (most up-to-date cumulative data)
latest_data = south_africa_data[south_africa_data["Date"] == latest_date]

# Sum over all provinces (if applicable)
total_deaths = latest_data["Deaths"].sum()
total_recoveries = latest_data["Recovered"].sum()

# Print comparison
print(f" Latest data as of {latest_date.date()}:")
print(f" Total Recoveries in South Africa: {int(total_recoveries):,}")
print(f" Total Deaths in South Africa: {int(total_deaths):,}")

# Optional: Visualize the comparison using a bar chart
comparison_df = pd.DataFrame({
    "Metric": ["Recoveries", "Deaths"],
    "Count": [total_recoveries, total_deaths]
})

plt.figure(figsize=(6, 4))
sns.barplot(data=comparison_df, x="Metric", y="Count", palette="Set2")
plt.title(f"Recoveries vs Deaths in South Africa (as of {latest_date.date()})")
plt.ylabel("Number of People")
plt.tight_layout()
plt.savefig("visuals/Recoveries_vs_Deaths_in_South_Africa.png")
plt.show()
plt.close()

# ques 8.3 - 
us_data = merged_df[merged_df["Country/Region"] == "US"].copy()

# Step 2: Group by Date to get national totals per day (sum over provinces/states)
us_daily = us_data.groupby("Date")[["Confirmed", "Recovered"]].sum().reset_index()

# Step 3: Set Date as index and resample to get data at the end of each month
us_monthly_cumulative = us_daily.set_index("Date").resample("M").last()

# Step 4: Compute month-wise Recoveries / Confirmed ratios
us_monthly_cumulative["RecoveryRatio"] = us_monthly_cumulative["Recovered"] / us_monthly_cumulative["Confirmed"]

# Step 5: Filter from March 2020 to May 2021
us_monthly_cumulative = us_monthly_cumulative.loc["2020-03-01":"2021-05-31"]

# Step 6: Plot the result
plt.figure(figsize=(10, 5))
sns.lineplot(data=us_monthly_cumulative, x=us_monthly_cumulative.index, y="RecoveryRatio", marker="o", color="green")
plt.title("Monthly Recovery-to-Confirmed Ratio in US (Mar 2020 – May 2021)")
plt.xlabel("Month")
plt.ylabel("Recovery Ratio")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("visuals/Monthly Recovery-to-Confirmed_Ratio_in_US.png")
plt.show()
plt.close()