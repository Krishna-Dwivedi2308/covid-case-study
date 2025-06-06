import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Loading- Loading all the data into Python using Pandas
try:
    confirmed = pd.read_csv("data/covid_19_confirmed.csv")
    confirmed['Country/Region'] = confirmed['Country/Region'].str.strip()
    deaths = pd.read_csv("data/covid_19_deaths.csv", header=1)
    deaths['Country/Region'] = deaths['Country/Region'].str.strip()
    recovered = pd.read_csv("data/covid_19_recovered.csv", header=1)
    recovered['Country/Region'] = recovered['Country/Region'].str.strip()
    print("Your csv files were successfully loaded")
except Exception as e:
    print(f"Error loading csv files: {e}")


# 2. Data Exploration
# Ques 2.1 - the structure of each dataset in terms of rows, columns, and data types
def ques2a():
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


# Question- 2.2-Generate plots of confirmed cases over time for the top countries
confirmed_totals=pd.DataFrame()
def ques2b():
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
def ques2c():
    confirmed_totals = confirmed.drop(columns=["Province/State", "Lat", "Long"])
    confirmed_totals = confirmed_totals.groupby("Country/Region").sum()
    confirmed_totals["Total"] = confirmed_totals.sum(axis=1)
    cases_china = confirmed_totals.loc[["China"]].reset_index()
    cases_china_melted = pd.melt(
        cases_china.drop(columns=["Total"]),
        id_vars="Country/Region",
        var_name="Date",
        value_name="Confirmed",
    )

    # convert to date-time
    cases_china_melted["Date"] = pd.to_datetime(
        cases_china_melted["Date"]
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
def ques3_and_4():
    def Handle_missing(df, name):
        print(f"\n{name} dataset being processed for missing values")
        df["Province/State"] = df["Province/State"].fillna("All Provinces")
        df = df.dropna(subset=["Lat", "Long"]) #drop if lat and long values are not present because they make no sense for geo mapping 
        print("\nAfter processing")
        print(df.isnull().sum())

    Handle_missing(confirmed, "Confirmed Cases")
    Handle_missing(deaths, "Deaths")
    Handle_missing(recovered, "Recovered Cases")


def ques5():
    # Solution 5.1
    print("\nAnswer 5.1\n")
    def find_daily_diff_data(df,name):
        print(f"\n{name} data being dealt with: Generating daily cases from cumulative Cases/data")
        temp = df.drop(columns=["Province/State", "Lat", "Long"]).groupby("Country/Region").sum()

        daily_data_diff = temp.diff(axis=1)
        daily_data_diff[daily_data_diff.columns[0]] = 0  # Replace NaN in first column with 0

        print(daily_data_diff)
        return daily_data_diff
    daily_confirmed_cases_per_Country = find_daily_diff_data(confirmed, "Confirmed Cases")
    daily_confirmed_cases_per_Country.to_csv("data/daily_confirmed_cases_per_Country.csv")

    daily_Deaths_cases_per_country = find_daily_diff_data(deaths, "Death Cases")
    daily_Deaths_cases_per_country.to_csv("data/daily_Deaths_cases_per_country.csv")

    daily_recovery_cases_per_country= find_daily_diff_data(recovered, "Recovery Cases")
    daily_recovery_cases_per_country.to_csv("data/daily_recovery_cases_per_country.csv")

    # daily cases data generated , now let us address highest single day surge in daily cases
    daily_confirmed_melted = pd.melt(
    daily_confirmed_cases_per_Country.reset_index(),  # reset_index to keep 'Country/Region' as column
    id_vars=['Country/Region'],                        # columns to keep as identifier variables
    var_name='Date',                                   # name for the melted date column
    value_name='DailyConfirmed'                        # name for the values column
    )

    print(daily_confirmed_melted.head())
    max_value_index=daily_confirmed_melted['DailyConfirmed'].idxmax()
    print(f"Maximum daily confirmed cases were {daily_confirmed_melted.loc[max_value_index, 'DailyConfirmed']} in {daily_confirmed_melted.loc[max_value_index, 'Country/Region']} on {daily_confirmed_melted.loc[max_value_index, 'Date']}.")
    top5 = daily_confirmed_melted.sort_values(by='DailyConfirmed', ascending=False).head(5)
    print(top5)
   

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=top5,
        x='DailyConfirmed',
        y='Country/Region',
        hue="Date"
    )
    plt.title('Top 5 Daily Confirmed COVID Cases by Country')
    plt.xlabel('Daily Confirmed Cases')
    plt.ylabel('Country/Region')
    plt.tight_layout()
    plt.savefig("visuals/Top_5_daily_spike_in_cases")
    plt.show()
    plt.close()

    # Solution 5.2
    print("\nAnswer 5.2\n")
    total_confirmed_cases=confirmed.drop(columns=["Province/State", "Lat", "Long"]).groupby('Country/Region').sum()['12/31/20']
    total_confirmed_cases=total_confirmed_cases.loc[['Canada','Australia']]
    print(f"\nTotal confirmed cases data:\n{total_confirmed_cases}")

    total_recovery_cases=recovered.drop(columns=["Province/State", "Lat", "Long"]).groupby('Country/Region').sum()['12/31/20']
    total_recovery_cases=total_recovery_cases.loc[['Canada','Australia']]
    print(f"\nTotal recovery cases data:\n{total_recovery_cases}")
    
    recovery_rates=total_recovery_cases/total_confirmed_cases
    for country, rate in recovery_rates.items():
        print(f"As of December 31, 2020, the recovery rate in {country} was {rate:.2%}.")


    # solution 5.3 - 
    print("\nAnswer 5.3\n")
    # Extract latest date (last column with date)
    latest_date = confirmed.columns[-1]

    # Filter data for Canada from confirmed and deaths datasets
    canada_confirmed = confirmed[confirmed['Country/Region'] == 'Canada']
    canada_deaths = deaths[deaths['Country/Region'] == 'Canada']

    # Drop unnecessary columns and set Province/State as index
    confirmed_prov = canada_confirmed.drop(columns=['Country/Region', 'Lat', 'Long']).set_index('Province/State')
    deaths_prov = canada_deaths.drop(columns=['Country/Region', 'Lat', 'Long']).set_index('Province/State')

    # Get values for the latest date
    confirmed_latest = confirmed_prov[latest_date]
    deaths_latest = deaths_prov[latest_date]

    # Create dataframe
    df = pd.DataFrame({
        'Confirmed': confirmed_latest,
        'Deaths': deaths_latest
    })
    # print(df)
    # Exclude rows where confirmed cases are 0 to avoid inf%
    df = df[df['Confirmed'] > 0]

    # Calculate death rates
    df['Death Rate'] = df['Deaths'] / df['Confirmed']
    # print(df)
    # Get province with max and min death rates
    max_province = df['Death Rate'].idxmax() #will give province name because that is the index
    # print(max_province)
    max_rate = df['Death Rate'].max()

    min_province = df['Death Rate'].idxmin() #will give province name because that is the index
    # print(min_province)
    min_rate = df['Death Rate'].min() #will give min value of the Death rate.

    print(f"As of {latest_date}, in Canada:")
    print(f"- The province with the highest death rate is {max_province} with a rate of {max_rate:.2%}.")
    print(f"- The province with the lowest death rate is {min_province} with a rate of {min_rate:.2%}.")


def ques6():
    # Solution 6.1
    deaths_metled_data=pd.melt(deaths,id_vars=['Country/Region','Province/State','Lat','Long'],var_name="Date",value_name='Deaths')
    print(deaths_metled_data.head(10))
    print("\nanswer 6.2\n")
    # Solution 6.2
    daily_deaths_per_country=pd.read_csv("data/daily_Deaths_cases_per_country.csv")
    daily_deaths_per_country.set_index("Country/Region",inplace=True)
    total_deaths_per_country=daily_deaths_per_country.sum(axis=1).reset_index()
    total_deaths_per_country.columns=['Country/Region',"Total Deaths"]
    total_deaths_per_country.to_csv("data/ques6b_total_deaths_per_country.csv")
    print(total_deaths_per_country)
    #solution 6.3
    avg_daily_deaths=daily_deaths_per_country.mean(axis=1).reset_index()
    avg_daily_deaths.columns=['Country/Region','Mean_daily_deaths']
    top_5 = avg_daily_deaths.sort_values('Mean_daily_deaths', ascending=False).head(5)
    top_5.to_csv("data/ques6c_top_5_countries_with_the_highest_average_daily_deaths.csv")
    print(f'\nThe top five countrues with highest average daily deaths are :\n {top_5}')

    # Solution 6.4
    print("\nAnswer 6.4\n")
    us_deaths = deaths[deaths["Country/Region"] == "US"].drop(columns=["Province/State", "Country/Region", "Lat", "Long"], errors="ignore")

    us_deaths_transposed = us_deaths.T
    us_deaths_transposed.index = pd.to_datetime(us_deaths_transposed.index)
    us_deaths_transposed.columns = ['Deaths']

    
    us_deaths_transposed = us_deaths_transposed.reset_index()
    us_deaths_transposed.columns = ['Date', 'Deaths']

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=us_deaths_transposed, x='Date', y='Deaths')
    plt.title('Cumulative COVID-19 Deaths in US Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Deaths')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("visuals/ques6d_US_deaths_lineplot.png")
    plt.show()
    plt.close()

def ques7():
    # solution 7.1
    # Melt Confirmed
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
        how="outer")
    merged_df.to_csv("data/merged_data_of_all_cumulative.csv")
    
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
    monthly_data.to_csv("data/ques7bmonthly_sum_of_confirmed_cases_deaths_and_recoveries.csv")
    # Display first few rows
    print('\nmonthly')
    print(monthly_data.head(10))

    # ques 7.3 - same analysis for US', 'Italy', 'Brazil
    select_analysis = monthly_data[monthly_data['Country/Region'].isin(['US', 'Italy', 'Brazil'])]
    select_analysis.to_csv("data/ques7cselect_analysis_for_United States_Italy_and_Brazil.csv")
    print(select_analysis)


def ques8():
    # solution 8.1
    daily_deaths = pd.read_csv("data/daily_Deaths_cases_per_country.csv", index_col="Country/Region")
    daily_confirmed = pd.read_csv("data/daily_confirmed_cases_per_Country.csv", index_col="Country/Region")
    
    # Compute mean daily deaths per country
    daily_avg_deaths_per_country = daily_deaths.mean(axis=1)
    daily_avg_confirmed_per_country = daily_confirmed.mean(axis=1)
    
    
    death_rates=daily_avg_deaths_per_country/daily_avg_confirmed_per_country
    top_3_death_rates = death_rates.sort_values(ascending=False).head(3)
    top_3_df = top_3_death_rates.reset_index()
    top_3_df.columns = ['Country/Region', 'Average Death Rate']
    top_3_df.to_csv("data/ques8.1three_countries_with_the_highest_average_death_rates.csv")
    print(f"Top 3 countries with highest death rates are : \n{top_3_df}")

    # solution 8.2
    merged_data=pd.read_csv("data/merged_data_of_all_cumulative.csv")
    merged_data_SA=merged_data[merged_data['Country/Region']=='South Africa']
    print(merged_data_SA)
    merged_data_SA["Date"] = pd.to_datetime(merged_data_SA["Date"])

    
    grouped = merged_data_SA.groupby(["Country/Region", "Date"])[["Confirmed", "Deaths", "Recovered"]].sum().reset_index()

    
    melted = pd.melt(
        grouped,
        id_vars=["Date"],
        value_vars=["Recovered", "Deaths"],
        var_name="Case_Type",
        value_name="Count"
    )

    
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=melted, x="Date", y="Count", hue="Case_Type", palette={"Recovered": "green", "Deaths": "red"})

    plt.title("COVID-19 Recoveries vs Deaths Over Time in South Africa")
    plt.xlabel("Date")
    plt.ylabel("Number of Cases")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("visuals/ques8brecoveries_vs_deaths_SA.png")
    plt.show()
    plt.close()
    
    #  solution 8.3
    us_data = merged_data[merged_data["Country/Region"] == "US"].copy()

    # Ensure Date column is in datetime format
    us_data["Date"] = pd.to_datetime(us_data["Date"])

    # Step 2: Group by Date to get national totals per day
    us_daily = us_data.groupby("Date")[["Confirmed", "Recovered"]].sum().reset_index()

    # Step 3: Set Date as index and resample to get last day of each month
    us_monthly_cumulative = us_daily.set_index("Date").resample("M").last()

    # Step 4: Calculate monthly recovery ratio
    us_monthly_cumulative["RecoveryRatio"] = us_monthly_cumulative["Recovered"] / us_monthly_cumulative["Confirmed"]

    # Step 5: Filter from March 2020 to May 2021
    us_monthly_cumulative = us_monthly_cumulative.loc["2020-03-01":"2021-05-31"]

    # Step 6: Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=us_monthly_cumulative,
        x=us_monthly_cumulative.index,
        y="RecoveryRatio",
        marker="o",
        color="green"
    )
    plt.title("Monthly Recovery-to-Confirmed Ratio in US (Mar 2020 to May 2021)")
    plt.xlabel("Month")
    plt.ylabel("Recovery Ratio")
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    plt.savefig("visuals/ques8cMonthly_Recovery_to_Confirmed_Ratio_in_US.png")
    plt.show()
    plt.close()

    
ques2a()
ques2b()
ques2c()
ques3_and_4()
ques5()
ques6()
ques7()
ques8()
