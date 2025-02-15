import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file with header row set to row index 3 (i.e. 4th row)
file_path = '/mnt/data/National_Results_MPI_2024.xlsx'
data = pd.read_excel(file_path, header=3)

# Inspect the columns (they will be mostly "Unnamed: x")
print("Columns in data:", data.columns)

# Rename the first column (which should contain the country names) to "Country"
data = data.rename(columns={data.columns[0]: 'Country'})

# Standardize country names to title case and strip extra spaces
data['Country'] = data['Country'].str.strip().str.title()

# Print unique country names to verify that our target countries are present
print("Unique countries:", data['Country'].unique())

# Define the three countries of interest.
countries = ['Nepal', 'Bhutan', 'Laos']

# Filter the data for these three countries.
filtered_data = data[data['Country'].isin(countries)]
print("Filtered data:")
print(filtered_data)

# For demonstration purposes, display all MPI-related indicators.
# (Assuming that all columns except 'Country' are MPI and related sub-indicators.)
print("MPI and related indicators for selected countries:")
print(filtered_data.to_string(index=False))

# -------------------------
# Plotting the MPI indicator for the three countries.
# We assume that the first numeric column after "Country" (i.e., column index 1) holds the main MPI value.
mpi_col = data.columns[1]
print("Using column '{}' as the MPI indicator for plotting.".format(mpi_col))

sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
sns.barplot(data=filtered_data, x='Country', y=mpi_col, palette='Set2')
plt.title('MPI Indicator for Nepal, Bhutan, and Laos (2024)', fontsize=16)
plt.xlabel('Country', fontsize=14)
plt.ylabel(mpi_col, fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
