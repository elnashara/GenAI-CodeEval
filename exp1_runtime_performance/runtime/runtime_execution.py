import timeit
import traceback
import textwrap
import random

class Node:
    """
    A class representing a node in a linked list.

    Attributes:
        val (int): The value of the node.
        next (Node): A reference to the next node in the linked list.
    """
    def __init__(self, val):
        """
        Initializes the Node with a given value and sets the next node to None.

        Args:
            val (int): The value to be stored in the node.
        """
        self.val = val
        self.next = None

def create_linked_list(size):
    """
    Creates a linked list of the specified size with random integer values.

    Args:
        size (int): The number of nodes in the linked list.

    Returns:
        Node: The head node of the created linked list.
    """
    head = Node(random.randint(0, 1000000))
    current = head
    for i in range(size):
        current.next = Node(random.randint(0, 1000000))
        current = current.next

    return head

def create_linked_list_loop(size):
    """
    Creates a linked list with a loop. The loop is formed by connecting the last node
    to a random node within the list.

    Args:
        size (int): The number of nodes in the linked list.

    Returns:
        Node: The head node of the created linked list with a loop.
    """
    head = Node(random.randint(0, 1000000))
    current = head
    for i in range(size):
        current.next = Node(random.randint(0, 1000000))
        current = current.next

    # Create a loop in the linked list (connect the last node to a random node)
    last_node = current
    random_node = head
    for i in range(random.randint(1, 100)):
        random_node = random_node.next
    last_node.next = random_node  

    return head

class RuntimeExecution:
    """
    A class to handle the execution of dynamically defined code, measuring the runtime performance
    over multiple versions.

    Attributes:
        func_code (str): The string representation of the function to be executed.
        versions (int): The number of versions or iterations to run the function.
        _timeout_counter (int): A counter to track the number of times the function has timed out.

    Methods:
        get_timeout_counter(): Returns the timeout counter value.
        execute(size, *args): Executes the provided function, measuring its runtime with different inputs.
    """
    
    def __init__(self, func_code, versions):
        """
        Initializes the RuntimeExecution class with the provided function code and the number of versions.

        Args:
            func_code (str): The code of the function to be dynamically executed.
            versions (int): The number of times the function will be executed.
        """
        self.func_code = func_code
        self.versions = versions
        self._timeout_counter = 1

    def get_timeout_counter(self):
        """
        Returns the current value of the timeout counter.

        Returns:
            int: The number of times the function has timed out.
        """
        return self._timeout_counter
    
    def execute(self, size, *args):
        """
        Executes the dynamically defined function, measuring its runtime performance for the specified size.

        The function is executed multiple times based on the number of versions specified. The arguments
        can include structures such as linked lists, and the execution time is measured using the timeit module.

        Args:
            size (int): The size of the input data (e.g., the size of a linked list).
            *args (tuple): Additional arguments to pass to the function.

        Returns:
            tuple: A tuple containing a list of runtimes for each execution and an exception message if applicable.
        
        Raises:
            Exception: Any exception raised during the execution of the function will be logged and re-raised.
        """
        try:
            for arg in args[0]:
                if size == arg['size']:
                    arg1 = arg['arg1']
                    arg2 = arg['arg2']
                    break
            
            if arg1 == 'LinkedList':
                arg1 = create_linked_list(size)
            elif arg1 == 'LinkedListwithLoop':
                arg1 = create_linked_list_loop(size)
            
            dedented_code = textwrap.dedent(self.func_code)
            compiled_code = compile(dedented_code, "<string>", "exec")
            exec(compiled_code, globals())

            funcImp = globals().get("funcImp")
            if funcImp is None or not callable(funcImp):
                raise RuntimeError("funcImp function not found or not callable")

            time_list = []
            self._timeout_counter = 0
            for i in range(self.versions):
                time_res = timeit.timeit(lambda: funcImp(i) if arg1 == 'N/A' and arg2 == 'N/A' else funcImp(arg1) if arg2 == 'N/A' else funcImp(arg1, arg2), number=100)
                time_list.append(time_res)
                del time_res
                self._timeout_counter += 1

            return (time_list, "N/A")
        except Exception as e:
            traceback.print_exc()
            raise
