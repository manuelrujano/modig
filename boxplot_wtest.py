import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

# Function to calculate peak depth for regions
def calculate_peak_depth_samtools(depth_file, regions):
    depth_data = pd.read_csv(depth_file, sep='\\s+', names=['chrom', 'position', 'depth'])
    peak_depths = []

    for region in regions:
        chrom, start, end = region
        region_data = depth_data[(depth_data['chrom'] == chrom) &
                                 (depth_data['position'] >= start) &
                                 (depth_data['position'] <= end)]
        peak_depth = region_data['depth'].max() if not region_data.empty else 0
        peak_depths.append(peak_depth)

    return peak_depths

# Define depth files and regions 
# 
# Outlier?
#    
#    

depth_files = {
    "1E": "/Users/xrujma/bin/tools/scripts/depth_results/1E_normalized_depth.txt",
    "1N": "/Users/xrujma/bin/tools/scripts/depth_results/1N_normalized_depth.txt",
    "2E": "/Users/xrujma/bin/tools/scripts/depth_results/2E_normalized_depth.txt",
    "2N": "/Users/xrujma/bin/tools/scripts/depth_results/2N_normalized_depth.txt",
    "3E": "/Users/xrujma/bin/tools/scripts/depth_results/3E_normalized_depth.txt",
    "3N": "/Users/xrujma/bin/tools/scripts/depth_results/3N_normalized_depth.txt",
    "4E": "/Users/xrujma/bin/tools/scripts/depth_results/4E_normalized_depth.txt",
    "4N": "/Users/xrujma/bin/tools/scripts/depth_results/4N_normalized_depth.txt",
    "5E": "/Users/xrujma/bin/tools/scripts/depth_results/5E_normalized_depth.txt",
    "5N": "/Users/xrujma/bin/tools/scripts/depth_results/5N_normalized_depth.txt",
    "6E": "/Users/xrujma/bin/tools/scripts/depth_results/6E_normalized_depth.txt",
    "6N": "/Users/xrujma/bin/tools/scripts/depth_results/6N_normalized_depth.txt",
    "2A": "/Users/xrujma/bin/tools/scripts/depth_results/2A_normalized_depth.txt",
    "2C": "/Users/xrujma/bin/tools/scripts/depth_results/2C_normalized_depth.txt", 
    "3A": "/Users/xrujma/bin/tools/scripts/depth_results/3A_normalized_depth.txt",
    "3C": "/Users/xrujma/bin/tools/scripts/depth_results/3C_normalized_depth.txt",
    "9A": "/Users/xrujma/bin/tools/scripts/depth_results/9A_normalized_depth.txt",
    "9C": "/Users/xrujma/bin/tools/scripts/depth_results/9C_normalized_depth.txt"
}
regions = [("chr9", 4490518, 4490548)]

# Collect peak depth data for all files
depth_values = {label: calculate_peak_depth_samtools(file, regions)[0] for label, file in depth_files.items()}

# Prepare the data for the DataFrame
data = []

for label, depth in depth_values.items():
    if "E" in label or "A" in label:  # Endometriosis cases
        group = "Endometriosis"
    elif "N" in label or "C" in label:  # Control cases
        group = "Control"
    else:
        continue  # Skip if label doesn't match expected patterns
    data.append({"Patient": label, "Group": group, "Depth": depth})

# Create the df
df = pd.DataFrame(data)

# Export the df
output_path = "/Users/xrujma/bin/tools/scripts/output_normalized.xlsx"  # Replace with your desired file path
df.to_excel(output_path, index=False, sheet_name="Depth Data")

# Create the boxplot with the statistical test
plt.figure(figsize=(8, 6))
sns.set(style="whitegrid")

# boxplot
boxplot = sns.boxplot(x="Group", y="Depth", data=df, palette="pastel")
sns.swarmplot(x="Group", y="Depth", data=df, color="red", size=10, dodge=True, ax=boxplot)

# Perform the Wilcoxon signed-rank test for paired data
endo = df[df['Group'] == 'Endometriosis']['Depth'].values
control = df[df['Group'] == 'Control']['Depth'].values
stat, p_value = wilcoxon(endo, control)

# Get the y-position for the line (a bit above the max depth value)
ymax = df['Depth'].max() * 1.05 

# Draw a line between the two groups to indicate comparison
plt.plot([0, 1], [ymax, ymax], color='black', lw=2)

# Add p-value annotation on the line
boxplot.text(0.5, ymax + 0.02, f'P-value = {p_value:.4f}', ha='center', va='bottom', fontsize=14, color="black")


# labels and title
boxplot.set_title("Total depth distribution in region chr9:4490518-4490548", fontsize=18)
boxplot.set_xlabel("Nine patients with endometriosis", fontsize=16)
boxplot.set_ylabel("Normalized read depth", fontsize=16)

# font size of x-axis group labels
plt.xticks(fontsize=16)

# Show the plot
plt.tight_layout()
plt.show()

# Output the p-value
print(f"Wilcoxon signed-rank test: statistic = {stat}, p-value = {p_value}")
