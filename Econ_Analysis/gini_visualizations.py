import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file and clean metadata
file_path = 'gini_world_data.csv'
# Full corrected code for visualizations using Nepal as an example

# Load and clean the dataset
gini_data = pd.read_csv(file_path, skiprows=4).drop(columns=["Unnamed: 68"]).dropna(how="all", axis=0).reset_index(drop=True)

# Transform data to long format for analysis
gini_long = gini_data.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="Gini Index"
)
gini_long = gini_long.dropna(subset=["Gini Index"])
gini_long["Year"] = pd.to_numeric(gini_long["Year"], errors="coerce")


# Function to extract data for a specific country and save to CSV
def extract_country_data(data, country_name, output_path=None):
    """
    Extracts all data for a specific country from the dataset and optionally saves it to a CSV file.
    
    Parameters:
        data (pd.DataFrame): The full dataset.
        country_name (str): The name of the country to extract data for.
        output_path (str): Optional path to save the extracted data as a CSV file.
    
    Returns:
        pd.DataFrame: The extracted data for the specified country.
    """
    country_data = data[data["Country Name"].str.contains(country_name, case=False, na=False)]
    if country_data.empty:
        print(f"No data found for country: {country_name}")
        return None
    if output_path:
        country_data.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    return country_data

# Example usage
nepal_data = extract_country_data(gini_data, "Nepal", "nepal_gini_index_data.csv")
if nepal_data is not None:
    print(nepal_data)



# General Visualization: Line plot for trends across countries
plt.figure(figsize=(14, 8))
sns.lineplot(data=gini_long, x="Year", y="Gini Index", hue="Country Name", legend=None)
plt.title("Trends of Gini Index Across Countries")
plt.xlabel("Year")
plt.ylabel("Gini Index")
# Adding labels for specific countries
countries_to_label = ["Nepal", "United States", "India", "China", "Brazil", "Germany", "South Korea"]
for country in countries_to_label:
    country_data = gini_long[gini_long["Country Name"] == country]
    if not country_data.empty:
        latest_data = country_data[country_data["Year"] == country_data["Year"].max()]
        for _, row in latest_data.iterrows():
            plt.text(row["Year"], row["Gini Index"], country, fontsize=9)
plt.show()

# General Visualization: Heatmap
heatmap_data = gini_long.pivot(index="Country Name", columns="Year", values="Gini Index")
heatmap_data_cleaned = heatmap_data.apply(pd.to_numeric, errors='coerce')

plt.figure(figsize=(16, 10))
sns.heatmap(heatmap_data_cleaned, cmap="YlGnBu", linewidths=0.5, cbar_kws={'label': 'Gini Index'})
plt.title("Gini Index Heatmap Across Countries and Years")
plt.xlabel("Year")
plt.ylabel("Country Name")
plt.show()

# Country-Specific Visualizations
def plot_country_gini(data, country_name):
    country_data = data[data["Country Name"].str.contains(country_name, case=False, na=False)]
    if country_data.empty:
        print(f"No data found for country: {country_name}")
        return

    country_long = country_data.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
        var_name="Year",
        value_name="Gini Index"
    ).dropna(subset=["Gini Index"])
    country_long["Year"] = pd.to_numeric(country_long["Year"], errors="coerce")

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=country_long, x="Year", y="Gini Index")
    plt.title(f"Gini Index Trend for {country_name}")
    plt.xlabel("Year")
    plt.ylabel("Gini Index")
    plt.show()

def bar_chart_country_gini_with_suggestion(data, country_name, years):
    country_data = data[data["Country Name"].str.contains(country_name, case=False, na=False)]
    if country_data.empty:
        print(f"No data found for country: {country_name}")
        return

    available_years = country_data.drop(columns=["Country Name", "Country Code", "Indicator Name", "Indicator Code"]).dropna(axis=1).columns
    available_years = [int(year) for year in available_years if year.isdigit()]
    
    valid_years = [year for year in years if str(year) in country_data.columns and year in available_years]
    if not valid_years:
        print(f"No Gini index data available for {country_name} in the selected years: {years}.")
        print(f"Available years with data for {country_name}: {sorted(available_years)}")
        return

    selected_columns = ["Country Name"] + [str(year) for year in valid_years]
    country_year_data = country_data[selected_columns].melt(
        id_vars=["Country Name"],
        var_name="Year",
        value_name="Gini Index"
    ).dropna(subset=["Gini Index"])

    plt.figure(figsize=(10, 6))
    sns.barplot(data=country_year_data, x="Year", y="Gini Index", palette="viridis")
    plt.title(f"Gini Index for {country_name} in Valid Selected Years")
    plt.xlabel("Year")
    plt.ylabel("Gini Index")
    plt.show()

# Example country: Nepal
plot_country_gini(gini_data, "Nepal")
bar_chart_country_gini_with_suggestion(gini_data, "Nepal", [2000, 2005, 2010, 2015, 2020])