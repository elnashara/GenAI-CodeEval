# Preparing and plotting the data for P1, P2, and P3, focusing only on the performance per prompt (regardless of size)
import os
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Re-load the data for P1 for GPT-3.5 Turbor and GPT-4, as the code execution state was reset
dir = os.path.dirname(__file__)

for i in range(1, 8):

    file_human = pathlib.Path(dir, f'data/summary/summary_human/p{i}_human_summary_execution_times.csv')
    file_gpt35turbo = pathlib.Path(dir, f'data/summary/summary-gpt-35turbo/_p{i}_gpt35turbo_summary_auto_execution_times.csv')
    file_gpt4 = pathlib.Path(dir, f'data/summary/summary_gpt-4/p{i}_gpt4_summary_auto_execution_times.csv')
    file_gpt4o = pathlib.Path(dir, f'data/summary/summary_gpt-4o/p{i}_gpt_4o_summary_auto_execution_times.csv')

    # Reading the files into DataFrames
    df_file_human = pd.read_csv(file_human)
    df_gpt35turbo = pd.read_csv(file_gpt35turbo)
    df_gpt4 = pd.read_csv(file_gpt4)
    df_gpt4o = pd.read_csv(file_gpt4o)

    # Adding a 'Model' column to each DataFrame
    df_file_human['Model'] = 'Human Solution'
    df_gpt35turbo['Model'] = 'GPT-3.5 Turbor'
    df_gpt4['Model'] = 'GPT-4'
    df_gpt4o['Model'] = 'GPT-4o'

    # Combining the data from both models
    df_combined = pd.concat([df_file_human, df_gpt35turbo, df_gpt4, df_gpt4o])

    # Plotting the comparison chart with increased font sizes
    plt.figure(figsize=(15, 8))
    sns.barplot(data=df_combined, x='prompt_name', y='Average', hue='Model', palette=['orange', 'green', 'red', 'blue'])

    # Increase font size for labels and title
    plt.xlabel('Prompt', fontsize=20)
    plt.ylabel('Average Execution Time (seconds)', fontsize=20)
    plt.title(f'Comparison of Average Execution Time for Different Prompts in {df_gpt4.iloc[0]["Function"]}', fontsize=20)
    
    # Increase the font size for tick labels
    plt.xticks(rotation=30, fontsize=20)
    plt.yticks(fontsize=20)

    # Increase the font size for the legend
    plt.legend(title='Model', fontsize=20, title_fontsize=20)

    # Show the plot
    plt.show()
