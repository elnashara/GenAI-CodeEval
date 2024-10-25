import os
import csv

# Define the function to detect cycles in a directed graph
def funcImp(graph):
    def dfs(node):
        if visited[node] == 1:
            return True
        if visited[node] == 2:
            return False
        
        visited[node] = 1
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        
        visited[node] = 2
        return False
    
    visited = {node: 0 for node in graph}
    
    for node in graph:
        if visited[node] == 0:
            if dfs(node):
                return True
    
    return False

# Test cases
test_cases = [
    {
        "graph": {'A': ['B'], 'B': ['C'], 'C': []},
        "expected": False,
        "description": "Graph with no cycles (A -> B -> C)"
    },
    {
        "graph": {'A': ['B'], 'B': ['C'], 'C': ['A']},
        "expected": True,
        "description": "Graph with a simple cycle (A -> B -> C -> A)"
    },
    {
        "graph": {'D': ['E'], 'E': [], 'F': ['G'], 'G': ['H'], 'H': ['F']},
        "expected": True,
        "description": "Disconnected components with one having a cycle (D -> E; F -> G -> H -> F)"
    },
    {
        "graph": {},
        "expected": False,
        "description": "Empty graph"
    }
]

# Check if CSV file exists and prepare to write or append data
csv_file = '1_Prompt1_ChatGPT4o_NaiveApproach.csv'
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers only if the file does not exist yet
    if not file_exists:
        writer.writerow(['problem_number', 'index', 'category', 'problem_type', 'problem', 
                         'solution_prompt', 'solution', 
                         'test_input', 'expected', 
                         'actual', 'status', 
                         'pass', 'exception'])
    
    # Execute each test case and log results
    for index, test_case in enumerate(test_cases):
        
        problem_description = (
            f"Determine if a directed graph contains a cycle using DFS. "
            f"Test case: {test_case['description']}"
        )
        
        solution_prompt = (
            f"Implement `funcImp` to detect cycles in directed graphs."
            f" Use DFS approach."
        )
        
        solution_code = (
            """def funcImp(graph):\n"""
            """... (function code omitted for brevity) ...\n"""
            """# Test cases\n"""
            """... (test cases omitted for brevity) ...\n"""
         )
    
        # Prepare input and expected output details
        test_input_str = str(test_case["graph"])
        expected_output = test_case["expected"]
        
        try:
            actual_output = funcImp(test_case["graph"])
            status = actual_output == expected_output
            exception_info = ""
        except Exception as e:
            actual_output = None
            status = False
            exception_info = str(e)
        
        # Log data into CSV format row by row.
        writer.writerow([
            50,
            index + 1,
            'hard',  # category placeholder
            'Depth-First Search (DFS)',  # problem_type placeholder
            'Determining if a directed graph contains a cycle using DFS.',
            '',
            '',
            test_input_str,
            expected_output,
            actual_output,
            ('PASS' if status else 'FAIL'),
            status,
            exception_info
        ])