# 🐍➡️🐘 Python to C Code Translator & Performance Comparator

A powerful tool that translates Python code to equivalent C code using OpenAI's GPT-4o model and compares their execution performance. Features both a web interface (Gradio) and command-line interface for maximum flexibility.

## ✨ Features

- **AI-Powered Translation**: Uses OpenAI's GPT-4o model for accurate Python-to-C conversion
- **Web Interface**: Beautiful Gradio-based UI for easy interaction
- **Command Line Interface**: Translate files or code snippets from terminal
- **Code Execution**: Run both Python and C code directly in the application
- **Performance Comparison**: Compare execution times between Python and C implementations
- **Detailed Explanations**: Optional explanations of translation choices
- **Example Code**: Built-in examples to get you started
- **Error Handling**: Robust error handling and validation
- **Multiple Input Methods**: Support for files, command-line input, and web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- GCC compiler (for C code execution)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/singh-krishan/ai_projects.git
   cd ai_projects/python-to-c-converter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   **Option A: Environment Variable**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```
   
   **Option B: .env file**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your API key
   ```

### Usage

#### 🌐 Web Interface (Recommended)

Launch the Gradio web interface:

```bash
python main.py --web
```

Then open your browser and go to `http://127.0.0.1:7860`

#### 💻 Command Line Interface

**Translate a Python file:**
```bash
python main.py --file example.py
```

**Translate code from command line:**
```bash
python main.py --code "print('Hello, World!')"
```

**Translate with explanation:**
```bash
python main.py --code "def add(a, b): return a + b" --explanation
```

**Translate and execute C code:**
```bash
python main.py --code "print('Hello')" --execute
```

**Compare performance:**
```bash
python main.py --code "for i in range(1000000): pass" --compare
```

**Save output to file:**
```bash
python main.py --file example.py --output translated.c
```

## 📁 Project Structure

```
python-to-c-converter/
├── main.py              # Main application entry point
├── translator.py         # Core translation logic
├── code_executor.py      # Code execution and performance comparison
├── gradio_app.py        # Gradio web interface
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment variables template
├── example.py           # Sample Python code for testing
├── setup.py             # Automated setup script
├── test_installation.py # Installation validation script
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### API Key Setup

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set it as an environment variable or in a `.env` file
3. The application will automatically detect and use it

## 📝 Examples

### Example 1: Simple Function
**Python:**
```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(f"Result: {result}")
```

**Generated C:**
```c
#include <stdio.h>

int add_numbers(int a, int b) {
    return a + b;
}

int main() {
    int result = add_numbers(5, 3);
    printf("Result: %d\n", result);
    return 0;
}
```

### Example 2: List Operations
**Python:**
```python
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(squared)
```

**Generated C:**
```c
#include <stdio.h>

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int squared[5];
    
    for (int i = 0; i < 5; i++) {
        squared[i] = numbers[i] * numbers[i];
    }
    
    printf("[");
    for (int i = 0; i < 5; i++) {
        printf("%d", squared[i]);
        if (i < 4) printf(", ");
    }
    printf("]\n");
    
    return 0;
}
```

## 🛠️ Advanced Usage

### Custom API Key
```bash
python main.py --api-key "your_key_here" --web
```

### Batch Translation
```bash
# Translate multiple files
for file in *.py; do
    python main.py --file "$file" --output "${file%.py}.c"
done
```

### Integration with Other Tools
```python
from translator import PythonToCTranslator

translator = PythonToCTranslator(api_key="your_key")
c_code = translator.translate("print('Hello, World!')")
print(c_code)
```

## ⚠️ Limitations

- **Complex Python Features**: Some advanced Python features may not translate perfectly
- **Library Dependencies**: Python standard library functions may need manual C equivalents
- **Dynamic Typing**: Python's dynamic typing is converted to appropriate C types
- **Memory Management**: Generated C code includes basic memory management

## 🔍 Troubleshooting

### Common Issues

**"OpenAI API key not provided"**
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Or create a `.env` file with your API key
- Or use the `--api-key` argument

**"Translation failed"**
- Check your internet connection
- Verify your OpenAI API key is valid
- Ensure you have sufficient OpenAI credits

**"Module not found"**
- Run `pip install -r requirements.txt` to install dependencies

**"GCC compiler not found"**
- Install GCC compiler: `brew install gcc` (macOS) or `sudo apt install gcc` (Ubuntu)

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check your internet connection

## 📄 License

This project is open source. Feel free to modify and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4o model
- Gradio team for the excellent web interface framework
- The Python and C programming communities

---

**Happy coding! 🚀**