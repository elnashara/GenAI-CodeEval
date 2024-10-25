# Import the generate_code function from ai_coder
from ai_coder import generate_code
import os
import pathlib
import configparser
import re
import csv

class CodeGenerator:
    """
    A class for automating the process of generating Python code using prompts.
    
    Attributes:
        PROMPT_ENSEMBLE (int): A constant representing the starting prompt number for ensemble generation.
        problem_number (int): The number of the current problem being worked on.
        prompt_properties (dict): A dictionary containing prompts and their values.
        filename (str): The name of the file to write generated code to.
        org_problem_name (str): The original problem name for contextual prompt generation.
        org_problem_value (str): The original problem value for contextual prompt generation.
    """
    
    PROMPT_ENSEMBLE = 7

    def __init__(self, problem_number, prompt_properties, filename, org_problem_name, org_problem_value):
        """
        Initializes the CodeGenerator object.
        
        Args:
            problem_number (int): The current problem number.
            prompt_properties (dict): Dictionary containing prompt names and values.
            filename (str): The file name to write generated code into.
            org_problem_name (str): The original problem name for customizing prompts.
            org_problem_value (str): The original problem value for customizing prompts.
        """
        self.problem_number = problem_number
        self.prompt_properties = prompt_properties
        self.filename = filename
        self.org_problem_name = org_problem_name
        self.org_problem_value = org_problem_value

    def generate_python_code(self, api_key):
        """
        Generates Python code for the given problem by iterating through prompts.
        
        Args:
            api_key (str): API key for the code generation service.
        """
        for prompt_number, (prompt_name, prompt_value) in enumerate(self.prompt_properties.items(), start=1):
            if prompt_name != "prompt_1":
                continue
            
            prompt_value = self.get_prompt_value(prompt_value)
            for code_number in range(1, 101):
                if code_number <=99:
                    continue
                
                try:
                    # Call the generate_code function
                    generated_code = generate_code([], [prompt_value], api_key, checkfn=compile, max_tries=10, temperature=0)
                    self.write_to_file(prompt_name, code_number, prompt_value, generated_code, 'N/A')
                except Exception as e:
                    self.write_to_file(prompt_name, code_number, prompt_value, generated_code, f'Error: {str(e)}')
                    print(f"Problem {self.problem_number} - Prompt {prompt_number}: Error: {str(e)}")
                    continue

    def generate_ensemble_python_code(self, api_key):
        """
        Generates ensemble Python code by skipping the first prompt and working with subsequent prompts.
        
        Args:
            api_key (str): API key for the code generation service.
        """
        prompt_number = self.PROMPT_ENSEMBLE
        iterator = iter(self.prompt_properties.items())
        next(iterator)  # Skip the first prompt

        for index, (prompt_name, prompt_value) in enumerate(iterator, start=2):
            prompt_value = self.get_prompt_value(prompt_value)
            for code_number in range(1, 21):
                try:
                    # Call the generate_code function
                    generated_code = generate_code([], [prompt_value], api_key, checkfn=compile, max_tries=10, temperature=0)
                    self.write_to_file(f'prompt_{prompt_number}', code_number, prompt_value, generated_code, 'N/A')
                except Exception as e:
                    self.write_to_file(f'prompt_{prompt_number}', code_number, prompt_value, generated_code, f'Error: {str(e)}')
                    print(f"Problem {self.problem_number} - Prompt {prompt_number}: Error: {str(e)}")
                    continue

    def write_to_file(self, prompt_name, code_number, prompt_value, generated_code, exception):
        """
        Writes generated code and any exceptions to a CSV file.
        
        Args:
            prompt_name (str): Name of the prompt being processed.
            code_number (int): Iteration number for the generated code.
            prompt_value (str): The prompt value used for generating code.
            generated_code (str): The generated Python code.
            exception (str): Any exception that occurred during code generation.
        """
        file_mode = "w" if not os.path.isfile(self.filename) else "a"
        
        with open(self.filename, mode=file_mode, newline='') as file:
            writer = csv.writer(file)
            if file_mode == "w":
                writer.writerow(['problem_number', 'prompt_name', 'code_number', 'prompt_value', 'generated_code', 'Exception'])
            writer.writerow([self.problem_number, prompt_name, code_number, prompt_value, generated_code, exception])

    def get_prompt_value(self, prompt_value):
        """
        Replaces placeholders in the prompt value with context-specific information.
        
        Args:
            prompt_value (str): The original prompt value containing placeholders.
        
        Returns:
            str: The modified prompt value with placeholders replaced.
        """
        function_description = ''
        if '_arr_' in self.org_problem_name:
            function_description = config['FUNCTION_DESCRIPTION']['func_desc_arr']
            function_argument = config['FUNCTION_ARGUMENT']['func_one_arg_arr'] if '_one_' in self.org_problem_name else config['FUNCTION_ARGUMENT']['func_two_arg_arr']
            function_description = function_description.replace('<FUNCTION_ARGUMENT>', function_argument)
        elif '_lnk_' in self.org_problem_name:
            function_description = config['FUNCTION_DESCRIPTION']['func_desc_lnk']
        elif '_pascal_' in self.org_problem_name:
            function_description = config['FUNCTION_DESCRIPTION']['func_desc_pascal']

        return prompt_value.replace('<ORIGINAL_PROMPT>', self.org_problem_value).replace('<FUNCTION_DESCRIPTION>', function_description).replace("'", "")

def clean_string(text):
    """
    Cleans a string by removing special characters, underscores, single quotes, and extra spaces.
    
    Args:
        text (str): The input string.
    
    Returns:
        str: The cleaned string.
    """
    text = re.sub('[^a-zA-Z0-9\s]+', ' ', text)
    text = text.lower().replace('_', '').replace("'", '')
    return re.sub('\s+', '', text).strip()

def main(config, api_key, data_dir):
    """
    Main function that processes problems and generates code for each one.
    
    Args:
        config (ConfigParser): Configuration settings from the config.ini file.
        api_key (str): API key for the code generation service.
        data_dir (Path): Directory where the generated files will be stored.
    """
    original_problem_properties = config['ORIGINAL_PROBLEM']
    prompt_properties = config['PROMPT']

    for problem_number, (org_problem_name, org_problem_value) in enumerate(original_problem_properties.items(), start=1):
        try:
            if problem_number != 7:
                continue
                       
            build_file_name = f"p{problem_number}.{clean_string(org_problem_value)}.csv"
            print(build_file_name)

            file_name = os.path.join(data_dir, build_file_name)
            code_generator = CodeGenerator(problem_number, prompt_properties, file_name, org_problem_name, org_problem_value)
            code_generator.generate_python_code(api_key)
            # code_generator.generate_ensemble_python_code()
        except Exception as e:
            print(f"\t\t ++++++ Error: {str(e)}")
            continue

def get_configuration():
    """
    Loads the configuration settings and API key from the local environment.
    
    Returns:
        tuple: A tuple containing the config object, API key, and data directory path.
    """
    dir = os.path.dirname(__file__)
    
    with open(os.path.join(dir, "api_key"), "r") as f:
        api_key = f.read().strip()
    data_dir = pathlib.Path(dir, 'data')
    config = configparser.ConfigParser()
    config.read(os.path.join(dir, "config.ini"))
    
    return config, api_key, data_dir

if __name__ == '__main__':
    config, api_key, data_dir = get_configuration()
    main(config, api_key, data_dir)
