#!/usr/bin/env python3
"""
Python to C Code Translator
Main application file that provides both CLI and web interface options.
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from translator import PythonToCTranslator
from code_executor import CodeExecutor, PerformanceComparator

def main():
    """
    Main function to handle CLI and web interface.
    
    This function serves as the entry point for the application, providing both
    command-line interface and web interface options for Python to C translation.
    """
    
    # ============================================================================
    # ARGUMENT PARSER SETUP
    # ============================================================================
    # Configure command-line argument parser with all available options
    parser = argparse.ArgumentParser(
        description="Python to C Code Translator using OpenAI GPT-4o",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch web interface
  python main.py --web
  
  # Translate a Python file
  python main.py --file example.py
  
  # Translate Python code from command line
  python main.py --code "print('Hello, World!')"
  
  # Translate with explanation
  python main.py --code "def add(a, b): return a + b" --explanation
  
  # Translate and execute C code
  python main.py --code "print('Hello')" --execute
  
  # Compare performance
  python main.py --code "for i in range(1000000): pass" --compare
        """
    )
    
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Launch the Gradio web interface"
    )
    
    parser.add_argument(
        "--file", 
        type=str, 
        help="Path to Python file to translate"
    )
    
    parser.add_argument(
        "--code", 
        type=str, 
        help="Python code to translate (as string)"
    )
    
    parser.add_argument(
        "--explanation", 
        action="store_true", 
        help="Include detailed explanation of translation"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output file path for translated C code"
    )
    
    parser.add_argument(
        "--api-key", 
        type=str, 
        help="OpenAI API key (overrides environment variable)"
    )
    
    parser.add_argument(
        "--execute", 
        action="store_true", 
        help="Execute the translated C code"
    )
    
    parser.add_argument(
        "--compare", 
        action="store_true", 
        help="Compare performance between Python and C code"
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # ============================================================================
    # ENVIRONMENT SETUP AND VALIDATION
    # ============================================================================
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Get OpenAI API key from command line argument or environment variable
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    
    # Validate that API key is provided - exit if not found
    if not api_key:
        print("❌ Error: OpenAI API key not provided.")
        print("Please provide your API key using one of these methods:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Create a .env file with OPENAI_API_KEY=your_key")
        print("3. Use --api-key argument")
        sys.exit(1)
    
    try:
        # ============================================================================
        # INITIALIZE CORE COMPONENTS
        # ============================================================================
        # Initialize the main components needed for translation and execution
        translator = PythonToCTranslator(api_key=api_key)  # OpenAI GPT-4o translator
        executor = CodeExecutor(timeout=10)                # Code execution engine
        comparator = PerformanceComparator()              # Performance comparison tool
        
        # ============================================================================
        # WEB INTERFACE MODE
        # ============================================================================
        # Launch the Gradio web interface if --web flag is provided
        if args.web:
            print("🚀 Launching web interface...")
            from gradio_app import create_gradio_interface
            interface = create_gradio_interface()
            interface.launch(
                server_name="127.0.0.1",
                server_port=7860,
                share=False,
                show_error=True
            )
            
        # ============================================================================
        # FILE TRANSLATION MODE
        # ============================================================================
        # Translate Python code from a file if --file flag is provided
        elif args.file:
            # Validate that the input file exists
            if not os.path.exists(args.file):
                print(f"❌ Error: File '{args.file}' not found.")
                sys.exit(1)
            
            # Read Python code from the specified file
            with open(args.file, 'r', encoding='utf-8') as f:
                python_code = f.read()
            
            print(f"📝 Translating file: {args.file}")
            
            # Translate Python code to C with or without explanation
            if args.explanation:
                c_code, explanation = translator.translate_with_explanation(python_code)
                print("\n" + "="*50)
                print("TRANSLATED C CODE:")
                print("="*50)
                print(c_code)
                print("\n" + "="*50)
                print("EXPLANATION:")
                print("="*50)
                print(explanation)
            else:
                c_code = translator.translate(python_code)
                print("\n" + "="*50)
                print("TRANSLATED C CODE:")
                print("="*50)
                print(c_code)
            
            # ============================================================================
            # FILE OUTPUT AND EXECUTION OPTIONS
            # ============================================================================
            # Save translated C code to output file if specified
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(c_code)
                print(f"\n💾 C code saved to: {args.output}")
            
            # Execute the translated C code if --execute flag is provided
            if args.execute:
                print("\n" + "="*50)
                print("EXECUTING C CODE:")
                print("="*50)
                output, error, exec_time = executor.execute_c(c_code)
                if output:
                    print("Output:")
                    print(output)
                if error:
                    print("Errors:")
                    print(error)
                print(f"Execution time: {exec_time:.4f} seconds")
            
            # Compare performance between Python and C if --compare flag is provided
            if args.compare:
                print("\n" + "="*50)
                print("PERFORMANCE COMPARISON:")
                print("="*50)
                results = comparator.compare_execution(python_code, c_code)
                
                print("Python Execution:")
                print(f"  Output: {results['python']['output']}")
                if results['python']['error']:
                    print(f"  Error: {results['python']['error']}")
                print(f"  Time: {results['python']['time']:.4f}s")
                
                print("\nC Execution:")
                print(f"  Output: {results['c']['output']}")
                if results['c']['error']:
                    print(f"  Error: {results['c']['error']}")
                print(f"  Time: {results['c']['time']:.4f}s")
                
                if results['comparison']['both_successful']:
                    faster = results['comparison']['faster']
                    speedup = results['comparison']['speedup']
                    print(f"\n🏆 {faster} is faster by {speedup:.2f}x")
                else:
                    print("\n❌ Cannot compare - one or both codes failed")
            
        # ============================================================================
        # COMMAND-LINE CODE TRANSLATION MODE
        # ============================================================================
        # Translate Python code provided directly via command line if --code flag is used
        elif args.code:
            print("📝 Translating Python code...")
            
            # Translate with or without explanation based on --explanation flag
            if args.explanation:
                c_code, explanation = translator.translate_with_explanation(args.code)
                print("\n" + "="*50)
                print("TRANSLATED C CODE:")
                print("="*50)
                print(c_code)
                print("\n" + "="*50)
                print("EXPLANATION:")
                print("="*50)
                print(explanation)
            else:
                c_code = translator.translate(args.code)
                print("\n" + "="*50)
                print("TRANSLATED C CODE:")
                print("="*50)
                print(c_code)
            
            # ============================================================================
            # COMMAND-LINE OUTPUT AND EXECUTION OPTIONS
            # ============================================================================
            # Save translated C code to output file if specified
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(c_code)
                print(f"\n💾 C code saved to: {args.output}")
            
            # Execute the translated C code if --execute flag is provided
            if args.execute:
                print("\n" + "="*50)
                print("EXECUTING C CODE:")
                print("="*50)
                output, error, exec_time = executor.execute_c(c_code)
                if output:
                    print("Output:")
                    print(output)
                if error:
                    print("Errors:")
                    print(error)
                print(f"Execution time: {exec_time:.4f} seconds")
            
            # Compare performance between Python and C if --compare flag is provided
            if args.compare:
                print("\n" + "="*50)
                print("PERFORMANCE COMPARISON:")
                print("="*50)
                results = comparator.compare_execution(args.code, c_code)
                
                print("Python Execution:")
                print(f"  Output: {results['python']['output']}")
                if results['python']['error']:
                    print(f"  Error: {results['python']['error']}")
                print(f"  Time: {results['python']['time']:.4f}s")
                
                print("\nC Execution:")
                print(f"  Output: {results['c']['output']}")
                if results['c']['error']:
                    print(f"  Error: {results['c']['error']}")
                print(f"  Time: {results['c']['time']:.4f}s")
                
                if results['comparison']['both_successful']:
                    faster = results['comparison']['faster']
                    speedup = results['comparison']['speedup']
                    print(f"\n🏆 {faster} is faster by {speedup:.2f}x")
                else:
                    print("\n❌ Cannot compare - one or both codes failed")
            
        # ============================================================================
        # DEFAULT MODE - WEB INTERFACE LAUNCH
        # ============================================================================
        # If no specific arguments provided, launch web interface by default
        else:
            # No arguments provided, show help and launch web interface
            print("🐍➡️🐘 Python to C Code Translator")
            print("\nNo specific action provided. Launching web interface...")
            print("Use --help to see all available options.")
            print()
            
            from gradio_app import create_gradio_interface
            interface = create_gradio_interface()
            interface.launch(
                server_name="127.0.0.1",
                server_port=7860,
                share=False,
                show_error=True
            )
    
    # ============================================================================
    # ERROR HANDLING AND CLEANUP
    # ============================================================================
    # Handle keyboard interrupts and other exceptions gracefully
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()