## 📊 Question 2.2: Visualizing Top 5 Countries with Highest COVID-19 Confirmed Cases

This section focuses on analyzing global COVID-19 data by identifying the top 5 most affected countries based on confirmed cases and visualizing their trends over time.

---

### ✅ Approach

We follow a step-by-step data processing and visualization pipeline:

#### 1. 🔍 Drop Unnecessary Columns
- Remove `"Province/State"`, `"Lat"`, and `"Long"` columns to simplify the dataset to country-level information.

#### 2. 🌍 Aggregate Data by Country
- Group the dataset by `"Country/Region"`.
- Sum all the date columns to get cumulative confirmed cases for each country over time.

#### 3. ➕ Compute Total Cases
- Add a new column called `"Total"` which contains the sum of all confirmed cases across all dates for each country.

#### 4. 🏆 Identify Top 5 Most Affected Countries
- Sort the countries in descending order based on the `"Total"` confirmed cases.
- Extract the top 5 countries from this sorted list.

#### 5. 🧹 Clean Country Names
- Strip whitespace from `"Country/Region"` entries to ensure reliable indexing and data retrieval.

#### 6. 📤 Extract Top 5 Countries' Data
- Retrieve only the rows corresponding to the top 5 countries.
- Reset the DataFrame index for better readability and processing.

#### 7. 🔄 Reshape Data for Visualization
- Use the `melt()` function to convert the wide-format DataFrame to long-format:
  - Each row now corresponds to a single country-date-confirmed-case record.
- Drop the `"Total"` column before melting as it's no longer needed.

#### 8. 📅 Format the Date Column
- Convert the `"Date"` column to `datetime` format for accurate plotting and time-series analysis.

#### 9. 📈 Plot the Trend Graph
- Use Seaborn’s `lineplot` to create a time-series graph:
  - **X-axis:** Date  
  - **Y-axis:** Number of Confirmed Cases  
  - **Hue:** Different lines for each of the top 5 countries
- Add title, axis labels, grid, and adjust layout for clarity.

#### 10. 💾 Save the Visualization
- Export the final graph as an image to the `visuals/` folder with the filename:
  - `top5_covid_trends.png`

---

### 📌 Output

A line chart displaying the daily cumulative confirmed COVID-19 cases for the **top 5 most affected countries**, allowing us to observe and compare their progression trends over time.

---
## 📊 Question 2.3: Plotting Confirmed COVID-19 Cases Over Time for China

This section focuses on visualizing the time-series trend of confirmed COVID-19 cases specifically for China.

---

### ✅ Approach

We follow a clear sequence of data preparation and visualization steps:

#### 1. 🇨🇳 Filter Data for China
- Extract only the rows related to `"China"` from the `confirmed_totals` DataFrame.
- Reset the index for easier manipulation.

#### 2. 🔄 Reshape Data to Long Format
- Use `pd.melt()` to convert the dataset from wide format (dates as columns) to long format.
- This results in columns: `"Country/Region"`, `"Date"`, and `"Confirmed"`.
- Drop the `"Total"` column before melting since it is not needed for plotting.

#### 3. 📅 Convert Date Strings to datetime Objects
- Convert the `"Date"` column from string format to Python datetime objects using the specified format `%m/%d/%y`.
- This allows accurate time-series plotting on the x-axis.

#### 4. 📈 Plot the Trend of Confirmed Cases Over Time
- Create a line plot with:
  - **X-axis:** Date  
  - **Y-axis:** Number of confirmed COVID-19 cases  
  - **Color:** Red line to represent China’s data clearly
- Enhance the plot with a descriptive title, axis labels, gridlines, and a tight layout for clarity.

#### 5. 💾 Save and Display the Plot
- Save the plot image to the `visuals/` directory as `china_covid_trend.png` with high resolution (`dpi=300`).
- Show the plot inline.
- Close the plot to free up memory.

---

### 📌 Output

A clean and informative line chart displaying the progression of confirmed COVID-19 cases over time in **China**, useful for observing the outbreak trend in this country.

---
