# This makes seperate charts for the ranked CIP codes and award levels

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load the CSV file from the current working directory
all_universities_df = pd.read_csv('HSI_universities.csv')

# Remove any single quotes around the CIP_Code values
all_universities_df['CIP_Code'] = all_universities_df['CIP_Code'].astype(str).str.replace("'", "")

# Rename columns for consistency
all_universities_df.rename(columns={
    'Name': 'University Name',
    'Hispanic_Latino_Total': 'Total Hispanic Student Population'
}, inplace=True)

# Group by the desired columns and aggregate based on Hispanic/Latino totals
grouped_df = all_universities_df.groupby(
    ['unitid', 'University Name', 'CIP_Code', 'CIP_Title', 'Award_Level'], as_index=False
).agg({
    'Total Hispanic Student Population': 'sum',  # Sum Hispanic/Latino students
    'Grand_Total': 'sum'  # Sum the overall total if needed
})

# Sort by CIP code and Award level
grouped_df = grouped_df.sort_values(by=['CIP_Code', 'Award_Level'], ascending=[True, True])

# Function to sanitize filenames by replacing or removing unwanted characters
def sanitize_filename(filename):
    return filename.replace("'", "").replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_")

# Create a directory to store the charts if it doesn't exist
chart_dir = 'CIP_Award_Level_Charts'
os.makedirs(chart_dir, exist_ok=True)

# Group by CIP_Code and Award_Level
grouped_by_cip_award = grouped_df.groupby(['CIP_Code', 'Award_Level'])

# Iterate through each CIP_Code and Award_Level combination
for (cip_code, award_level), group in grouped_by_cip_award:
    num_universities = group.shape[0]

    # Check if there are at least 3 universities
    if num_universities < 3:
        print(f"Not enough universities to create a chart for CIP_Code {cip_code} and Award_Level {award_level}. Found {num_universities}.")
        continue  # Skip to the next combination

    # Sanitize the award level for filename
    sanitized_award_level = sanitize_filename(award_level)
    
    # Create a bar chart for the top 10 universities based on the Total Hispanic Student Population
    top_10_universities = group.nlargest(10, 'Total Hispanic Student Population')
    
    # Set up the bar plot with improved aesthetics
    plt.figure(figsize=(10, 6))
    
    # Use a dark blue color for all bars
    dark_blue_color = '#003366'  # Dark blue color
    sns.barplot(
        data=top_10_universities,
        x='Total Hispanic Student Population',
        y='University Name',
        color='#0b1d78',  # Color for all bars
    )
    
    # Customize the title, labels, and fonts
    plt.title(f"Top 10 Universities for CIP {cip_code} - {award_level}", 
              fontsize=18, fontweight='bold', fontfamily='Times New Roman')
    plt.xlabel('Total Hispanic Student Population', fontsize=14, fontweight='normal', fontstyle='italic', fontfamily='Times New Roman')
    plt.ylabel('University Name', fontsize=14, fontweight='normal', fontstyle='italic', fontfamily='Times New Roman')
    
    # Set x-axis ticks to be integers
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Adjust gridlines and other chart aesthetics
    # plt.grid(axis='x', linestyle='--', alpha=0.7)  # Gridlines on the x-axis
    plt.xticks(fontsize=12, fontfamily='Times New Roman')  # Adjust the font size and family for x-axis ticks
    plt.yticks(fontsize=12, fontfamily='Times New Roman')  # Adjust the font size and family for y-axis ticks

    # Save the chart to the charts directory
    chart_filename = f"chart_{cip_code}_{sanitized_award_level}.png"
    plt.savefig(os.path.join(chart_dir, chart_filename), bbox_inches='tight')
    plt.close()  # Close the plot to free memory for the next plot
    
    print(f"Chart saved: {chart_filename}")
