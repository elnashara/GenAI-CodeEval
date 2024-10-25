import autogen
print(autogen.__file__)
print(autogen.__version__)

import sys
import io
import os
import pandas as pd

class AutoGenTaskManager:
    def __init__(self, api_key):
        self.OPENAI_API_KEY = api_key
        self.gpt_config_list = [
            {
                'model': 'gpt-4o', #'gpt-3.5-turbo',
                'api_key': self.OPENAI_API_KEY,
            }
        ]
        self.llm_config = {
            "request_timeout": 600,
            "seed": 42,
            "config_list": self.gpt_config_list,
            "temperature": 0
        }
        self.assistant = self._create_assistant_agent()
        self.user_proxy = self._create_user_proxy_agent()

    def _create_assistant_agent(self):
        return autogen.AssistantAgent(
            name="assistant",
            system_message="Solving and Testing Computer Science Problems with AutoGen",
            llm_config=self.llm_config,
            is_termination_msg=self.is_termination_msg,
        )

    def _create_user_proxy_agent(self):
        return autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=self.is_termination_msg,
            code_execution_config={
                "work_dir": "work_dir",
                "use_docker": False
            },
            llm_config=self.llm_config,
            system_message="""Reply TERMINATE if the task has been solved at full satisfaction, otherwise reply CONTINUE or explain why the task is not solved yet."""
        )

    @staticmethod
    def is_termination_msg(data):
        has_content = "content" in data and data["content"] is not None
        return has_content and "TERMINATE" in data["content"]

    def initiate_solution_generation(self, SolutionGenerationPrompt):
        
        self.user_proxy.initiate_chat(
            recipient=self.assistant,
            message=SolutionGenerationPrompt,
            clear_history=False
        )

    def initiate_test_logging(self, test_result_logging_prompt):
        self.user_proxy.initiate_chat(
            recipient=self.assistant,
            message=test_result_logging_prompt,
            clear_history=False
        )

    def capture_output(self, solution_prompt):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the solution prompt
        self.user_proxy.initiate_chat(
            recipient=self.assistant,
            message=solution_prompt,
            clear_history=False
        )

        sys.stdout = original_stdout
        output_string = captured_output.getvalue()
        return output_string

    @staticmethod
    def extract_last_python_code(text):
        start_delimiter = "---START---"
        end_delimiter = "---END---"

        start_index = text.rfind(start_delimiter)
        if start_index == -1:
            return None

        start_index += len(start_delimiter)
        end_index = text.find(end_delimiter, start_index)
        if end_index == -1:
            return None

        return text[start_index:end_index].strip()

    def generate_solution_prompt(self, problem):
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

    def generate_test_result_logging_prompt(self, file_name, problem_number, category, problem_type, problem, solution_prompt):
        TestResultsLoggingPrompt=f"""
## Importing Necessary Modules
- Before logging the test cases, make sure to import all necessary modules at the beginning of your script.
- Specifically, import the 'os' module to check for file existence and handle file paths.

## Logging Test Cases to a CSV File
- Log the results of each test case in a CSV file named '{file_name}'.

## CSV File Handling
- Use the 'os' module to check if 'Prompt1_NaiveApproach.csv' exists.
- If it does not exist, create the file and add the following headers in the first row:
    'problem_number, index, category, problem_type, problem, solution_prompt, solution, test_input, expected, actual, status, pass, exception'.
- If it exists, append the data without adding headers again.

## Individual Test Case Logging
For each test case, record the following in the CSV file:
- problem_number:{problem_number}
- index: An auto-incrementing number starting from zero.
- category: {category}
- problem_type: {problem_type}
- problem: {problem}
- solution_prompt: {solution_prompt}.
- solution: The actual Python script including the 'funcImp' function and test cases.
- test_input: The input used in each test case.
- expected: The expected output for each test case.
- actual: The actual output produced by the function for each test case.
- status: 'PASS' if the actual output matches the expected output, otherwise 'FAIL'.
- pass: True if the test case passes, otherwise False.
- exception: Log any exceptions encountered during execution.

## Note
- Ensure that each test case is logged individually.
- Update the CSV file accordingly, ensuring that headers are not repeated if the file already exists.
"""
        return TestResultsLoggingPrompt

if __name__ == "__main__":
    # GPT API Key and parameters
    dir = os.path.dirname(__file__)
    
    with open(os.path.join(dir, "api_key"), "r") as f:
        api_key = f.read().strip()

    manager = AutoGenTaskManager(api_key)

    file_name_problems = os.path.join(dir, 'data\\computer_science_problems.csv')
    file_name_result = '1_Prompt1_AutoGen_031_NaiveApproach.csv'

    # Load the problems from the CSV
    df = pd.read_csv(file_name_problems)
    # Loop through each problem
    for index, row in df.iterrows():
        
        if index != 51 - 1:
            continue
        
        problem_number = row['seq']
        category = row['category']
        problem_type = ' '.join(row['problem_type'].split())
        problem = row['problem']
        
        print(f"problem_number: {problem_number}")
        print(f"category: {category}")
        print(f"problem_type: {problem_type}")
        print(f"problem : {problem}")

        solution_prompt = manager.generate_solution_prompt(problem)
        print(f"solution_prompt\n{solution_prompt}")
        print("-------------------------------------------------")
        print("Initiating Solution Generation...")
        manager.initiate_solution_generation(solution_prompt)

        test_result_logging_prompt = manager.generate_test_result_logging_prompt(file_name_result,problem_number,category, problem_type, problem, solution_prompt)
        print(f"test_result_logging_prompt\n{test_result_logging_prompt}")
        print("-------------------------------------------------")
        print("Initiating Test Logging...")
        manager.initiate_test_logging(test_result_logging_prompt)
        
        print("Capturing Output...")
        output = manager.capture_output(solution_prompt)
        print("Output Captured:", output)

        extracted_code = manager.extract_last_python_code(output)
        print("Extracted Code:", extracted_code)
    
        break
