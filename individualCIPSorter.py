# This ranks the universities by a specified CIP code and Award Level

import pandas as pd

# Make sure to change the file name to your desired file
# Load the CSV file from the current working directory
all_universities_df = pd.read_csv('HSI_Universities.csv')

# Remove any single quotes around the CIP_Code values
all_universities_df['CIP_Code'] = all_universities_df['CIP_Code'].astype(str).str.replace("'", "")

# Filter by specific CIP code and Award level code
desired_cip_code = '11.0101'  # Example: '11.0101' for Computer and Information Sciences, General
desired_award_level = 'Bachelor\'s degree'  # Example: "Bachelor's" or numeric code for it

filtered_df = all_universities_df[
    (all_universities_df['CIP_Code'] == desired_cip_code) &
    (all_universities_df['Award_Level'] == desired_award_level)
]

# Sort by Hispanic/Latino student count
# Assuming the column is 'Hispanic_Latino_Total'. Adjust this if needed.
ranked_df = filtered_df.sort_values(by='Hispanic_Latino_Total', ascending=False)

# Reorganize and keep all columns, but repopulate them in the ranked order
# Replace with actual column names as needed
ranked_df = ranked_df[['unitid', 'Name', 'CIP_Code', 'CIP_Title', 'Award_Level', 'Hispanic_Latino_Total', 'Grand_Total']]

# Create a sanitized file name from the CIP code and Award level
safe_cip_code = desired_cip_code.replace('.', '_')
safe_award_level = desired_award_level.replace("'", "").replace(" ", "").replace("degree", "")

# Save the ranked DataFrame to a new CSV file, including the CIP code and Award level in the filename
file_name = f'Ranked_{safe_cip_code}_{safe_award_level}.csv'
ranked_df.to_csv(file_name, index=False)

print(f"Ranked universities saved to '{file_name}'.")