import pandas as pd

# Before running, please make sure that your columns names have been changed to:
# Name - originally Institution Name or some variation
# Year - originally year or some variation
# Major_Type - originally C2023_A.First or Second Major or some variation
# CIP_Code - originally C2023_A.CIP Code -  2020 Classification or some variationor some variation
# CIP_Title - originally CipTitle or some variation
# Award_Level - originally C2023_A.Award Level code or some variation
# Grand_Total - originally C2023_A.Grand total or some variation
# Hispanic_Latino_Total - originally C2023_A.Hispanic or Latino total or some variation
# Hispanic_Latino_Men - originally C2023_A.Hispanic or Latino men or some variation
# Hispanic_Latino_Women - originally C2023_A.Hispanic or Latino men or some variation


# Load the CSV file with all universities
all_universities_df = pd.read_csv('2023_Completions_All_and_Latinos.csv')

# Load the CSV file with updated Hispanic Serving Institutions (HSIs) list
hsi_universities_df = pd.read_csv('2024_HSI_List_HACU.csv')

# This creates the list of HSIs

# Assuming the university names are stored in a column called 'Name' in both CSVs
# If the column names are different, adjust the names accordingly.
matched_universities_df = all_universities_df[all_universities_df['Name'].isin(hsi_universities_df['Name'])]

# Save the matched universities to a new CSV file
matched_universities_df.to_csv('HSI_Universities.csv', index=False)

print(f"Matched {len(matched_universities_df)} programs found and saved to 'HSI_Universities.csv'.")

# This creates the list of non-HSIs

# Make sure the university names are stored in a column called 'Name' in both CSVs !
# If the column names are different, adjust the names accordingly.
non_hsi_universities_df = all_universities_df[~all_universities_df['Name'].isin(hsi_universities_df['Name'])]

# Save the non-HSI universities to a new CSV file
non_hsi_universities_df.to_csv('nonHSI_Universities.csv', index=False)

print(f"Filtered out HSIs. {len(non_hsi_universities_df)} non-HSI university programs saved to 'nonHSI_Universities.csv'.")