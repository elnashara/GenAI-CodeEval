import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib

def plot_data(df, size, title):
    
    # Filter the DataFrame based on the size, if specified
    if size is not None:
        df_filtered = df[df['Size'] == size]
    else:
        df_filtered = df

    # Define the thresholds
    thresholds = [1, 5, 10, 15, 20, 25, 30, 50, "50+"]

    # Initialize a structure to hold the counts for each threshold and prompt
    prompt_counts = {threshold: {prompt: 0 for prompt in df_filtered['prompt_name'].unique()} for threshold in thresholds}

    # Categorize each row into the correct threshold bucket
    for _, row in df_filtered.iterrows():
        for threshold in thresholds[:-1]:
            if row['Percentage'] <= threshold:
                prompt_counts[threshold][row['prompt_name']] += 1
                break
        else:
            # This handles the "50+" category
            prompt_counts["50+"][row['prompt_name']] += 1

    # Define hatches for each percentage range, leaving the last one empty
    hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '']

    # Create a new figure for the combined chart
    plt.figure(figsize=(15, 8))  # Adjusted figure size for better layout

    # For each prompt, create a stacked bar chart with hatches
    bottom_values = np.zeros(len(df_filtered['prompt_name'].unique()))
    bar_width = 0.5  # Further reduced bar width

    for i, threshold in enumerate(thresholds):
        values = [prompt_counts[threshold][prompt] for prompt in df_filtered['prompt_name'].unique()]
        plt.bar(df_filtered['prompt_name'].unique(), values, bottom=bottom_values, label=f'Within {threshold}%', 
                hatch=hatches[i], width=bar_width)
        bottom_values += np.array(values)

    # Add titles and labels with larger font size
    plt.title(title, fontsize=18)
    plt.xlabel('Prompt', fontsize=14)
    plt.ylabel('Number of Problems', fontsize=14)

    plt.title(title, fontsize=20)
    plt.xlabel('Prompt', fontsize=20)
    plt.ylabel('Number of Problems', fontsize=20)
    
    # Increase the font size of the ticks
    plt.xticks(rotation=30, fontsize=20)
    plt.yticks(fontsize=20)

    # Move the legend outside the plot on the right with a larger font size
    plt.legend(title='Percentage Range', loc='upper left', bbox_to_anchor=(1, 1), fontsize=20, title_fontsize=20)

    # Adjust the margins of the plot to ensure the legend and bars fit well
    plt.subplots_adjust(right=0.85)

    # Show the combined chart
    plt.show()

# Load the data from the CSV file
dir = os.path.dirname(__file__)
file_path = pathlib.Path(dir, 'data/aggregate/p1_p7_gpt4o-Aggregate_plot_summary_auto_execution_times.csv')
df = pd.read_csv(file_path)

# Call the function for each use case
plot_data(df, None, 'Number of Solutions within X% of the Best Solution Across All Prompts (All Sizes)')
plot_data(df, 1000, 'Number of Solutions within X% of the Best Runtime (Input Size 1,000)')
plot_data(df, 10000, 'Number of Solutions within X% of the Best Runtime (Input Size 10,000)')
plot_data(df, 100000, 'Number of Solutions within X% of the Best Runtime (Input Size 100,000)')
