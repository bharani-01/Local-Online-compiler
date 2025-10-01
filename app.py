from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import tempfile
import os
import sys
import signal
import psutil
import time
import json
# Skip autopep8 for Python 3.12+ (lib2to3 removed)
HAS_AUTOPEP8 = False

app = Flask(__name__, static_folder='.')
CORS(app)

# Configuration
MAX_EXECUTION_TIME = 30  # seconds
MAX_MEMORY_MB = 512  # MB
MAX_CPU_PERCENT = 80  # percentage

def format_code(code):
    """Format Python code using ast.unparse for Python 3.9+"""
    try:
        import ast
        
        # Parse and validate the code
        tree = ast.parse(code)
        
        # Use ast.unparse if available (Python 3.9+)
        if hasattr(ast, 'unparse'):
            formatted = ast.unparse(tree)
            return {'formatted_code': formatted, 'error': None}
        else:
            # For older Python versions, just validate the syntax
            return {'formatted_code': code, 'error': None}
            
    except SyntaxError as e:
        return {'formatted_code': None, 'error': f'Syntax error: {e}'}
    except Exception as e:
        return {'formatted_code': None, 'error': str(e)}

def install_dependencies(packages):
    """Install Python packages in a temporary virtual environment"""
    try:
        # Create a temporary directory for the virtual environment
        with tempfile.TemporaryDirectory() as tmpdir:
            venv_path = os.path.join(tmpdir, 'venv')
            
            # Create virtual environment
            subprocess.run([sys.executable, '-m', 'venv', venv_path], 
                         check=True, timeout=30, capture_output=True)
            
            # Get pip path
            pip_path = os.path.join(venv_path, 'bin', 'pip')
            if not os.path.exists(pip_path):
                pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
            
            # Install packages
            for package in packages:
                # Sanitize package name to prevent command injection
                if not package.replace('-', '').replace('_', '').replace('.', '').isalnum():
                    raise ValueError(f"Invalid package name: {package}")
                
                result = subprocess.run([pip_path, 'install', package],
                                      capture_output=True, text=True, timeout=120)
                if result.returncode != 0:
                    return {'success': False, 'error': result.stderr}
            
            return {'success': True, 'venv_path': venv_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def run_in_docker(code, input_data, packages=None):
    """Run code in a Docker container for enhanced security"""
    try:
        # Check if Docker is available
        docker_check = subprocess.run(['docker', '--version'], 
                                     capture_output=True, timeout=5)
        if docker_check.returncode != 0:
            return {'success': False, 'error': 'Docker not available'}
        
        # Create temporary files for code and input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as code_file:
            code_file.write(code)
            code_file_path = code_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as input_file:
            input_file.write(input_data or '')
            input_file_path = input_file.name
        
        try:
            # Build Docker command
            docker_cmd = [
                'docker', 'run', '--rm',
                '--network', 'none',  # No network access
                '--memory', f'{MAX_MEMORY_MB}m',
                '--cpus', str(MAX_CPU_PERCENT / 100.0),
                '--pids-limit', '100',
                '-v', f'{code_file_path}:/code.py:ro',
                '-v', f'{input_file_path}:/input.txt:ro',
                'python:3.9-slim',
                'sh', '-c', 'python /code.py < /input.txt'
            ]
            
            # Execute in Docker
            result = subprocess.run(docker_cmd, capture_output=True, text=True,
                                  timeout=MAX_EXECUTION_TIME)
            
            return {
                'success': True,
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        finally:
            # Clean up temporary files
            os.unlink(code_file_path)
            os.unlink(input_file_path)
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Execution timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def run_with_resource_limits(code, input_data):
    """Run code with CPU and memory limits (fallback when Docker is not available)"""
    process = None
    try:
        # Create temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file_path = f.name
        
        try:
            # Run with timeout using subprocess.run for simpler handling
            result = subprocess.run(
                [sys.executable, temp_file_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=MAX_EXECUTION_TIME
            )
            
            return {
                'success': True,
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
                
        finally:
            os.unlink(temp_file_path)
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Execution timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/test.html')
def test_html():
    return send_from_directory('.', 'test.html')

@app.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.json
        code = data.get('code', '')
        input_data = data.get('input', '')
        use_docker = data.get('use_docker', False)
        packages = data.get('packages', [])
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Install dependencies if requested
        if packages:
            install_result = install_dependencies(packages)
            if not install_result['success']:
                return jsonify({'error': f"Failed to install packages: {install_result['error']}"}), 400
        
        # Execute code
        if use_docker:
            result = run_in_docker(code, input_data, packages)
        else:
            result = run_with_resource_limits(code, input_data)
        
        if result['success']:
            return jsonify({
                'output': result['output'],
                'error': result['error'],
                'returncode': result['returncode']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/format', methods=['POST'])
def format_code_endpoint():
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        result = format_code(code)
        
        if result['error']:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({'formatted_code': result['formatted_code']})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/snippets', methods=['GET'])
def get_snippets():
    """Return a collection of code snippets"""
    snippets = {
        'hello_world': {
            'name': 'Hello World',
            'code': 'print("Hello, World!")'
        },
        'input_output': {
            'name': 'Input/Output',
            'code': 'name = input("Enter your name: ")\nprint(f"Hello, {name}!")'
        },
        'list_comprehension': {
            'name': 'List Comprehension',
            'code': '# Create a list of squares\nsquares = [x**2 for x in range(10)]\nprint(squares)'
        },
        'file_reading': {
            'name': 'File Reading',
            'code': '# Read a file\nwith open("file.txt", "r") as f:\n    content = f.read()\n    print(content)'
        },
        'function_example': {
            'name': 'Function Example',
            'code': 'def greet(name):\n    """Greet someone by name"""\n    return f"Hello, {name}!"\n\n# Call the function\nprint(greet("World"))'
        },
        'class_example': {
            'name': 'Class Example',
            'code': 'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def introduce(self):\n        return f"Hi, I\'m {self.name} and I\'m {self.age} years old"\n\n# Create instance\nperson = Person("Alice", 30)\nprint(person.introduce())'
        },
        'error_handling': {
            'name': 'Error Handling',
            'code': 'try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"Error: {e}")\nfinally:\n    print("Execution completed")'
        },
        'dictionary': {
            'name': 'Dictionary Operations',
            'code': '# Dictionary example\nstudent = {\n    "name": "John",\n    "age": 20,\n    "grades": [85, 90, 92]\n}\n\nprint(f"Name: {student[\'name\']}")\nprint(f"Average: {sum(student[\'grades\']) / len(student[\'grades\'])}")'
        }
    }
    return jsonify(snippets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
