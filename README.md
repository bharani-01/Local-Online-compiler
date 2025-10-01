# Online Python Compiler

This project provides a web-based environment for writing and executing Python code, demonstrating two distinct architectures: **Server-Side Execution** (using Flask) and **Client-Side Execution** (using Pyodide/WebAssembly).

## 🚀 Key Features

### Dual Architecture
- **Server-Side Execution**: Robust execution with Docker sandboxing and resource limits
- **Client-Side Execution**: Fast, instant execution using Pyodide (CPython in WebAssembly)

### Editor & UI Improvements
- ✨ **Code Snippets**: Collection of ready-to-use Python code templates for common tasks
- 🎨 **Theme Switching**: Dark mode and multiple editor themes (Monokai, Dracula, Material, Eclipse)
- 🔧 **Automatic Formatting**: Code formatter using autopep8 for clean indentation and style
- 💾 **Persistence**: Code and input saved to browser's local storage
- 🖥️ **Syntax Highlighting**: Integrated CodeMirror editor for professional coding experience

### Server-Side Enhancements
- 🐳 **Docker Sandboxing**: Enhanced security with isolated container execution
- 📦 **Dependency Management**: Install Python packages on-demand (experimental)
- ⚡ **Resource Limits**: Fine-grained CPU and memory monitoring
- 🔒 **Security**: Process isolation and resource constraints

### Client-Side Enhancements
- 📦 **Micropip Support**: Install Pyodide-compatible packages (numpy, pandas, matplotlib, etc.)
- 📊 **Plot Rendering**: Display matplotlib plots directly in the browser
- ⚡ **Instant Feedback**: No server required, runs entirely in the browser
- 🎯 **Interactive Input**: Custom stdin handler for input prompts

## 💻 Architecture Overview

### 1. Server-Side Execution (Recommended for heavier tasks)

**Files**: `app.py`, `index.html`

- **Backend**: Python Flask application (`app.py`)
- **Execution**: Frontend sends code and input to `/run` endpoint
- **Sandboxing**: Code executes in Docker containers or with resource limits
- **Features**: 
  - Docker isolation (network disabled, memory/CPU limits)
  - Package installation support
  - Code formatting endpoint
  - Snippets API
  - Resource monitoring (CPU, memory, timeout)

**How to Access**: Run the Flask server (see Getting Started below) and navigate to `http://127.0.0.1:5001/`

### 2. Client-Side Execution (Recommended for instant feedback)

**File**: `test.html`

- **Execution**: Uses Pyodide (CPython compiled to WebAssembly)
- **Runtime**: Python interpreter runs directly in the browser
- **Input**: Custom stdin handler for interactive prompts
- **Features**:
  - Micropip package installation
  - Matplotlib plot rendering
  - Base64-encoded image output
  - No server required

**How to Access**: Simply open `test.html` in your web browser

## ⚙️ Getting Started (Server-Side)

### Prerequisites
- Python 3.x installed
- Docker (optional, for enhanced sandboxing)

### 1. Setup Environment

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Build Docker Image (Optional)

For Docker-based sandboxing:

```bash
docker build -t python-sandbox .
```

### 4. Run the Server

Start the Flask application:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5001/`

### 5. Access the Compiler

- **Server-Side Compiler**: Open `http://127.0.0.1:5001/`
- **Client-Side Compiler**: Open `http://127.0.0.1:5001/test.html` or open `test.html` directly in browser

## 🎯 Features in Detail

### Code Snippets
Pre-loaded templates for:
- Hello World
- Input/Output handling
- List comprehensions
- Functions and Classes
- Dictionary operations
- Error handling
- File operations

### Theme Switching
- **UI Theme**: Toggle between light and dark mode
- **Editor Themes**: Choose from Default, Monokai, Dracula, Material, and Eclipse

### Auto-Formatting
Server-side endpoint uses autopep8 to:
- Fix indentation
- Normalize spacing
- Apply PEP 8 style guidelines

### Docker Sandboxing
When enabled:
- ✅ Network access disabled
- ✅ Memory limit: 512MB (configurable)
- ✅ CPU limit: 80% (configurable)
- ✅ Process limit: 100
- ✅ Read-only code mounting
- ✅ Automatic cleanup

### Resource Limits (Non-Docker)
Fallback execution with:
- ⏱️ Execution timeout: 30 seconds
- 💾 Memory limit: 512MB
- 🔄 Process monitoring

### Micropip Package Installation
Client-side support for installing:
- numpy
- pandas
- matplotlib
- scipy
- scikit-learn
- And more Pyodide-compatible packages

### Plot Rendering
Matplotlib plots automatically displayed:
- Saves figure to base64
- Renders in dedicated plot area
- Supports multiple plots

## 🔒 Security Considerations

### Server-Side
- Docker isolation prevents filesystem access
- Network disabled in containers
- Resource limits prevent DoS
- Package name sanitization
- Process monitoring and termination

### Client-Side
- Runs in browser sandbox
- No server access required
- Limited by browser security model

## 🛠️ Configuration

Edit `app.py` to adjust limits:

```python
MAX_EXECUTION_TIME = 30  # seconds
MAX_MEMORY_MB = 512      # MB
MAX_CPU_PERCENT = 80     # percentage
```

## 📝 API Endpoints

### POST `/run`
Execute Python code
```json
{
  "code": "print('hello')",
  "input": "optional input",
  "use_docker": false,
  "packages": ["numpy"]
}
```

### POST `/format`
Format Python code
```json
{
  "code": "def hello( ):\n  print('world')"
}
```

### GET `/snippets`
Get available code snippets

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Flask**: Web framework
- **Pyodide**: Python in WebAssembly
- **CodeMirror**: Code editor
- **Tailwind CSS**: UI styling
- **Docker**: Containerization
