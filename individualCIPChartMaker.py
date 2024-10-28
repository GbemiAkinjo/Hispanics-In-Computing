# This will generate a chart for a desired CIP code and Award level.

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

# Specify the CIP_Code and Award_Level to create charts for
specified_cip_code = '11.0101'  # Example: Change this to the desired CIP code
specified_award_level = "Bachelor's degree"  # Example: Change to the desired award level

# Filter the dataframe for the specific CIP_Code and Award_Level
filtered_df = grouped_df[(grouped_df['CIP_Code'] == specified_cip_code) & 
                         (grouped_df['Award_Level'] == specified_award_level)]

# Check the number of universities
num_universities = filtered_df.shape[0]

if num_universities < 3:
    print(f"Not enough universities to create a chart. Found {num_universities} for CIP_Code {specified_cip_code} and Award_Level {specified_award_level}.")
else:
    # Create a directory to store the charts if it doesn't exist
    chart_dir = 'CIP_Award_Level_Charts'
    os.makedirs(chart_dir, exist_ok=True)
    
    # Sanitize the award level for filename
    sanitized_award_level = sanitize_filename(specified_award_level)
    
    # Create a bar chart for the top 10 universities based on the Total Hispanic Student Population
    top_10_universities = filtered_df.nlargest(10, 'Total Hispanic Student Population')
    
    # Set up the bar plot with improved aesthetics
    plt.figure(figsize=(10, 6))
    
    sns.barplot(
        data=top_10_universities,
        x='Total Hispanic Student Population',
        y='University Name',
        color='#0b1d78',  # Color for all bars
    )
    
    # Customize the title, labels, and fonts
    plt.title(f"Top 10 Universities for CIP {specified_cip_code} - {specified_award_level}", 
              fontsize=18, fontweight='bold', fontfamily='Times New Roman')
    plt.xlabel('Total Hispanic Student Population', fontsize=14, fontweight='normal', fontstyle='italic', fontfamily='Times New Roman')
    plt.ylabel('University Name', fontsize=14, fontweight='normal', fontstyle='italic', fontfamily='Times New Roman')
    
    # Adjust gridlines and other chart aesthetics
    # plt.grid(axis='x', linestyle='--', alpha=0.7)  # Gridlines on the x-axis
    plt.xticks(fontsize=12, fontfamily='Times New Roman')  # Adjust the font size and family for x-axis ticks
    plt.yticks(fontsize=12, fontfamily='Times New Roman')  # Adjust the font size and family for y-axis ticks

    # Save the chart to the charts directory
    chart_filename = f"{specified_cip_code}_{sanitized_award_level}_Graph.png"
    plt.savefig(os.path.join(chart_dir, chart_filename), bbox_inches='tight')
    plt.close()  # Close the plot to free memory for the next plot
    
    print(f"Chart saved: {chart_filename}")