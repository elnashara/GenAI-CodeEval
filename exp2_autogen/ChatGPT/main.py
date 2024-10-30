import openai
import os
import pandas as pd

class GptTaskManager:
    def __init__(self, api_key, model, temperature=0, max_tokens=2048, top_p=0.8, frequency_penalty=0.5, presence_penalty=0.5):
        """
        Initialize GptTaskManager with the necessary OpenAI API parameters.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        openai.api_key = self.api_key
    
    def call_gpt_chat_api(self, prompt):
        """
        Call the OpenAI GPT API with the given prompt.
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty
        )
        return response['choices'][0]['message']['content'].strip()
    
    def generate_solution_prompt(self, problem):
        """
        Generate the solution prompt for the GPT-4o API.
        """
        solution_prompt = f"""
## Problem Statement
- Develop a Python script to solve the problem: '{problem}'

## Solution Development
- Create a Python function named 'funcImp' that implements the solution.
- Ensure that the function is defined at the beginning of your script and is accessible throughout the script.

## Script Requirements
- The script should define the 'funcImp' function at the root level, not inside any class or other function.
- Include comments in the script to explain the logic and functionality of the 'funcImp' function.
- Test the function within the script to ensure it's correctly defined and functioning as expected.

## Test Case Execution
- Execute the 'funcImp' function with various test cases to verify its correctness.
- Ensure that the function 'funcImp' is defined and accessible in the scope where the test cases are executed.

## Test Case Preparation
- Prepare a set of test cases, including edge cases, to thoroughly test the function.
- Test cases should cover different types of input strings, such as alphabetic, numeric, special characters, and empty strings.

## Execution Process
- Run each test case through the 'funcImp' function.
- Capture the output of each test case to compare it with the expected result."""
        return solution_prompt

    def generate_solution(self, problem):
        """
        Generate a solution using the GPT-4o API for the given problem.
        """
        solution_prompt = self.generate_solution_prompt(problem)
        print(solution_prompt)
        
        solution = self.call_gpt_chat_api(solution_prompt)
        return solution

    def generate_test_results_logging_prompt(self, solution_python, file_name):
        """
        Generate the test results logging prompt for the GPT-4o API.
        """
        TestResultsLoggingPrompt = f"""
        ## Importing Necessary Modules
        - Before logging the test cases, make sure to import all necessary modules at the beginning of your script.
        - Specifically, import the 'os' module to check for file existence and handle file paths.

        ## Python Script to be Executed
        - The Python script to be used as part of developing the solution: {solution_python}

        ## Preparing the CSV File for Logging Test Cases
        - Check if '{file_name}' exists using the 'os' module.
          - If not, create it and write the headers: 'index, category, problem_type, problem, solution_prompt, solution, test_input, expected, actual, status, pass, exception'.
          - If it exists, prepare to append data without adding headers again.

        ## Executing and Logging Each Test Case
        - For each test case:
          1. Execute the test case using the provided Python script.
          2. Collect the following data:
             - problem: Detailed description of the problem.
             - solution_prompt: The prompt used to generate the solution.
             - solution: The Python script including the 'funcImp' function and test cases.
             - test_input: Input used in the test case.
             - expected: Expected output.
             - actual: Actual output produced by the function.
             - status: 'PASS' if actual output matches expected output, otherwise 'FAIL'.
             - pass: Boolean value, True if the test case passes, otherwise False.
             - exception: Any exceptions encountered during execution.
          3. Log the collected data to '{file_name}'.

        ## CSV File Writing
        - Use the 'csv' module to write the collected data into the CSV file.
        - Ensure each test case is logged individually and the file is updated correctly.
        - Manage file operations to avoid data loss or corruption.

        ## Note
        - This script will automate the process of executing test cases and logging their results in a structured CSV format.
        """
        return TestResultsLoggingPrompt

    def log_test_results(self, solution_python, file_name):
        """
        Generate the test results logging script using the GPT-4o API.
        """
        prompt = self.generate_test_results_logging_prompt(solution_python, file_name)
        result = self.call_gpt_chat_api(prompt)
        print(result)
        return result

if __name__ == "__main__":
    # GPT API Key and parameters
    dir = os.path.dirname(__file__)
    
    with open(os.path.join(dir, "api_key"), "r") as f:
        api_key = f.read().strip()

    file_name_problems = os.path.join(dir, 'data\\computer_science_problems.csv')
    file_name_result = os.path.join('1_Prompt1_ChatGPT4o_NaiveApproach.csv')

    model="gpt-4o"
    # Initialize GptTaskManager
    gpt_api = GptTaskManager(api_key, model)

    # Load the problems from the CSV
    df = pd.read_csv(file_name_problems)
    # Loop through each problem
    for index, row in df.iterrows():
        
        if index != 1 - 1:
            continue
        
        idx = row['seq']
        category = row['category']
        problem_type = ' '.join(row['problem_type'].split())
        problem = row['problem']
        
        print(f"Processing problem: {idx}")
        print(f"category: {category}")
        print(f"problem_type: {problem_type}")
        print(f"problem : {problem}")
    
        # Generate the solution for the problem
        solution_python = gpt_api.generate_solution(problem)
        print(f"Generated Solution:\n{solution_python}")

        # Log test results using the solution
        test_logging_script = gpt_api.log_test_results(solution_python, file_name_result)
        print(f"Generated Test Logging Script:\n{test_logging_script}")

        break
