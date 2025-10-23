"""
Python to C Code Translator Module

This module provides the core translation functionality using OpenAI's GPT-4o model.
It handles the conversion of Python code to equivalent C code with proper error handling
and support for both simple translation and detailed explanations.
"""

import openai
import os
from dotenv import load_dotenv
from typing import Optional

class PythonToCTranslator:
    """
    A translator that converts Python code to C code using OpenAI's GPT-4o model.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the translator with OpenAI API key.
        
        Args:
            api_key: OpenAI API key. If None, will try to load from environment variables.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Initialize OpenAI client with provided API key or environment variable
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            self.client = openai.OpenAI(api_key=api_key)
    
    def translate(self, python_code: str) -> str:
        """
        Translate Python code to C code.
        
        Args:
            python_code: The Python code to translate
            
        Returns:
            The translated C code
            
        Raises:
            Exception: If translation fails
        """
        # Validate input - return error message if no code provided
        if not python_code.strip():
            return "Error: No Python code provided."
        
        try:
            # ============================================================================
            # OPENAI API CALL FOR TRANSLATION
            # ============================================================================
            # Create a chat completion request to GPT-4o with detailed system prompt
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert C programmer who specializes in translating Python code to C code. 
                        
                        Your task is to:
                        1. Analyze the provided Python code
                        2. Convert it to equivalent C code
                        3. Include necessary headers and libraries
                        4. Handle Python-specific features appropriately (e.g., dynamic typing, lists, dictionaries)
                        5. Ensure the C code is syntactically correct and compilable
                        6. Add comments explaining the translation when helpful
                        
                        Guidelines:
                        - Use appropriate C data types
                        - Handle memory management properly
                        - Convert Python lists to arrays or linked lists as appropriate
                        - Convert Python dictionaries to structs or hash tables
                        - Handle Python's dynamic typing with appropriate C types
                        - Include necessary #include statements
                        - Add a main() function if the Python code is a script
                        
                        Return only the C code without any additional explanations or markdown formatting."""
                    },
                    {
                        "role": "user",
                        "content": f"Translate this Python code to C:\n\n```python\n{python_code}\n```"
                    }
                ],
                temperature=0.1,  # Low temperature for consistent, deterministic output
                max_tokens=4000  # Sufficient tokens for most code translations
            )
            
            # ============================================================================
            # RESPONSE PROCESSING AND CLEANUP
            # ============================================================================
            # Extract the translated C code from the response
            content = response.choices[0].message.content.strip()
            
            # Clean markdown formatting if present (remove ```c and ``` markers)
            if content.startswith('```c'):
                content = content[4:]  # Remove ```c
            if content.startswith('```'):
                content = content[3:]   # Remove ```
            if content.endswith('```'):
                content = content[:-3]  # Remove trailing ```
            
            return content.strip()
            
        except Exception as e:
            return f"Error during translation: {str(e)}"
    
    def translate_with_explanation(self, python_code: str) -> tuple[str, str]:
        """
        Translate Python code to C code with explanation.
        
        Args:
            python_code: The Python code to translate
            
        Returns:
            A tuple containing (c_code, explanation)
        """
        # Validate input - return error message if no code provided
        if not python_code.strip():
            return "Error: No Python code provided.", ""
        
        try:
            # ============================================================================
            # OPENAI API CALL FOR TRANSLATION WITH EXPLANATION
            # ============================================================================
            # Create a chat completion request that includes detailed explanation
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert C programmer who specializes in translating Python code to C code. 
                        
                        Your task is to:
                        1. Analyze the provided Python code
                        2. Convert it to equivalent C code
                        3. Provide a detailed explanation of the translation process
                        
                        Return your response in the following format:
                        
                        C CODE:
                        [The translated C code here]
                        
                        EXPLANATION:
                        [Detailed explanation of the translation choices and C concepts used]"""
                    },
                    {
                        "role": "user",
                        "content": f"Translate this Python code to C with explanation:\n\n```python\n{python_code}\n```"
                    }
                ],
                temperature=0.1,  # Low temperature for consistent output
                max_tokens=4000  # Sufficient tokens for code and explanation
            )
            
            # ============================================================================
            # RESPONSE PARSING AND SEPARATION
            # ============================================================================
            # Extract the full response content
            content = response.choices[0].message.content.strip()
            
            # Parse the response to separate C code and explanation
            if "C CODE:" in content and "EXPLANATION:" in content:
                parts = content.split("EXPLANATION:")
                c_code = parts[0].replace("C CODE:", "").strip()
                explanation = parts[1].strip()
                return c_code, explanation
            else:
                # Fallback if format is not as expected
                return content, "Translation completed successfully."
                
        except Exception as e:
            return f"Error during translation: {str(e)}", ""