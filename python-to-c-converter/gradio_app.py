"""
Gradio Web Interface Module

This module provides a comprehensive web interface for the Python to C code translator.
It includes translation functionality, code execution capabilities, and performance
comparison features in an intuitive web-based interface.
"""

import gradio as gr
from translator import PythonToCTranslator
from code_executor import CodeExecutor, PerformanceComparator
import os
from dotenv import load_dotenv

def create_gradio_interface():
    """
    Create and configure the Gradio interface for Python to C translation.
    
    This function sets up the complete web interface including:
    - Translation functionality
    - Code execution capabilities  
    - Performance comparison features
    - Example code loading
    - Error handling and validation
    
    Returns:
        gr.Blocks: Configured Gradio interface
    """
    
    # ============================================================================
    # ENVIRONMENT SETUP AND COMPONENT INITIALIZATION
    # ============================================================================
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Initialize the core components needed for the application
    translator = PythonToCTranslator()  # OpenAI GPT-4o translator
    executor = CodeExecutor(timeout=10)  # Code execution engine with 10s timeout
    comparator = PerformanceComparator()  # Performance comparison tool
    
    # ============================================================================
    # CORE FUNCTION DEFINITIONS
    # ============================================================================
    
    def translate_code(python_code, include_explanation):
        """
        Translate Python code to C code.
        
        Args:
            python_code: The Python code to translate
            include_explanation: Whether to include detailed explanation
            
        Returns:
            Tuple of (c_code, explanation)
        """
        # Validate input - return error if no code provided
        if not python_code.strip():
            return "Please enter Python code to translate.", ""
        
        try:
            # Use appropriate translation method based on explanation flag
            if include_explanation:
                c_code, explanation = translator.translate_with_explanation(python_code)
                return c_code, explanation
            else:
                c_code = translator.translate(python_code)
                return c_code, ""
        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            return error_msg, ""
    
    def execute_python_code(python_code):
        """Execute Python code and return output, errors, and execution time."""
        # Validate input - return error if no code provided
        if not python_code.strip():
            return "No Python code provided.", "", 0.0
        
        # Execute Python code using the executor
        output, error, exec_time = executor.execute_python(python_code)
        return output, error, exec_time
    
    def execute_c_code(c_code):
        """Execute C code and return output, errors, and execution time."""
        # Validate input - return error if no code provided
        if not c_code.strip():
            return "No C code provided.", "", 0.0
        
        # Execute C code using the executor (includes compilation)
        output, error, exec_time = executor.execute_c(c_code)
        return output, error, exec_time
    
    def compare_performance(python_code, c_code):
        """
        Compare performance between Python and C code execution.
        
        Args:
            python_code: Python code to execute
            c_code: C code to execute
            
        Returns:
            Tuple containing execution results and comparison metrics
        """
        # Validate inputs - return error if either code is missing
        if not python_code.strip() or not c_code.strip():
            return "Please provide both Python and C code for comparison.", "", "", 0.0, 0.0, ""
        
        # Use the performance comparator to analyze both codes
        results = comparator.compare_execution(python_code, c_code)
        
        # ============================================================================
        # FORMAT COMPARISON RESULTS
        # ============================================================================
        # Create a formatted comparison text based on execution results
        comparison_text = ""
        if results['comparison']['both_successful']:
            faster = results['comparison']['faster']
            speedup = results['comparison']['speedup']
            comparison_text = f"Performance Comparison:\n"
            comparison_text += f"✅ Both codes executed successfully\n"
            comparison_text += f"🏆 {faster} is faster by {speedup:.2f}x\n"
            comparison_text += f"⏱️  Python: {results['python']['time']:.4f}s\n"
            comparison_text += f"⏱️  C: {results['c']['time']:.4f}s"
        else:
            comparison_text = "❌ Cannot compare performance - one or both codes failed to execute"
        
        # Return all results in the expected format for the UI
        return (
            results['python']['output'], 
            results['python']['error'],
            results['c']['output'],
            results['c']['error'],
            results['python']['time'],
            results['c']['time'],
            comparison_text
        )
    
    def clear_all():
        """Clear all text areas in the interface."""
        return "", "", "", "", "", "", "", "", "", "", ""
    
    # ============================================================================
    # GRADIO INTERFACE CREATION
    # ============================================================================
    # Create the main Gradio interface with custom styling and layout
    with gr.Blocks(
        title="Python to C Code Translator",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .code-textarea {
            font-family: 'Courier New', monospace !important;
        }
        """
    ) as interface:
        
        # ============================================================================
        # INTERFACE HEADER AND DESCRIPTION
        # ============================================================================
        # Display the main title and feature description
        gr.Markdown(
            """
            # 🐍➡️🐘 Python to C Code Translator & Performance Comparator
            
            Translate your Python code to equivalent C code using OpenAI's GPT-4o model and compare their performance!
            
            **Features:**
            - 🔄 **Translate**: Convert Python code to C code
            - ▶️ **Execute**: Run both Python and C code
            - 📊 **Compare**: Compare execution performance
            - 📚 **Examples**: Built-in example code
            
            **Instructions:**
            1. Enter your Python code in the text area below
            2. Click "Translate to C" to get the C equivalent
            3. Use "Run Python" and "Run C" to execute the codes
            4. Click "Compare Performance" to see execution time comparison
            
            **Note:** Make sure you have set your OpenAI API key and installed GCC compiler.
            """
        )
        
        # ============================================================================
        # TRANSLATION SECTION
        # ============================================================================
        # Main input/output area for Python to C translation
        with gr.Row():
            with gr.Column(scale=1):
                python_input = gr.Textbox(
                    label="Python Code",
                    placeholder="Enter your Python code here...",
                    lines=12,
                    elem_classes=["code-textarea"],
                    show_copy_button=True
                )
                
                with gr.Row():
                    include_explanation = gr.Checkbox(
                        label="Include Explanation",
                        value=False,
                        info="Get detailed explanation of the translation"
                    )
                    
                    translate_btn = gr.Button(
                        "Translate to C",
                        variant="primary",
                        size="lg"
                    )
            
            with gr.Column(scale=1):
                c_output = gr.Textbox(
                    label="Generated C Code",
                    lines=12,
                    elem_classes=["code-textarea"],
                    show_copy_button=True,
                    interactive=False
                )
                
                explanation_output = gr.Textbox(
                    label="Translation Explanation",
                    lines=6,
                    visible=False,
                    interactive=False
                )
        
        # Execution Section
        with gr.Row():
            with gr.Column():
                gr.Markdown("### ▶️ Code Execution")
                
                with gr.Row():
                    run_python_btn = gr.Button("Run Python", variant="secondary", size="lg")
                    run_c_btn = gr.Button("Run C", variant="secondary", size="lg")
                    compare_btn = gr.Button("Compare Performance", variant="primary", size="lg")
        
        # Output Section
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🐍 Python Execution Results")
                python_output = gr.Textbox(
                    label="Output",
                    lines=8,
                    elem_classes=["code-textarea"],
                    interactive=False
                )
                python_error = gr.Textbox(
                    label="Errors",
                    lines=4,
                    elem_classes=["code-textarea"],
                    interactive=False
                )
                python_time = gr.Textbox(
                    label="Execution Time",
                    lines=1,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 🐘 C Execution Results")
                c_exec_output = gr.Textbox(
                    label="Output",
                    lines=8,
                    elem_classes=["code-textarea"],
                    interactive=False
                )
                c_exec_error = gr.Textbox(
                    label="Errors",
                    lines=4,
                    elem_classes=["code-textarea"],
                    interactive=False
                )
                c_exec_time = gr.Textbox(
                    label="Execution Time",
                    lines=1,
                    interactive=False
                )
        
        # Performance Comparison
        with gr.Row():
            comparison_output = gr.Textbox(
                label="📊 Performance Comparison",
                lines=6,
                interactive=False,
                elem_classes=["code-textarea"]
            )
        
        # Control Buttons
        with gr.Row():
            clear_btn = gr.Button("Clear All", variant="secondary", size="lg")
        
        # Example section
        with gr.Accordion("📚 Examples", open=False):
            gr.Markdown(
                """
                **Example 1: Simple Function**
                ```python
                def add_numbers(a, b):
                    return a + b
                
                result = add_numbers(5, 3)
                print(f"Result: {result}")
                ```
                
                **Example 2: List Operations**
                ```python
                numbers = [1, 2, 3, 4, 5]
                squared = [x**2 for x in numbers]
                print(squared)
                ```
                
                **Example 3: Class Definition**
                ```python
                class Person:
                    def __init__(self, name, age):
                        self.name = name
                        self.age = age
                    
                    def greet(self):
                        return f"Hello, I'm {self.name}"
                ```
                """
            )
        
        # Event handlers
        translate_btn.click(
            fn=translate_code,
            inputs=[python_input, include_explanation],
            outputs=[c_output, explanation_output]
        )
        
        run_python_btn.click(
            fn=execute_python_code,
            inputs=[python_input],
            outputs=[python_output, python_error, python_time]
        )
        
        run_c_btn.click(
            fn=execute_c_code,
            inputs=[c_output],
            outputs=[c_exec_output, c_exec_error, c_exec_time]
        )
        
        compare_btn.click(
            fn=compare_performance,
            inputs=[python_input, c_output],
            outputs=[python_output, python_error, c_exec_output, c_exec_error, python_time, c_exec_time, comparison_output]
        )
        
        clear_btn.click(
            fn=clear_all,
            outputs=[python_input, c_output, explanation_output, python_output, python_error, python_time, c_exec_output, c_exec_error, c_exec_time, comparison_output]
        )
        
        # Show/hide explanation based on checkbox
        include_explanation.change(
            fn=lambda x: gr.update(visible=x),
            inputs=include_explanation,
            outputs=explanation_output
        )
        
        # Add some example buttons
        with gr.Row():
            example_btn1 = gr.Button("Load Example 1", size="sm")
            example_btn2 = gr.Button("Load Example 2", size="sm")
            example_btn3 = gr.Button("Load Example 3", size="sm")
        
        # Example handlers
        example_btn1.click(
            fn=lambda: "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(5, 3)\nprint(f\"Result: {result}\")",
            outputs=python_input
        )
        
        example_btn2.click(
            fn=lambda: "numbers = [1, 2, 3, 4, 5]\nsquared = [x**2 for x in numbers]\nprint(squared)",
            outputs=python_input
        )
        
        example_btn3.click(
            fn=lambda: "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def greet(self):\n        return f\"Hello, I'm {self.name}\"",
            outputs=python_input
        )
    
    return interface

if __name__ == "__main__":
    # Check if API key is available
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        print("You can create a .env file with: OPENAI_API_KEY=your_api_key_here")
    
    # Launch the interface
    interface = create_gradio_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )