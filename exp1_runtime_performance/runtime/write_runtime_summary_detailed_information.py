from collections import defaultdict
import os
import csv
import pandas as pd

class WriteRuntimeSummaryDetailedInformation:
    """
    A class to handle the writing of detailed and summary runtime information to CSV files.

    Attributes:
        problem_number (int): The number representing the problem being evaluated.
        problem (str): The description of the problem being evaluated.
        dir (str): The directory where the output files will be stored.

    Methods:
        write_runtime_detailed_information(data, output_detailed_file): Writes detailed runtime information to a CSV file.
        write_runtime_summary_information(output_detailed_file, output_summary_file): Writes summary runtime information to a CSV file.
        calc_percentage(output_summary_file): Calculates the percentage difference between average runtimes and the minimum average per size.
    """

    def __init__(self, problem_number, problem, dir):
        """
        Initializes the WriteRuntimeSummaryDetailedInformation class with the provided problem number, problem description, and directory.

        Args:
            problem_number (int): The number of the problem being evaluated.
            problem (str): The description of the problem being evaluated.
            dir (str): The directory where the output files will be stored.
        """
        self.problem_number = problem_number
        self.problem = problem
        self.dir = dir

    def write_runtime_detailed_information(self, data, output_detailed_file):
        """
        Writes detailed runtime information, including minimum, average, and maximum execution times, to a CSV file.

        Args:
            data (list): A list of dictionaries containing runtime information for each test case.
            output_detailed_file (str): The name of the CSV file where detailed runtime information will be stored.

        Returns:
            None
        """
        result = defaultdict(lambda: defaultdict(list))
        file_loc = os.path.join(self.dir, 'results', output_detailed_file)
        write_header = False
        if not os.path.isfile(file_loc):
            write_header = True

        # Write detailed information to the CSV file
        with open(file_loc, mode='a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(['problem', 'prompt_name', 'code_index', 'code_segment', 'Size', 'Min', 'Average', 'Max', 'Exception'])

            for row in data:
                prompt_name = row['prompt_name']
                size = row['size']

                result[(prompt_name, size)]['min_time'].append(row['min_time'])
                result[(prompt_name, size)]['avg_time'].append(row['avg_time'])
                result[(prompt_name, size)]['max_time'].append(row['max_time'])

                writer.writerow([self.problem, prompt_name, row['code_index'], [row['code_segment']], size, row['min_time'], row['avg_time'], row['max_time'], row['Exception']])

    def write_runtime_summary_information(self, output_detailed_file, output_summary_file):
        """
        Writes summary runtime information, including minimum, average, and maximum execution times, to a CSV file.

        Args:
            output_detailed_file (str): The name of the detailed runtime information CSV file.
            output_summary_file (str): The name of the summary runtime information CSV file.

        Returns:
            None
        """
        result = defaultdict(lambda: defaultdict(list))
        file_loc_detailed = os.path.join(self.dir, 'results', output_detailed_file)

        if not os.path.exists(file_loc_detailed):
            return

        data = pd.read_csv(file_loc_detailed, encoding='latin-1')

        # Iterate over the rows of the detailed runtime data
        for index, row in data.iterrows():
            prompt_name = row['prompt_name']
            size = row['Size']
            min_time = row['Min']
            avg_time = row['Average']
            max_time = row['Max']

            if min_time == 0 or min_time == 600:
                continue

            result[(prompt_name, size)]['min_time'].append(min_time)
            result[(prompt_name, size)]['avg_time'].append(avg_time)
            result[(prompt_name, size)]['max_time'].append(max_time)

        write_header = False
        file_loc_summary = os.path.join(self.dir, 'results', output_summary_file)
        if not os.path.isfile(file_loc_summary):
            write_header = True

        # Write summary information to the CSV file
        with open(file_loc_summary, mode='a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(['Size', 'prompt_name', 'Function', 'Min', 'Average', 'Max'])

            for (prompt_name, size), times in result.items():
                min_time = min(times['min_time'])
                avg_time = sum(times['avg_time']) / len(times['avg_time'])
                max_time = max(times['max_time'])

                writer.writerow([size, str(prompt_name), self.problem, min_time, avg_time, max_time])

    def calc_percentage(self, output_summary_file):
        """
        Calculates the percentage difference between the average runtimes and the minimum average runtime per size.

        Args:
            output_summary_file (str): The name of the summary runtime information CSV file.

        Returns:
            None
        """
        try:
            file = os.path.join(self.dir, 'results', output_summary_file)
            if not os.path.exists(file):
                return

            df = pd.read_csv(file)

            # Calculate the minimum average per size
            min_avg_df = df.groupby('Size')['Average'].min().reset_index()
            min_avg_df.columns = ['Size', 'Minimum Average']

            # Merge the minimum average DataFrame with the original DataFrame
            merged_df = pd.merge(df, min_avg_df, on='Size', how='left')

            # Calculate the percentage difference with respect to the minimum average per size
            merged_df['Percentage'] = 100 * ((merged_df['Average'] - merged_df['Minimum Average']) / merged_df['Minimum Average'] if (merged_df['Minimum Average'] != 0).any() else 0)

            # Save the updated result back to the CSV file
            merged_df.to_csv(file, index=False)
        except Exception as e:
            print(f"Error: {str(e)}")
