# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

### 3. Open Your Browser
- Server-Side: http://127.0.0.1:5001/
- Client-Side: http://127.0.0.1:5001/test.html

## 🎯 Try These Features

### Code Snippets
1. Select a snippet from the dropdown (e.g., "Hello World")
2. Click "Load" to insert it into the editor
3. Click "Run Code" to execute

### Theme Switching
- Click "🌙 Dark Mode" to toggle between light and dark themes
- Use the "Editor Theme" dropdown to change syntax highlighting

### Code Formatting
1. Write some messy Python code
2. Click "✨ Format Code"
3. Watch your code get automatically formatted

### Docker Sandboxing (Optional)
1. Build the Docker image: `docker build -t python-sandbox .`
2. Check "Use Docker Sandbox" before running code
3. Enjoy enhanced security with isolated execution

### Client-Side with Pyodide
1. Open http://127.0.0.1:5001/test.html
2. Install packages like matplotlib: enter "matplotlib" and click "📦 Install"
3. Try the matplotlib snippet to see plot rendering

## 📝 Example Code

### Hello World
```python
print("Hello, World!")
```

### With Input
```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```

### List Comprehension
```python
squares = [x**2 for x in range(10)]
print(squares)
```

### Matplotlib Plot (Client-Side Only)
```python
import matplotlib.pyplot as plt
import io
import base64

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Simple Plot')
plt.grid(True)

buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
import base64
img_str = base64.b64encode(buf.read()).decode()
print(f"IMAGE:{img_str}")
plt.close()
```

## 🔧 Configuration

Edit these values in `app.py` to adjust limits:
```python
MAX_EXECUTION_TIME = 30  # seconds
MAX_MEMORY_MB = 512      # MB
MAX_CPU_PERCENT = 80     # percentage
```

## 🐛 Troubleshooting

### Port Already in Use
Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change 5001 to another port
```

### Docker Not Available
The compiler works without Docker! Just don't check the "Use Docker Sandbox" option.

### CDN Resources Blocked
The UI uses CDN resources (CodeMirror, Tailwind). If blocked by your network, download them locally.

## 🧪 Run Tests
```bash
python test_features.py
```

## 📚 Learn More
See [README.md](README.md) for comprehensive documentation.
