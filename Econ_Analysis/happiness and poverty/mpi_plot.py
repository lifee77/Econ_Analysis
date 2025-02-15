import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------
# STEP 1: Read the entire sheet
# -----------------------------
file_path = "National_Results_MPI_2024.xlsx"
sheet_name = 0  # or use the actual sheet name if not the first
df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

# Drop fully empty rows at the top/bottom (just in case)
df_raw.dropna(how='all', inplace=True)
df_raw.reset_index(drop=True, inplace=True)

# -----------------------------
# STEP 2: Locate the header row
# -----------------------------
# We'll look for a row containing "Country" and "MPI" (or partial matches).
# Adjust as needed if your file uses different keywords (like "Multidimensional poverty index").
required_keywords = ["Country", "Multidimensional poverty"]  # minimal set

header_row_index = None
for i in range(len(df_raw)):
    row_values = df_raw.iloc[i].astype(str).tolist()
    # Check if each required keyword appears in this row
    if all(any(req.lower() in cell.lower() for cell in row_values) for req in required_keywords):
        header_row_index = i
        break

if header_row_index is None:
    raise ValueError(
        f"Could not find a row containing these keywords: {required_keywords}. "
        "Please adjust the search logic or check the file."
    )

# -----------------------------
# STEP 3: Set that row as header
# -----------------------------
df_raw.columns = df_raw.iloc[header_row_index].astype(str).str.strip()
df = df_raw[header_row_index+1:].copy()
df.reset_index(drop=True, inplace=True)

# Remove any rows that are entirely NaN after the header
df.dropna(how='all', inplace=True)

# -----------------------------
# STEP 4: Clean/Rename Columns
# -----------------------------
# Print columns to see what they look like
# print("Columns after header assignment:", df.columns.tolist())

# Example: rename columns if you see partial matches in the screenshot.
# Adjust these mappings to your exact column labels (the text might differ).
rename_map = {
    "Multidimensional poverty index (MPI = H x A)": "MPI",
    "Headcount ratio: Population in multidimensional poverty (H)": "H",
    "Intensity of deprivation among the poor (A)": "A",
    "Vulnerable to poverty (who experience 20-33.32% intensity of deprivation)": "Vulnerable",
    "In severe poverty (severity 50% or higher)": "Severe",
    "Headcount ratio: population in multidimensional destitution poverty (D)": "D",
    "Proportion of poor who are destitute": "DestituteProp"
}

# We'll try to rename by looking for partial matches as well:
for col in df.columns:
    col_stripped = col.strip().lower()
    for key, val in rename_map.items():
        if key.lower() in col_stripped:
            df.rename(columns={col: val}, inplace=True)

# Also rename "Country" if it’s slightly different (e.g. "ISO country code" or similar)
# For demonstration, if your file just says "Country" or something else, adjust as needed:
# e.g., if the actual column is "Country name" or "ISO country name"
for col in df.columns:
    if "country" in col.lower():
        df.rename(columns={col: "Country"}, inplace=True)

# Strip whitespace from final column names
df.columns = df.columns.str.strip()

# Print final columns
# print("Final columns:", df.columns.tolist())

# -----------------------------
# STEP 5: Filter for Nepal, Laos, Bhutan
# -----------------------------
countries_of_interest = ["Nepal", "Laos", "Bhutan"]

if "Country" not in df.columns:
    raise KeyError("Could not find a column named 'Country'. Adjust rename logic accordingly.")

df_filtered = df[df["Country"].isin(countries_of_interest)].copy()

# Ensure MPI column is present
if "Multidimensional poverty" not in df_filtered.columns:
    raise KeyError("Could not find a column named 'MPI'. Adjust rename logic accordingly.")

# Convert numeric columns to float (if they are strings)
for col in ["MPI", "H", "A", "Vulnerable", "Severe", "D", "DestituteProp"]:
    if col in df_filtered.columns:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

df_filtered.dropna(subset=["MPI"], inplace=True)

# -----------------------------
# STEP 6: Plot 1 – Overall MPI
# -----------------------------
overall_mpi = df_filtered.set_index("Country")["MPI"]

plt.figure(figsize=(8, 6))
bars = plt.bar(overall_mpi.index, overall_mpi.values, color=["#4e79a7", "#f28e2b", "#76b7b2"])
plt.title("Overall MPI Comparison")
plt.ylabel("MPI Score")
plt.ylim(0, max(overall_mpi.values) * 1.2)

# Annotate each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + 0.01,
        f"{yval:.3f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

# -----------------------------
# STEP 7: Plot 2 – Grouped Bar
# -----------------------------
# Choose which dimensions you want to compare. 
# From your screenshot, we might pick: H, A, Vulnerable, Severe, D, DestituteProp
dimensions = []
for possible_col in ["H", "A", "Vulnerable", "Severe", "D", "DestituteProp"]:
    if possible_col in df_filtered.columns:
        dimensions.append(possible_col)

# Build a dictionary of dimension scores for each country
data = {}
for country in countries_of_interest:
    row = df_filtered[df_filtered["Country"] == country]
    if row.empty:
        continue
    data[country] = []
    for dim in dimensions:
        data[country].append(row[dim].values[0] if dim in row.columns else 0)

x = np.arange(len(dimensions))
width = 0.25

plt.figure(figsize=(10, 6))
for idx, country in enumerate(countries_of_interest):
    if country in data:
        offset = (idx - 1) * width  # shift bars left/right for each country
        plt.bar(x + offset, data[country], width, label=country)

plt.xticks(x, dimensions)
plt.ylabel("Score")
plt.title("Comparison of Poverty Dimensions by Country")
max_val = max([max(vals) for vals in data.values()]) if data else 0
plt.ylim(0, max_val * 1.2 if max_val else 1)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# STEP 8: Plot 3 – Radar Chart
# -----------------------------
# Convert dimension data to a long-form DataFrame
radar_data = []
for country in data:
    for dim, val in zip(dimensions, data[country]):
        radar_data.append({"Country": country, "Dimension": dim, "Score": val})

df_radar = pd.DataFrame(radar_data)

fig = px.line_polar(
    df_radar,
    r="Score",
    theta="Dimension",
    color="Country",
    line_close=True,
    title="Radar Chart of Poverty Dimensions"
)
fig.update_traces(fill="toself")
fig.show()
