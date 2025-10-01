# Feature Documentation

## 🎨 Code Snippets

### Available Snippets (Server-Side)
1. **Hello World** - Basic print statement
2. **Input/Output** - Interactive user input
3. **List Comprehension** - Python list comprehension example
4. **Function Example** - Function definition and usage
5. **Class Example** - Object-oriented programming
6. **Error Handling** - Try/except blocks
7. **Dictionary Operations** - Working with dictionaries
8. **File Reading** - File I/O operations

### How to Use
1. Select snippet from dropdown menu
2. Click "Load" button
3. Snippet code appears in editor
4. Modify as needed
5. Click "Run Code" to execute

## 🎨 Theme System

### UI Themes
- **Light Mode** (default) - Clean, bright interface
- **Dark Mode** - Easy on the eyes for long coding sessions

Toggle: Click the "🌙 Dark Mode" button in header

### Editor Themes
Choose from 5 professional themes:
- **Default** - Classic light theme
- **Monokai** - Popular dark theme with vibrant colors
- **Dracula** - Modern dark theme
- **Material** - Google's Material Design theme
- **Eclipse** - IDE-inspired theme

Settings persist across browser sessions.

## ✨ Code Formatting

### Auto-Format Feature
Automatically formats your Python code to follow consistent style guidelines.

**Uses:** Python's built-in AST (Abstract Syntax Tree) module

**What it does:**
- Normalizes spacing around operators
- Fixes indentation
- Ensures consistent style

**Example:**
```python
# Before formatting
x=1+2
y  =  3+4
print(  x,y  )

# After formatting
x = 1 + 2
y = 3 + 4
print(x, y)
```

**How to use:**
1. Write or paste code
2. Click "✨ Format Code" button
3. Code is automatically reformatted

## 🐳 Docker Sandboxing

### What is Docker Sandboxing?
Runs your code in an isolated container for maximum security.

### Security Features
- ✅ **No Network Access** - Container cannot access internet
- ✅ **Memory Limit** - Maximum 512MB RAM (configurable)
- ✅ **CPU Limit** - Maximum 80% CPU usage (configurable)
- ✅ **Process Limit** - Maximum 100 processes
- ✅ **Non-Root User** - Code runs as unprivileged user
- ✅ **Read-Only Code** - Cannot modify host files

### How to Enable
1. Build Docker image: `docker build -t python-sandbox .`
2. Check "Use Docker Sandbox" checkbox
3. Run your code normally

### When to Use Docker
- Running untrusted code
- Need extra security
- Want resource isolation
- Production environments

### Fallback Mode
If Docker is not available, code runs with:
- 30-second timeout
- Memory monitoring
- Process isolation

## 📦 Package Installation

### Server-Side (Experimental)
Install Python packages before execution.

**Features:**
- Package name sanitization
- Virtual environment isolation
- Timeout protection

**Example:**
```
Input: numpy, pandas
```

**Note:** This feature is experimental and may slow down execution.

### Client-Side (Pyodide/micropip)
Install packages directly in the browser!

**Supported packages:**
- numpy
- pandas
- matplotlib
- scipy
- scikit-learn
- And many more pure-Python packages

**How to install:**
1. Enter package name (e.g., "matplotlib")
2. Click "📦 Install" button
3. Wait for installation
4. Use in your code

**Example:**
```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())
```

## 📊 Plot Rendering (Client-Side)

### Matplotlib in Browser
Render matplotlib plots directly in the output area!

**How it works:**
1. Create plot with matplotlib
2. Save to BytesIO buffer
3. Encode as base64
4. Print with "IMAGE:" prefix
5. Plot appears automatically

**Example Code:**
```python
import matplotlib.pyplot as plt
import io
import base64

# Create plot
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Simple Plot')
plt.grid(True)

# Save and display
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img_str = base64.b64encode(buf.read()).decode()
print(f"IMAGE:{img_str}")
plt.close()
```

**Result:** Plot appears below output area

## 💾 Persistence

### What is Saved
- Python code
- Input text
- Editor theme preference
- Dark mode preference

### Storage
Uses browser's LocalStorage API

### Privacy
All data stored locally in your browser - nothing sent to server except during execution.

## ⚡ Performance

### Server-Side
- Execution: Fast for most code
- First run: ~100-500ms
- With Docker: +200-500ms overhead
- With packages: Slower (install time)

### Client-Side (Pyodide)
- Initial load: 3-5 seconds (downloads Python runtime)
- Subsequent runs: Very fast
- Package install: 1-30 seconds depending on package
- No server needed!

## 🔒 Security Best Practices

### For Server Deployment
1. ✅ Enable Docker sandboxing
2. ✅ Use HTTPS
3. ✅ Set reasonable resource limits
4. ✅ Monitor for abuse
5. ✅ Consider rate limiting
6. ✅ Disable package installation in production

### For Users
1. Don't run untrusted code without Docker
2. Be careful with file operations
3. Review code before execution
4. Use client-side for sensitive data

## 🐛 Error Handling

### Types of Errors

**Syntax Errors:**
```python
print("missing closing quote)
# Shows: SyntaxError with line number
```

**Runtime Errors:**
```python
print(undefined_variable)
# Shows: NameError with traceback
```

**Timeout:**
```python
while True:
    pass
# Shows: "Execution timed out"
```

**Memory Limit:**
```python
big_list = [0] * 10000000000
# Shows: "Memory limit exceeded"
```

## 📱 Browser Compatibility

### Server-Side (index.html)
Works in all modern browsers:
- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### Client-Side (test.html)
Requires WebAssembly support:
- ✅ Chrome 57+
- ✅ Firefox 52+
- ✅ Safari 11+
- ✅ Edge 16+

## 🎯 Use Cases

### Education
- Learn Python syntax
- Practice algorithms
- Test code snippets
- Demonstrate concepts

### Development
- Quick prototyping
- Test ideas
- Debug issues
- Share code examples

### Data Science
- Explore data with pandas
- Create visualizations
- Test ML algorithms
- Interactive analysis

## 💡 Tips & Tricks

### Tip 1: Keyboard Shortcuts
Most CodeMirror shortcuts work:
- `Ctrl+/` - Comment line
- `Ctrl+D` - Delete line
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo

### Tip 2: Multiple Inputs
For multiple input() calls, separate with newlines:
```
Input (stdin):
Alice
25
Python
```

### Tip 3: Clear Output
Output accumulates - use "🗑 Clear" to reset.

### Tip 4: Theme Persistence
Your theme preference is saved automatically.

### Tip 5: Code Templates
Use snippets as starting points - modify them for your needs.

### Tip 6: Client-Side for Privacy
Use test.html (Pyodide) when working with sensitive data - nothing leaves your browser.

### Tip 7: Format Before Sharing
Always format code before sharing - makes it more readable.

## 🔄 Switching Between Modes

### Server-Side → Client-Side
Click "Switch to Client-Side" button

**Advantages:**
- Instant execution
- No server load
- Works offline
- Package installation
- Plot rendering

### Client-Side → Server-Side
Click "Switch to Server-Side" button

**Advantages:**
- More packages available
- Better performance for heavy tasks
- Docker sandboxing
- File operations
- More memory

## 📊 Resource Limits

### Default Limits (Configurable)

| Resource | Server-Side | Client-Side |
|----------|-------------|-------------|
| Timeout | 30 seconds | Browser limit |
| Memory | 512 MB | Browser limit |
| CPU | 80% | 100% |
| Processes | 100 (Docker) | N/A |
| Network | Disabled (Docker) | Limited by CORS |

### Adjusting Limits
Edit `app.py`:
```python
MAX_EXECUTION_TIME = 30  # seconds
MAX_MEMORY_MB = 512      # MB
MAX_CPU_PERCENT = 80     # percentage
```

## 🌐 API Usage

### Execute Code
```bash
curl -X POST http://localhost:5001/run \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello\")",
    "input": "",
    "use_docker": false
  }'
```

### Format Code
```bash
curl -X POST http://localhost:5001/format \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x=1+2"
  }'
```

### Get Snippets
```bash
curl http://localhost:5001/snippets
```

## 🎓 Learning Resources

### Next Steps
1. Try all code snippets
2. Experiment with themes
3. Install packages
4. Create plots
5. Build something cool!

### Documentation
- **README.md** - Overview and setup
- **QUICKSTART.md** - Get started quickly
- **FEATURES.md** - This file
- **Code comments** - Implementation details
