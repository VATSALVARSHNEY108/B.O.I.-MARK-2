"""
Code Templates for Common Programming Problems
Provides instant code generation without API calls
"""

PYTHON_TEMPLATES = {
    "palindrome": '''def is_palindrome(text):
    """
    Check if a given string is a palindrome.
    
    A palindrome is a word, phrase, number, or other sequence of characters
    which reads the same backward as forward, ignoring spaces, punctuation,
    and capitalization.
    
    Args:
        text: The string to check.
    
    Returns:
        True if the string is a palindrome, False otherwise.
    """
    # Remove spaces and convert to lowercase for comparison
    processed_text = ''.join(char.lower() for char in text if char.isalnum())
    
    # Compare the processed text with its reverse
    return processed_text == processed_text[::-1]


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"'madam' is a palindrome: {is_palindrome('madam')}")  # Expected: True
    print(f"'A man, a plan, a canal: Panama' is a palindrome: {is_palindrome('A man, a plan, a canal: Panama')}")  # Expected: True
    print(f"'racecar' is a palindrome: {is_palindrome('racecar')}")  # Expected: True
    print(f"'hello' is a palindrome: {is_palindrome('hello')}")  # Expected: False
    print(f"'12321' is a palindrome: {is_palindrome('12321')}")  # Expected: True
''',

    "reverse_number": '''def reverse_number(num):
    """
    Reverse the digits of a number.
    
    Args:
        num: The number to reverse (can be positive or negative).
    
    Returns:
        The number with its digits reversed.
    """
    # Handle negative numbers
    is_negative = num < 0
    num = abs(num)
    
    # Reverse the number
    reversed_num = 0
    while num > 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num = num // 10
    
    # Apply the sign back
    return -reversed_num if is_negative else reversed_num


def reverse_number_string_method(num):
    """
    Alternative method: Reverse number using string manipulation.
    
    Args:
        num: The number to reverse.
    
    Returns:
        The reversed number.
    """
    # Convert to string, reverse, and convert back to integer
    is_negative = num < 0
    num_str = str(abs(num))
    reversed_str = num_str[::-1]
    reversed_num = int(reversed_str)
    
    return -reversed_num if is_negative else reversed_num


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"Reverse of 12345: {reverse_number(12345)}")  # Expected: 54321
    print(f"Reverse of -9876: {reverse_number(-9876)}")  # Expected: -6789
    print(f"Reverse of 100: {reverse_number(100)}")  # Expected: 1
    print(f"Reverse of 7: {reverse_number(7)}")  # Expected: 7
    
    # Using string method
    print(f"\\nUsing string method:")
    print(f"Reverse of 12345: {reverse_number_string_method(12345)}")  # Expected: 54321
''',

    "fibonacci": '''def fibonacci(n):
    """
    Generate Fibonacci sequence up to n terms.
    
    The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    Each number is the sum of the two preceding ones.
    
    Args:
        n: Number of terms to generate.
    
    Returns:
        List containing the Fibonacci sequence.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    # Initialize the sequence
    fib_sequence = [0, 1]
    
    # Generate remaining terms
    for i in range(2, n):
        next_term = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_term)
    
    return fib_sequence


def fibonacci_recursive(n):
    """
    Calculate nth Fibonacci number using recursion.
    Note: This is less efficient for large n.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed).
    
    Returns:
        The nth Fibonacci number.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


# Example usage
if __name__ == "__main__":
    # Generate sequence
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
    print(f"First 15 Fibonacci numbers: {fibonacci(15)}")
    
    # Individual terms
    print(f"\\n5th Fibonacci number: {fibonacci_recursive(5)}")
    print(f"10th Fibonacci number: {fibonacci_recursive(10)}")
''',

    "factorial": '''def factorial(n):
    """
    Calculate the factorial of a number.
    Factorial of n (n!) = n × (n-1) × (n-2) × ... × 1
    
    Args:
        n: Non-negative integer.
    
    Returns:
        The factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def factorial_recursive(n):
    """
    Calculate factorial using recursion.
    
    Args:
        n: Non-negative integer.
    
    Returns:
        The factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    
    return n * factorial_recursive(n - 1)


# Example usage
if __name__ == "__main__":
    # Test cases
    print(f"Factorial of 5: {factorial(5)}")  # Expected: 120
    print(f"Factorial of 7: {factorial(7)}")  # Expected: 5040
    print(f"Factorial of 0: {factorial(0)}")  # Expected: 1
    
    # Using recursive method
    print(f"\\nUsing recursion:")
    print(f"Factorial of 6: {factorial_recursive(6)}")  # Expected: 720
''',

    "prime": '''def is_prime(n):
    """
    Check if a number is prime.
    
    A prime number is a natural number greater than 1 that has no
    positive divisors other than 1 and itself.
    
    Args:
        n: The number to check.
    
    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    
    return True


def get_primes_up_to(limit):
    """
    Find all prime numbers up to a given limit using Sieve of Eratosthenes.
    
    Args:
        limit: Upper limit for finding primes.
    
    Returns:
        List of all prime numbers up to limit.
    """
    if limit < 2:
        return []
    
    # Create a boolean array and initialize all entries as true
    is_prime_array = [True] * (limit + 1)
    is_prime_array[0] = is_prime_array[1] = False
    
    # Sieve of Eratosthenes
    p = 2
    while p * p <= limit:
        if is_prime_array[p]:
            # Mark all multiples of p as not prime
            for i in range(p * p, limit + 1, p):
                is_prime_array[i] = False
        p += 1
    
    # Collect all prime numbers
    return [num for num in range(limit + 1) if is_prime_array[num]]


# Example usage
if __name__ == "__main__":
    # Test individual numbers
    print(f"Is 17 prime? {is_prime(17)}")  # Expected: True
    print(f"Is 25 prime? {is_prime(25)}")  # Expected: False
    print(f"Is 2 prime? {is_prime(2)}")  # Expected: True
    
    # Get all primes up to 50
    print(f"\\nPrime numbers up to 50: {get_primes_up_to(50)}")
''',

    "bubble_sort": '''def bubble_sort(arr):
    """
    Sort an array using the bubble sort algorithm.
    
    Bubble sort repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order.
    
    Args:
        arr: List of comparable elements to sort.
    
    Returns:
        The sorted list.
    """
    # Create a copy to avoid modifying the original
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize: stop if no swaps occur
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element is greater than the next element
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        # If no swapping occurred, array is already sorted
        if not swapped:
            break
    
    return arr_copy


# Example usage
if __name__ == "__main__":
    # Test cases
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_array}")
    print(f"Sorted array: {bubble_sort(test_array)}")
    
    # Test with already sorted array
    sorted_array = [1, 2, 3, 4, 5]
    print(f"\\nAlready sorted: {sorted_array}")
    print(f"After sorting: {bubble_sort(sorted_array)}")
    
    # Test with reverse sorted array
    reverse_array = [9, 7, 5, 3, 1]
    print(f"\\nReverse sorted: {reverse_array}")
    print(f"After sorting: {bubble_sort(reverse_array)}")
''',

    "binary_search": '''def binary_search(arr, target):
    """
    Search for a target value in a sorted array using binary search.
    
    Binary search works by repeatedly dividing the search interval in half.
    Time complexity: O(log n)
    
    Args:
        arr: Sorted list of comparable elements.
        target: The value to search for.
    
    Returns:
        Index of target if found, -1 otherwise.
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # Calculate middle index
        mid = (left + right) // 2
        
        # Check if target is at mid
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target not found
    return -1


def binary_search_recursive(arr, target, left=0, right=None):
    """
    Recursive implementation of binary search.
    
    Args:
        arr: Sorted list of comparable elements.
        target: The value to search for.
        left: Left boundary of search range.
        right: Right boundary of search range.
    
    Returns:
        Index of target if found, -1 otherwise.
    """
    if right is None:
        right = len(arr) - 1
    
    # Base case: element not found
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    # Target found
    if arr[mid] == target:
        return mid
    
    # Search left half
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)
    
    # Search right half
    else:
        return binary_search_recursive(arr, target, mid + 1, right)


# Example usage
if __name__ == "__main__":
    # Test array (must be sorted!)
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
    
    # Test cases
    print(f"Array: {sorted_array}")
    print(f"Search for 23: Index {binary_search(sorted_array, 23)}")  # Expected: 5
    print(f"Search for 56: Index {binary_search(sorted_array, 56)}")  # Expected: 8
    print(f"Search for 100: Index {binary_search(sorted_array, 100)}")  # Expected: -1
    
    # Using recursive method
    print(f"\\nUsing recursion:")
    print(f"Search for 12: Index {binary_search_recursive(sorted_array, 12)}")  # Expected: 3
'''
}


def get_template_code(problem_keywords, language="python"):
    """
    Get template code for common programming problems.
    
    Args:
        problem_keywords: Description or keywords of the problem.
        language: Programming language (currently only Python supported).
    
    Returns:
        Template code if available, None otherwise.
    """
    if language.lower() != "python":
        return None
    
    keywords_lower = problem_keywords.lower()
    
    # Match problem to template
    if "palindrome" in keywords_lower:
        return PYTHON_TEMPLATES["palindrome"]
    
    elif "reverse" in keywords_lower and "number" in keywords_lower:
        return PYTHON_TEMPLATES["reverse_number"]
    
    elif "fibonacci" in keywords_lower or "fib" in keywords_lower:
        return PYTHON_TEMPLATES["fibonacci"]
    
    elif "factorial" in keywords_lower:
        return PYTHON_TEMPLATES["factorial"]
    
    elif "prime" in keywords_lower:
        return PYTHON_TEMPLATES["prime"]
    
    elif "bubble" in keywords_lower and "sort" in keywords_lower:
        return PYTHON_TEMPLATES["bubble_sort"]
    
    elif "binary" in keywords_lower and "search" in keywords_lower:
        return PYTHON_TEMPLATES["binary_search"]
    
    return None


def list_available_templates():
    """
    List all available code templates.
    
    Returns:
        List of available template names.
    """
    return list(PYTHON_TEMPLATES.keys())
