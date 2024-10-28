# This ranks the universities by their CIP code, totalling all the levels to form its ranking

import pandas as pd

# Make sure to change the file name to your desired file
# Load the CSV file from the current working directory
all_universities_df = pd.read_csv('HSI_Universities.csv')

# Remove any single quotes around the CIP_Code values
all_universities_df['CIP_Code'] = all_universities_df['CIP_Code'].astype(str).str.replace("'", "")

# Filter by specific CIP code (consider all award levels for that CIP code)
desired_cip_code = '11.0101'  # Example: '52.0101' for Business

filtered_df = all_universities_df[
    all_universities_df['CIP_Code'] == desired_cip_code
]

# Group by university (assuming 'Name' or 'unitid' identifies each university) and sum the Hispanic/Latino totals
grouped_df = filtered_df.groupby(['unitid', 'Name', 'CIP_Code', 'CIP_Title']).agg(
    Hispanic_Latino_Total_Sum=('Hispanic_Latino_Total', 'sum'),
    Grand_Total_Sum=('Grand_Total', 'sum')
).reset_index()

# Sort by the total Hispanic/Latino student count across all award levels
ranked_df = grouped_df.sort_values(by='Hispanic_Latino_Total_Sum', ascending=False)

# Save the ranked DataFrame to a new CSV file
safe_cip_code = desired_cip_code.replace('.', '_')
file_name = f'Ranked_{safe_cip_code}_All_Award_Levels.csv'
ranked_df.to_csv(file_name, index=False)

print(f"Ranked universities saved to '{file_name}'.")
