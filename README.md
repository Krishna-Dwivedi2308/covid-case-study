# COVID-19 Data Analysis Project

## Overview

This project performs comprehensive data analysis and visualization of COVID-19 datasets, including confirmed cases, deaths, and recoveries. The code is written in Python and uses libraries such as Pandas, Matplotlib, and Seaborn to load, process, explore, and visualize the data. The analysis addresses various questions, including data exploration, trend visualization, handling missing data, calculating daily and monthly metrics, and generating insights for specific countries.

The project is structured into modular functions (`ques2a`, `ques2b`, `ques2c`, `ques3_and_4`, `ques5`, `ques6`, `ques7`, `ques8`), each addressing specific analysis tasks. Outputs include printed results, CSV files with processed data, and visualizations saved as PNG files.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Data Requirements](#data-requirements)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Function Descriptions](#function-descriptions)
  - [ques2a: Data Exploration](#ques2a-data-exploration)
  - [ques2b: Top 5 Countries Confirmed Cases Plot](#ques2b-top-5-countries-confirmed-cases-plot)
  - [ques2c: China Confirmed Cases Plot](#ques2c-china-confirmed-cases-plot)
  - [ques3_and_4: Handling Missing Data](#ques3_and_4-handling-missing-data)
  - [ques5: Daily Cases and Recovery Rates](#ques5-daily-cases-and-recovery-rates)
  - [ques6: Deaths Analysis](#ques6-deaths-analysis)
  - [ques7: Monthly Data Analysis](#ques7-monthly-data-analysis)
  - [ques8: Advanced Analysis](#ques8-advanced-analysis)
- [Outputs](#outputs)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.8 or higher
- Required Python libraries:
  - pandas
  - matplotlib
  - seaborn

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd covid-19-analysis
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install pandas matplotlib seaborn
   ```

4. **Prepare the Data**:
   - Place the required CSV files in the `data/` directory (see [Data Requirements](#data-requirements)).
   - Ensure the `visuals/` directory exists for saving plots.

## Data Requirements

The project requires three CSV files containing COVID-19 data, typically sourced from repositories like Johns Hopkins University:

- `covid_19_confirmed.csv`: Contains cumulative confirmed cases by country/region and province/state over time.
- `covid_19_deaths.csv`: Contains cumulative deaths by country/region and province/state over time.
- `covid_19_recovered.csv`: Contains cumulative recoveries by country/region and province/state over time.

Each CSV file should have:

- Columns for `Province/State`, `Country/Region`, `Lat`, `Long`, and date columns (e.g., `1/22/20`, `1/23/20`, etc.).
- Ensure consistent formatting across files (e.g., date formats, country names).

Place these files in the `data/` directory.

## Directory Structure

```plaintext
covid-19-analysis/
├── data/
│   ├── covid_19_confirmed.csv
│   ├── covid_19_deaths.csv
│   ├── covid_19_recovered.csv
│   ├── daily_confirmed_cases_per_Country.csv (generated)
│   ├── daily_Deaths_cases_per_country.csv (generated)
│   ├── daily_recovery_cases_per_country.csv (generated)
│   ├── merged_data_of_all_cumulative.csv (generated)
│   ├── ques6b_total_deaths_per_country.csv (generated)
│   ├── ques6c_top_5_countries_with_the_highest_average_daily_deaths.csv (generated)
│   ├── ques7bmonthly_sum_of_confirmed_cases_deaths_and_recoveries.csv (generated)
│   ├── ques7cselect_analysis_for_United States_Italy_and_Brazil.csv (generated)
│   ├── ques8.1three_countries_with_the_highest_average_death_rates.csv (generated)
├── visuals/
│   ├── top5_covid_trends.png (generated)
│   ├── china_covid_trend.png (generated)
│   ├── Top_5_daily_spike_in_cases.png (generated)
│   ├── ques6d_US_deaths_lineplot.png (generated)
│   ├── ques8brecoveries_vs_deaths_SA.png (generated)
│   ├── ques8cMonthly_Recovery_to_Confirmed_Ratio_in_US.png (generated)
├── main.py
├── README.md
```

## Usage

1. Ensure the `data/` directory contains the required CSV files.
2. Create a `visuals/` directory if it doesn't exist:
   ```bash
   mkdir visuals
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. The script will:
   - Load the datasets.
   - Execute all analysis functions (`ques2a` to `ques8`).
   - Print results to the console.
   - Save processed data as CSV files in the `data/` directory.
   - Save visualizations as PNG files in the `visuals/` directory.

To run specific functions, comment out unwanted function calls in `main.py`.

## Function Descriptions

### ques2a: Data Exploration

**Purpose**: Explores the structure of the confirmed, deaths, and recovered datasets.

**Actions**:
- Prints the shape (rows, columns), column names, data types, missing values, and a preview of each dataset.
- Uses a helper function `explore_dataset` to process each dataset.

**Output**:
- Console output with dataset details (shape, columns, data types, missing values, head).

### ques2b: Top 5 Countries Confirmed Cases Plot

**Purpose**: Visualizes the trend of confirmed COVID-19 cases over time for the top 5 countries with the highest total cases.

**Actions**:
- Aggregates confirmed cases by country, dropping `Province/State`, `Lat`, and `Long`.
- Identifies the top 5 countries by total cases.
- Melts the data for plotting (converts to long format with `Country/Region`, `Date`, `Confirmed`).
- Converts `Date` to datetime format.
- Plots a line graph using Seaborn.

**Output**:
- Line plot saved as `visuals/top5_covid_trends.png`.
- Displays the plot.

### ques2c: China Confirmed Cases Plot

**Purpose**: Visualizes the trend of confirmed COVID-19 cases over time for China.

**Actions**:
- Similar to `ques2b`, but focuses on China only.
- Aggregates data, melts it, and converts `Date` to datetime.
- Plots a line graph in red using Seaborn.

**Output**:
- Line plot saved as `visuals/china_covid_trend.png` (300 DPI).
- Displays the plot.

### ques3_and_4: Handling Missing Data

**Purpose**: Processes missing values in the confirmed, deaths, and recovered datasets.

**Actions**:
- Fills missing `Province/State` values with "All Provinces".
- Drops rows with missing `Lat` or `Long` values (as they are critical for geospatial analysis).
- Prints missing value counts before and after processing.

**Output**:
- Console output with missing value counts for each dataset.

### ques5: Daily Cases and Recovery Rates

**Purpose**: Analyzes daily cases, recovery rates, and death rates.

**Sub-tasks**:
1. **Daily Cases (5.1)**:
   - Calculates daily differences from cumulative data for confirmed, deaths, and recoveries.
   - Saves daily data to CSV files.
   - Identifies the maximum single-day surge in confirmed cases and the top 5 surges.
   - Plots a bar chart of the top 5 daily surges.
2. **Recovery Rates (5.2)**:
   - Calculates recovery rates for Canada and Australia as of December 31, 2020.
3. **Death Rates in Canada (5.3)**:
   - Calculates death rates by province in Canada for the latest date.
   - Identifies provinces with the highest and lowest death rates.

**Output**:
- CSV files: `data/daily_confirmed_cases_per_Country.csv`, `data/daily_Deaths_cases_per_country.csv`, `data/daily_recovery_cases_per_country.csv`.
- Bar plot: `visuals/Top_5_daily_spike_in_cases.png`.
- Console output: daily cases, maximum surge details, recovery rates, and death rates.

### ques6: Deaths Analysis

**Purpose**: Analyzes death-related metrics.

**Sub-tasks**:
1. **Melted Deaths Data (6.1)**:
   - Melts the deaths dataset into a long format (`Country/Region`, `Province/State`, `Lat`, `Long`, `Date`, `Deaths`).
2. **Total Deaths per Country (6.2)**:
   - Sums daily deaths per country and saves to CSV.
3. **Top 5 Countries by Average Daily Deaths (6.3)**:
   - Calculates mean daily deaths per country and identifies the top 5.
   - Saves results to CSV.
4. **US Deaths Plot (6.4)**:
   - Plots cumulative deaths in the US over time.

**Output**:
- CSV files: `data/ques6b_total_deaths_per_country.csv`, `data/ques6c_top_5_countries_with_the_highest_average_daily_deaths.csv`.
- Line plot: `visuals/ques6d_US_deaths_lineplot.png`.
- Console output: melted deaths data, total deaths, top 5 average daily deaths.

### ques7: Monthly Data Analysis

**Purpose**: Analyzes monthly cumulative and new cases.

**Sub-tasks**:
1. **Merged Data (7.1)**:
   - Melts confirmed, deaths, and recovered datasets and merges them.
   - Saves merged data to CSV.
2. **Monthly New Cases (7.2)**:
   - Calculates monthly new confirmed cases, deaths, and recoveries by country.
   - Saves results to CSV.
3. **Selected Countries Analysis (7.3)**:
   - Filters monthly data for the US, Italy, and Brazil.
   - Saves results to CSV.

**Output**:
- CSV files: `data/merged_data_of_all_cumulative.csv`, `data/ques7bmonthly_sum_of_confirmed_cases_deaths_and_recoveries.csv`, `data/ques7cselect_analysis_for_United States_Italy_and_Brazil.csv`.
- Console output: merged data preview, monthly data, and selected countries data.

### ques8: Advanced Analysis

**Purpose**: Performs advanced analyses on death rates and specific country trends.

**Sub-tasks**:
1. **Top 3 Countries by Average Death Rate (8.1)**:
   - Calculates average death rates (daily deaths / daily confirmed cases) per country.
   - Identifies the top 3 countries and saves to CSV.
2. **South Africa Recoveries vs. Deaths (8.2)**:
   - Plots recoveries vs. deaths over time for South Africa.
3. **US Recovery Ratio (8.3)**:
   - Calculates and plots the monthly recovery-to-confirmed ratio for the US from March 2020 to May 2021.

**Output**:
- CSV file: `data/ques8.1three_countries_with_the_highest_average_death_rates.csv`.
- Line plots: `visuals/ques8brecoveries_vs_deaths_SA.png`, `visuals/ques8cMonthly_Recovery_to_Confirmed_Ratio_in_US.png`.
- Console output: top 3 death rates, South Africa data.

## Outputs

- **CSV Files**: Generated data files are saved in the `data/` directory (listed in [Directory Structure](#directory-structure)).
- **Visualizations**: Plots are saved as PNG files in the `visuals/` directory.
- **Console Output**: Detailed analysis results, including dataset summaries, metrics, and insights.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

Please ensure code follows PEP 8 style guidelines and includes appropriate documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.