# This ranks all of the universities by their CIP code and Award Level

import pandas as pd
import os

# Load the CSV file from the current working directory
all_universities_df = pd.read_csv('HSI_Universities.csv')

# Remove any single quotes around the CIP_Code values
all_universities_df['CIP_Code'] = all_universities_df['CIP_Code'].astype(str).str.replace("'", "")

# Group by the desired columns and aggregate based on Hispanic/Latino totals
grouped_df = all_universities_df.groupby(
    ['unitid', 'Name', 'CIP_Code', 'CIP_Title', 'Award_Level'], as_index=False
).agg({
    'Hispanic_Latino_Total': 'sum',  # Sum Hispanic/Latino students
    'Grand_Total': 'sum'  # Sum the overall total if needed
})

# Sort by CIP code and Award level
grouped_df = grouped_df.sort_values(by=['CIP_Code', 'Award_Level'], ascending=[True, True])

# Create a directory to store the output files if it doesn't exist
output_dir = 'CIP_Award_Level_Files'
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize filenames by replacing or removing unwanted characters
def sanitize_filename(filename):
    return filename.replace("'", "").replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_")

# Iterate through unique combinations of CIP_Code and Award_Level to create separate CSV files
for (cip_code, award_level), group in grouped_df.groupby(['CIP_Code', 'Award_Level']):
    # Sanitize the award level for filename
    sanitized_award_level = sanitize_filename(award_level)
    
    # Define the output filename without the "CIP_Award_Level_Files" portion
    filename = f"{cip_code}_{sanitized_award_level}.csv"
    
    # Save the group to a CSV file in the output directory
    group.to_csv(os.path.join(output_dir, filename), index=False, columns=[
        'unitid', 'Name', 'CIP_Code', 'CIP_Title', 'Award_Level', 'Hispanic_Latino_Total', 'Grand_Total'
    ])
    
    print(f"File saved: {filename}")

print("All files have been created based on CIP code and Award level.")