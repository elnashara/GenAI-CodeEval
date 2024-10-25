import os
import ast
import csv

class ChatGPTPrompt:
    """
    A class to handle ChatGPT prompt-related operations, such as retrieving file paths,
    reading file content, and extracting code segments.

    Attributes:
        problem_number (int): The number representing the problem.
        prefix (str): The prefix used for filtering files.
        suffix (str): The suffix used for filtering files.
    """

    def __init__(self, problem_number, prefix, suffix):
        """
        Initializes the ChatGPTPrompt class with the provided problem number, prefix, and suffix.

        Args:
            problem_number (int): The number representing the problem.
            prefix (str): The prefix used for filtering files.
            suffix (str): The suffix used for filtering files.
        """
        self.problem_number = problem_number
        self.prefix = prefix
        self.suffix = suffix

    def get_file_path(self, directory_path):
        """
        Retrieves the file path that matches the specified prefix and suffix within the given directory.

        Args:
            directory_path (str): The path of the directory to search for the file.

        Returns:
            str: The file path that matches the prefix and suffix, or None if no matching file is found.

        Example:
            directory_path = "/path/to/directory"
            file_path = get_file_path(directory_path)
        """
        print(directory_path)
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if filename.startswith(self.prefix) and filename.endswith(self.suffix):
                    print(f"filename: {filename}")
                    return file_path

    def get_file_content(self, file_path):
        """
        Reads the content of a CSV file and returns the list of dictionaries representing rows.

        Args:
            file_path (str): The path of the CSV file to read.

        Returns:
            list[dict]: A list of dictionaries containing the content of the file.
            Each dictionary represents a row from the CSV file with keys such as:
            'problem_number', 'prompt_name', 'code_number', 'prompt_value', 'generated_code', 'Exception'.

        Example:
            file_content = get_file_content("/path/to/file.csv")
        """
        file_content_list = []
        try:
            with open(file_path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    result = {
                        'problem_number': row['problem_number'],
                        'prompt_name': row['prompt_name'],
                        'code_number': row['code_number'],
                        'prompt_value': row['prompt_value'],
                        'generated_code': row['generated_code'],
                        'Exception': row['Exception']
                    }
                    file_content_list.append(result)
        except FileNotFoundError:
            print("File not found")
        except UnicodeDecodeError:
            print("Unable to decode the file with the specified encoding")

        return file_content_list

    def get_code_segment(self, generated_code):
        """
        Extracts and returns the Python code segment from the generated code string.
        
        Args:
            generated_code (str): The string containing the generated code, usually in Markdown with code blocks.

        Returns:
            str: The extracted and cleaned Python code segment, or an error message if there are issues with the syntax.

        Example:
            code_segment = get_code_segment(generated_code)
        """
        try:
            code_start_index = generated_code.replace("```python", "```Python").find("```Python")
            if code_start_index > 0: 
                code_end_index = generated_code.find("```", code_start_index + len("```Python"))
                code_string = generated_code[code_start_index + len("```Python"):code_end_index]
                code_string = code_string.strip().replace("\\n", "\n")
                code_string = code_string.encode().decode('unicode_escape')
                code_ast = ast.parse(code_string.replace("print(", "pass #print("), mode='exec')
                code_segment = ast.unparse(code_ast)

                return code_segment
            else:
                return 'N/A'
        except SyntaxError as e:
            error = f"Syntax error: {e}"
            print(error)
            return error
