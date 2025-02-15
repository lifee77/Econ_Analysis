import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file (adjust the file path if needed)
data = pd.read_excel('DataForFigure2.1+with+sub+bars+2024.xls')

# Display the first few rows to verify the columns.
print("Columns in data:", data.columns)
print(data.head())

# Define the countries of interest.
countries = ['Nepal', 'Bhutan', 'Laos']

# Filter the data using the correct column name.
filtered_data = data[data['Country name'].isin(countries)]

# Optionally, ensure the 'Country name' values are stripped.
filtered_data['Country name'] = filtered_data['Country name'].str.strip()

# Set the visual style
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

# Create a bar plot using seaborn.
sns.barplot(
    data=filtered_data,
    x='Country name',
    y='Ladder score',
    palette='Set2'
)

plt.title('Happiness Score for Nepal, Bhutan, and Laos (2024)', fontsize=16)
plt.xlabel('Country', fontsize=14)
plt.ylabel('Ladder Score', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
#plt.show()
print(data['Country name'].unique())
