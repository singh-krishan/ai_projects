"""
Code Execution Module

This module provides safe execution capabilities for both Python and C code.
It includes timeout protection, error handling, and performance comparison features.
The module ensures secure execution by using temporary files and proper cleanup.
"""

import subprocess
import tempfile
import os
import time
import sys
from typing import Tuple, Optional
import threading
import queue

class CodeExecutor:
    """
    A class to execute Python and C code safely with timeout and error handling.
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the code executor.
        
        Args:
            timeout: Maximum execution time in seconds
        """
        self.timeout = timeout
    
    def execute_python(self, python_code: str) -> Tuple[str, str, float]:
        """
        Execute Python code and return output, errors, and execution time.
        
        Args:
            python_code: The Python code to execute
            
        Returns:
            Tuple of (stdout, stderr, execution_time)
        """
        # Validate input - return error if no code provided
        if not python_code.strip():
            return "", "Error: No Python code provided.", 0.0
        
        try:
            # ============================================================================
            # TEMPORARY FILE CREATION AND CODE WRITING
            # ============================================================================
            # Create a temporary file for the Python code to ensure safe execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(python_code)
                temp_file = f.name
            
            # ============================================================================
            # PYTHON CODE EXECUTION
            # ============================================================================
            # Execute the Python code using subprocess with timeout protection
            start_time = time.time()
            
            result = subprocess.run(
                [sys.executable, temp_file],  # Use current Python interpreter
                capture_output=True,          # Capture stdout and stderr
                text=True,                    # Return strings instead of bytes
                timeout=self.timeout          # Apply timeout protection
            )
            
            execution_time = time.time() - start_time
            
            # ============================================================================
            # CLEANUP AND RETURN RESULTS
            # ============================================================================
            # Clean up the temporary file
            os.unlink(temp_file)
            
            return result.stdout, result.stderr, execution_time
            
        except subprocess.TimeoutExpired:
            # Handle timeout - clean up temporary file and return timeout error
            try:
                os.unlink(temp_file)
            except:
                pass
            return "", f"Error: Code execution timed out after {self.timeout} seconds.", 0.0
            
        except Exception as e:
            # Handle any other execution errors
            try:
                os.unlink(temp_file)
            except:
                pass
            return "", f"Error executing Python code: {str(e)}", 0.0
    
    def execute_c(self, c_code: str) -> Tuple[str, str, float]:
        """
        Compile and execute C code and return output, errors, and execution time.
        
        Args:
            c_code: The C code to compile and execute
            
        Returns:
            Tuple of (stdout, stderr, execution_time)
        """
        # Validate input - return error if no code provided
        if not c_code.strip():
            return "", "Error: No C code provided.", 0.0
        
        # Initialize variables for temporary files
        temp_c_file = None
        temp_exe_file = None
        
        try:
            # ============================================================================
            # TEMPORARY FILE CREATION AND CODE WRITING
            # ============================================================================
            # Create a temporary file for the C code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(c_code)
                temp_c_file = f.name
            
            # Create a temporary executable file name (replace .c with no extension)
            temp_exe_file = temp_c_file.replace('.c', '')
            
            # ============================================================================
            # C CODE COMPILATION
            # ============================================================================
            # Compile the C code using GCC compiler
            compile_result = subprocess.run(
                ['gcc', temp_c_file, '-o', temp_exe_file],  # GCC compilation command
                capture_output=True,                        # Capture compilation output
                text=True,                                  # Return strings instead of bytes
                timeout=self.timeout                        # Apply timeout protection
            )
            
            # Check if compilation was successful
            if compile_result.returncode != 0:
                return "", f"Compilation error:\n{compile_result.stderr}", 0.0
            
            # ============================================================================
            # C CODE EXECUTION
            # ============================================================================
            # Execute the compiled C program
            start_time = time.time()
            
            exec_result = subprocess.run(
                [temp_exe_file],        # Execute the compiled binary
                capture_output=True,    # Capture program output
                text=True,              # Return strings instead of bytes
                timeout=self.timeout    # Apply timeout protection
            )
            
            execution_time = time.time() - start_time
            
            return exec_result.stdout, exec_result.stderr, execution_time
            
        except subprocess.TimeoutExpired:
            # Handle timeout during compilation or execution
            return "", f"Error: Code execution timed out after {self.timeout} seconds.", 0.0
            
        except FileNotFoundError:
            # Handle case where GCC compiler is not installed
            return "", "Error: GCC compiler not found. Please install GCC to compile C code.", 0.0
            
        except Exception as e:
            # Handle any other compilation or execution errors
            return "", f"Error executing C code: {str(e)}", 0.0
            
        finally:
            # ============================================================================
            # CLEANUP TEMPORARY FILES
            # ============================================================================
            # Always clean up temporary files, regardless of success or failure
            try:
                if temp_c_file and os.path.exists(temp_c_file):
                    os.unlink(temp_c_file)
                if temp_exe_file and os.path.exists(temp_exe_file):
                    os.unlink(temp_exe_file)
            except:
                pass  # Ignore cleanup errors

class PerformanceComparator:
    """
    A class to compare performance between Python and C code execution.
    
    This class provides functionality to execute both Python and C versions of code
    and compare their execution times, providing detailed performance analysis.
    """
    
    def __init__(self):
        """Initialize the performance comparator with a code executor."""
        self.executor = CodeExecutor()
    
    def compare_execution(self, python_code: str, c_code: str) -> dict:
        """
        Compare execution performance between Python and C code.
        
        Args:
            python_code: Python code to execute
            c_code: C code to execute
            
        Returns:
            Dictionary with comparison results including execution times and performance metrics
        """
        # ============================================================================
        # INITIALIZE RESULTS STRUCTURE
        # ============================================================================
        # Create a structured dictionary to store all comparison results
        results = {
            'python': {'output': '', 'error': '', 'time': 0.0, 'success': False},
            'c': {'output': '', 'error': '', 'time': 0.0, 'success': False},
            'comparison': {'faster': '', 'speedup': 0.0, 'both_successful': False}
        }
        
        # ============================================================================
        # PYTHON CODE EXECUTION
        # ============================================================================
        # Execute Python code and store results
        py_output, py_error, py_time = self.executor.execute_python(python_code)
        results['python']['output'] = py_output
        results['python']['error'] = py_error
        results['python']['time'] = py_time
        results['python']['success'] = not bool(py_error)  # Success if no errors
        
        # ============================================================================
        # C CODE EXECUTION
        # ============================================================================
        # Execute C code and store results
        c_output, c_error, c_time = self.executor.execute_c(c_code)
        results['c']['output'] = c_output
        results['c']['error'] = c_error
        results['c']['time'] = c_time
        results['c']['success'] = not bool(c_error)  # Success if no errors
        
        # ============================================================================
        # PERFORMANCE COMPARISON ANALYSIS
        # ============================================================================
        # Compare performance only if both codes executed successfully
        if results['python']['success'] and results['c']['success']:
            results['comparison']['both_successful'] = True
            
            # Calculate speedup ratio if both execution times are valid
            if py_time > 0 and c_time > 0:
                if py_time > c_time:
                    # C is faster
                    results['comparison']['faster'] = 'C'
                    results['comparison']['speedup'] = py_time / c_time
                else:
                    # Python is faster
                    results['comparison']['faster'] = 'Python'
                    results['comparison']['speedup'] = c_time / py_time
        
        return results