import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

def plot_summary_result(file):
    # Read data from file
    df = pd.read_csv(file)
    
    print(file)
    problem_number = file.split('_')[0]
    
    # Calculate the percentage difference
    optimal_time = df['Percentage'].min()
    
    # Define the categories
    categories = {
        '0% Optimal': lambda x: x == 0,
        '5% Slower': lambda x: 0 < x <= 5,
        '10% Slower': lambda x: 5 < x <= 10,
        '> 10% Slower': lambda x: x > 10
    }
    
    # Convert 'Prompt' column to a categorical data type with desired order
    category_order = list(categories.keys())
    
    # Categorize the prompts
    df['Category'] = df.groupby('prompt_name')['Percentage'].apply(
        lambda x: x.apply(lambda y: next((category for category, condition in categories.items() if condition(y)), None))
    )
    
    # Calculate the percentage of prompts in each category
    category_counts = df.groupby(['prompt_name', 'Category']).size().unstack(fill_value=0)
    category_percentages = category_counts.div(category_counts.sum(axis=1), axis=0) * 100
    
    # Create the stacked bar chart
    ax = category_percentages.plot(kind='bar', stacked=True, colormap='tab20', width=0.8)
    
    # Add titles and labels with larger font sizes
    plt.xlabel('Prompt', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.title(f"Problem {problem_number} \n Performance Comparison of Prompts", fontsize=18)
    
    # Increase the font size of the ticks
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Adjust legend font size and position
    plt.legend(title='Category', labels=category_order, loc="upper right", bbox_to_anchor=(1.30, 1), fontsize=12, title_fontsize=14)

    # Add percentage labels
    totals = category_counts.sum(axis=1)
    for i, prompt in enumerate(category_percentages.index):
        values = category_percentages.loc[prompt]
        prev_value = 0
        for j, (category, value) in enumerate(values.items()):
            if value == 0.0 or value >= 600:
                continue
            ax.text(i, prev_value + value / 2, f'{value:.1f}%', ha='center', va='center', fontsize=10)  # Added fontsize for text
            prev_value += value
    
    # Display the chart
    plt.show()

if __name__ == '__main__':
    aggregate_file = os.path.join('data', 'aggregate/p1_p7_gpt4o-Aggregate_plot_summary_auto_execution_times.csv')
    dir_path = os.path.dirname(os.path.realpath(__file__))  # This gets the script's directory
    file = os.path.join(dir_path, aggregate_file)
    
    plot_summary_result(file)
