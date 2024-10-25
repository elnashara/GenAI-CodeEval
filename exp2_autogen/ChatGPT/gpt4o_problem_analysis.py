import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class GPT4oProblemAnalysis:
    def __init__(self, csv_filename):
        """
        Initialize the class with the CSV file path and load the dataset.
        """
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.dataset_file_path = os.path.join(dir_path, csv_filename)
        self.document_df = pd.read_csv(self.dataset_file_path)
    
    def plot_problem_status_count(self):
        """
        Group by 'problem_number' and 'status' to count pass/fail cases and plot the bar chart.
        """
        problem_status_count_new = self.document_df.groupby(['problem_number', 'status']).size().unstack(fill_value=0)

        colors = ["#1f77b4", "#ff7f0e"]  # Blue for pass, Orange for fail
        problem_status_count_new.plot(kind='bar', stacked=True, color=colors, figsize=(12, 6))

        plt.title('Number of Pass and Fail Test Cases for Each Problem Using GPT-4o', fontsize=20)
        plt.xlabel('Problem Number', fontsize=20)
        plt.ylabel('Number of Test Cases', fontsize=20)
        plt.xticks(rotation=0, fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(title='Status', fontsize=20, title_fontsize=20)
        plt.tight_layout()

        # Display the chart
        plt.show()

    def plot_problem_category_distribution(self):
        """
        Plot a bar chart showing the distribution of problem categories.
        """
        category_counts = self.document_df['category'].value_counts()
        plt.figure(figsize=(10, 6))
        category_counts.plot(kind='bar')
        plt.title('GPT-4o - Distribution of Problem Categories', fontsize=20)
        plt.xlabel('Category', fontsize=20)
        plt.ylabel('Frequency', fontsize=20)
        plt.xticks(rotation=45, fontsize=20)
        plt.yticks(fontsize=20)
        plt.tight_layout()
        plt.show()

    def plot_pass_rate_pie_chart(self):
        """
        Generate a pie chart for the pass rate of solutions.
        """
        pass_counts = self.document_df['pass'].value_counts()
        plt.figure(figsize=(8, 8))
        pass_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, textprops={'fontsize': 20})
        plt.title('GPT-4o - Pass Rate of Solutions', fontsize=20)
        plt.ylabel('')  # Hide the y-label
        plt.tight_layout()
        plt.show()

    def plot_problem_index_vs_status(self):
        """
        Generate a line graph showing problem index vs. pass/fail status.
        """
        status_numerical = self.document_df['status'].apply(lambda x: 1 if x == 'PASS' else 0)
        plt.figure(figsize=(14, 6))
        plt.plot(self.document_df['index'], status_numerical, marker='o')
        plt.title('GPT-4o - Problem Index vs. Pass/Fail Status', fontsize=20)
        plt.xlabel('Problem Index', fontsize=20)
        plt.ylabel('Status (1=Pass, 0=Fail)', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_problem_statement_length_histogram(self):
        """
        Generate a histogram for the length of the problem statements.
        """
        problem_lengths = self.document_df['problem'].apply(len)
        plt.figure(figsize=(10, 6))
        plt.hist(problem_lengths, bins=20)
        plt.title('GPT-4o - Histogram of Problem Statement Lengths', fontsize=20)
        plt.xlabel('Length of Problem Statement', fontsize=20)
        plt.ylabel('Frequency', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def plot_success_rate_by_difficulty(self):
        """
        Calculate and plot success rates for each problem difficulty category.
        """
        success_rate = self.document_df.groupby('category')['pass'].mean()

        plt.figure(figsize=(10, 6))
        bar_plot = sns.barplot(x=success_rate.index, y=success_rate.values * 100)  # Convert to percentage
        plt.title('GPT-4o - Problem Difficulty vs. Success Rate', fontsize=20)
        plt.ylabel('Success Rate (%)', fontsize=20)
        plt.xlabel('Problem Difficulty', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        # Add success rate values on top of bars
        for p in bar_plot.patches:
            height = p.get_height()
            plt.text(p.get_x() + p.get_width()/2., height + 0.5, '{:1.2f}%'.format(height), ha='center', va='bottom', fontsize=20)

        plt.tight_layout()
        plt.show()

    def plot_problem_type_and_category(self):
        """
        Plot success and failure cases for problem types and categories.
        """
        category_analysis = self.document_df.groupby(['problem_type', 'category'])['status'].value_counts().unstack().fillna(0)
        category_analysis = category_analysis.rename(columns={'PASS': 'Success', 'FAIL': 'Failure'})

        # Plotting the new graph
        plt.figure(figsize=(10, 6))
        category_analysis.plot(kind='bar', stacked=False, figsize=(10, 6))

        # Adding labels and title
        plt.title('GPT-4o Success and Failure Analysis by Problem Type and Category', fontsize=20)
        plt.xlabel('Problem Type and Category', fontsize=20)
        plt.ylabel('Number of Test Cases', fontsize=20)
        plt.xticks(rotation=45, ha='right', fontsize=20)
        plt.yticks(fontsize=20)

        plt.tight_layout()
        plt.show()

# Example usage:
if __name__ == "__main__":
    analysis = GPT4oProblemAnalysis("data\\Prompt1_ChatGPT4o_NaiveApproach.csv")

    # Plot the various visualizations
    analysis.plot_problem_status_count()
    analysis.plot_problem_category_distribution()
    analysis.plot_pass_rate_pie_chart()
    analysis.plot_problem_index_vs_status()
    analysis.plot_problem_statement_length_histogram()
    analysis.plot_success_rate_by_difficulty()
    analysis.plot_problem_type_and_category()
