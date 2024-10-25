import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class CSProblemAnalysis:
    def __init__(self, csv_filename):
        """
        Initialize the analysis class with the CSV file path.
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_file_path = os.path.join(self.script_dir, csv_filename)
        self.cs_problems_df = None
        self.latest_category_counts = None
        self.latest_difficulty_counts = None

    def load_data(self):
        """
        Load the dataset from the CSV file.
        """
        try:
            self.cs_problems_df = pd.read_csv(self.dataset_file_path)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"File {self.dataset_file_path} not found.")
    
    def analyze_data(self):
        """
        Perform analysis on the dataset by counting problem types and difficulty levels.
        """
        if self.cs_problems_df is not None:
            self.latest_category_counts = self.cs_problems_df['ProblemType'].value_counts()
            self.latest_difficulty_counts = self.cs_problems_df['Category'].value_counts()
            print("Data analysis completed.")
        else:
            print("Data not loaded. Please load the data first.")
    
    def plot_pie_charts(self):
        """
        Plot pie charts for problem types and difficulty levels distribution.
        """
        if self.latest_category_counts is not None and self.latest_difficulty_counts is not None:
            # Ensure the 'data' directory exists
            output_dir = os.path.join(self.script_dir, 'data')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Created directory: {output_dir}")
            
            # Prepare data for pie charts
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

            # Pie chart for Category distribution with increased font size
            axes[0].pie(self.latest_category_counts, labels=self.latest_category_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 20})
            axes[0].set_title('Problem Types Distribution', fontsize=20)

            # Pie chart for Difficulty distribution with increased font size
            axes[1].pie(self.latest_difficulty_counts, labels=self.latest_difficulty_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 20})
            axes[1].set_title('Distribution of Problems by DifficultyLevel/Category', fontsize=20)

            # Adjust layout
            plt.tight_layout()

            # Save the plot as an image
            pie_chart_path = os.path.join(output_dir, 'cs_problems_distribution.png')
            plt.savefig(pie_chart_path)

            # Show the plot
            plt.show()

            return pie_chart_path
        else:
            print("Data not analyzed. Please analyze the data first.")

# Example usage
if __name__ == "__main__":
    # Create an instance of the class
    analysis = CSProblemAnalysis("data\\computer_science_problems.csv")
    
    # Load the data
    analysis.load_data()
    
    # Perform analysis
    analysis.analyze_data()
    
    # Plot the pie charts
    chart_path = analysis.plot_pie_charts()
    print(f"Chart saved at: {chart_path}")
