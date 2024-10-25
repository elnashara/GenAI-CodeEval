from runtime_execution import RuntimeExecution
import multiprocessing as mp
import statistics

class RuntimePerformance:
    """
    A class to handle the runtime performance measurement of dynamically executed code.

    Attributes:
        problem_number (int): The number representing the problem being evaluated.
        function_param (list): The parameters used by the function being evaluated.
        sizes (list): A list of sizes for the input data to test the function with.
        versions (int): The number of times the function will be executed to measure performance.
        timeout (int): The maximum time (in seconds) to wait for a function to complete execution.

    Methods:
        get_runtime(prompt_name, code_index, func_code): Executes the provided function with different input sizes
        and collects runtime performance metrics such as minimum, average, and maximum execution times.
    """

    def __init__(self, problem_number, function_param, sizes, versions, timeout):
        """
        Initializes the RuntimePerformance class with the provided problem number, function parameters, sizes, 
        number of versions, and timeout.

        Args:
            problem_number (int): The number of the problem being evaluated.
            function_param (list): The function parameters.
            sizes (list): The sizes of input data to test with.
            versions (int): The number of times the function will be executed.
            timeout (int): The maximum allowable time (in seconds) for function execution.
        """
        self.problem_number = problem_number
        self.function_param = function_param
        self.sizes = sizes
        self.versions = versions
        self.timeout = timeout

    def get_runtime(self, prompt_name, code_index, func_code):
        """
        Executes the provided function (func_code) for different input sizes, measuring runtime performance
        such as minimum, average, and maximum times.

        Args:
            prompt_name (str): The name of the prompt or test being executed.
            code_index (int): The index of the code being executed.
            func_code (str): The function code to be executed as a string.

        Returns:
            list[dict]: A list of dictionaries containing runtime performance results for each input size, including:
            - 'prompt_name': The name of the prompt.
            - 'code_segment': The code being executed.
            - 'code_index': The index of the code.
            - 'size': The input size for the function.
            - 'min_time': The minimum runtime.
            - 'avg_time': The average runtime.
            - 'max_time': The maximum runtime.
            - 'Exception': Any exceptions encountered during execution.

        Raises:
            Exception: Any exception raised during function execution will be handled and recorded.
        """
        execution = RuntimeExecution(func_code, self.versions)
        
        p_result_list = []
        exception = 'N/A'

        for size in self.sizes:
            pool = mp.Pool(processes=1)  # Create a multiprocessing pool with 1 process
            lock = mp.Lock()  # Create a lock for synchronization
            print(f"\tTesting for list size {size}")
            time_list = []
            if exception == 'N/A':
                lock.acquire()  # Acquire the lock before running get_runtime
                async_result = pool.apply_async(execution.execute, args=(size, self.function_param,))  # Run get_runtime asynchronously
                try:
                    time_list, exception = async_result.get(timeout=self.timeout)  # Get the result within timeout seconds
                except mp.TimeoutError:
                    exception = f"\t runtime.get_runtime terminated after {self.timeout} seconds"
                    timeout_counter = execution.get_timeout_counter()
                    print(f'timeout:{self.timeout}, timeout_counter: {timeout_counter}, exception: {exception}')
                    pool.terminate()  # Terminate the pool
                    time_list.append(self.timeout/timeout_counter)
                except Exception as e:
                    exception = f"\t exception: {e}"
                    print(exception)
                    pool.terminate()  # Terminate the pool
                    time_list.append(0)
                lock.release()  # Release the lock after funcA completes
            elif 'runtime.get_runtime' in exception:
                timeout_counter = execution.get_timeout_counter()
                print(f'timeout:{self.timeout}, timeout_counter: {timeout_counter}, exception: {exception}')
                time_list.append(self.timeout/timeout_counter)
            else:
                print(exception)
                time_list.append(0)
        
            min_time = min(time_list)
            avg_time = statistics.mean(time_list)
            max_time = max(time_list)
            
            pool.close()
            pool.join()
            result = {
                'prompt_name': prompt_name,
                'code_segment': str(func_code),
                'code_index': code_index,
                'size': size,
                'min_time': min_time,
                'avg_time': avg_time,
                'max_time': max_time,
                'Exception': exception
            }
            # print(f"\t\t\tResult: {result} ")
            p_result_list.append(result)
        del execution
        return p_result_list
