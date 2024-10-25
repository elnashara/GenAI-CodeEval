from chatgpt_prompt import ChatGPTPrompt
from runtime_performance import RuntimePerformance
from write_runtime_summary_detailed_information import WriteRuntimeSummaryDetailedInformation
from problem_set import ProblemSet
from collections import OrderedDict
import os
import pathlib

class GPT4oCodeEvaluator:
    """
    A class to handle the evaluation of GPT-4o-generated code solutions, including runtime analysis
    and detailed performance summaries.

    Methods:
        main(): Processes the prompt file, retrieves code, and writes detailed runtime information.
        calculate_summary_percentage(): Calculates and writes runtime summary percentage.
        run(): Entry point for the class, orchestrating the evaluation process.
    """

    def __init__(self, problem_number, model='gpt_4o'):
        """
        Initializes the GPT4oCodeEvaluator with the problem number, model, and other necessary configurations.
        
        Args:
            problem_number (int): The number of the problem to process.
            model (str): The LLM model being evaluated (default is 'gpt_4o').
        """
        self.problem_number = problem_number
        self.model = model
        self.output_detailed = f"p{problem_number}_{model}_detailed_auto_execution_times.csv"
        self.output_summary = f"p{problem_number}_{model}_summary_auto_execution_times.csv"
        self.sizes = [1000, 10000, 100000]
        self.versions = 100
        self.timeout = 600  # 10 minutes
        self.dir = os.path.dirname(__file__)
        self.directory_path = pathlib.Path(self.dir).parent / 'code_generator' / 'data'
        self.prefix = f"{model}_p{problem_number}."
        self.suffix = ".csv"
        self.problem_set = ProblemSet(problem_number, self.sizes)
        problem_info = self.problem_set.handle_problem_number()
        self.problem = problem_info[0]['problem']
        self.function_param = problem_info[0]['function_parameters']
        self.prompt = ChatGPTPrompt(problem_number, self.prefix, self.suffix)
        self.runtimeperformance = RuntimePerformance(problem_number, self.function_param, self.sizes, self.versions, self.timeout)
        self.write = WriteRuntimeSummaryDetailedInformation(problem_number, self.problem, self.dir)

    def main(self):
        """
        The main function for processing prompt files, generating runtime performance data, and writing detailed runtime information.
        
        This function:
        1. Retrieves a file based on the prompt's directory path, prefix, and suffix.
        2. Parses the content from the CSV file and processes each prompt and its generated code.
        3. For valid Python code, it measures runtime performance using the `RuntimePerformance` class.
        4. Writes the results to a detailed output file.
        5. Handles cases where no valid Python code is present by generating empty runtime statistics with exceptions.

        Args:
            None

        Returns:
            None
        """
        file_path = self.prompt.get_file_path(self.directory_path)
        if file_path is None:
            return
        content_list = self.prompt.get_file_content(file_path)
        
        unique_prompts = OrderedDict.fromkeys(item['prompt_name'] for item in content_list)
        print(f"total_prompts {len(unique_prompts)}")
        
        for index, content in enumerate(content_list, start=1):
            p_result_list = []
            code_segment = self.prompt.get_code_segment(content['generated_code'])
            print(f'index: {index}, {content["prompt_name"]}, code_number: {content["code_number"]}')
            if code_segment != 'N/A' and "Syntax error" not in code_segment:
                p_result_list = self.runtimeperformance.get_runtime(content["prompt_name"], content["code_number"], code_segment)
            else:
                for size in self.sizes:
                    result = {
                        'prompt_name': content['prompt_name'],
                        'code_segment': content['generated_code'],
                        'code_index': content['code_number'],
                        'size': size,
                        'min_time': 0,
                        'avg_time': 0,
                        'max_time': 0,
                        'Exception': f'function_index: {content["prompt_name"]}, code_start_index: -1, No Python code available'
                    }
                    p_result_list.append(result)
            
            self.write.write_runtime_detailed_information(p_result_list, self.output_detailed)

    def calculate_summary_percentage(self):
        """
        Calculates and writes the summary percentage of runtime information.

        This function:
        1. Writes a summary of runtime information from the detailed data.
        2. Calculates the percentage performance of the code solutions.
        
        Args:
            None

        Returns:
            None
        """
        self.write.write_runtime_summary_information(self.output_detailed, self.output_summary)
        self.write.calc_percentage(self.output_summary)

    def run(self):
        """
        The main entry point for running the GPT-4o code evaluation.

        This method:
        1. Calls the `main` function to process and evaluate the problem set.
        2. Calls `calculate_summary_percentage` to summarize the evaluation results.

        Args:
            None

        Returns:
            None
        """
        print(f'problem_number: {self.problem_number}')
        self.main()
        self.calculate_summary_percentage()


if __name__ == '__main__':
    """
    The entry point of the program.
    
    For each problem number (from 1 to 15), this script:
    1. Configures various parameters such as problem size, model, timeout, and output file paths.
    2. Initializes the GPT4oCodeEvaluator class and runs the evaluation process for each problem.
    
    Args:
        None

    Returns:
        None
    """
    for problem_number in range(1, 16):
        evaluator = GPT4oCodeEvaluator(problem_number)
        evaluator.run()
