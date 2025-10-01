import subprocess
import tempfile
import os
import sys
import logging
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    """
    Serves the main HTML page for the online Python compiler.
    """
    logging.info("Request received for index.html. Serving static file.")
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        logging.exception("Failed to serve index.html")
        return "Error serving frontend: " + str(e), 500

@app.route('/run', methods=['POST'])
def run_code():
    """
    Handles POST requests to execute Python code on the server.
    Receives code and optional 'stdin' via JSON.
    Runs it in a subprocess and returns output or errors.
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            logging.warning("Received /run request with missing or invalid JSON data.")
            return jsonify({'error': 'Invalid request: Missing "code" field.'}), 400
        
        code = data.get('code', '')
        # Get optional stdin input as a string
        stdin_input = data.get('stdin', '') 

        if not code.strip():
            logging.warning("No executable code provided in /run request.")
            return jsonify({'error': 'No code provided to execute.'}), 400

        temp_filepath = None 
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py', encoding='utf-8') as temp_file:
                temp_file.write(code)
                temp_filepath = temp_file.name
            
            logging.info(f"Executing code from temporary file: {temp_filepath} (Code length: {len(code)} chars, Stdin length: {len(stdin_input)} chars)")
            process = subprocess.run(
                [sys.executable, temp_filepath],
                input=stdin_input, # <-- Pass stdin_input to the subprocess
                capture_output=True,
                text=True,
                timeout=10, 
            )
            output = process.stdout.strip()
            error = process.stderr.strip()
            if error:
                logging.error(f"Code execution error in {temp_filepath}:\n{error}")
                return jsonify({'error': error})
            else:
                logging.info(f"Code from {temp_filepath} executed successfully. Output length: {len(output)} chars.")
                return jsonify({'output': output})
        except subprocess.TimeoutExpired as e:
            logging.warning(f"Code execution timed out for {temp_filepath} after 10 seconds. Partial output/error: Stdout='{e.stdout.strip()}', Stderr='{e.stderr.strip()}'")
            return jsonify({'error': 'Execution timed out after 10 seconds. ' + e.stderr.strip()}), 408 
        except FileNotFoundError:
            logging.error(f"Python interpreter not found at {sys.executable}.")
            return jsonify({'error': 'Server configuration error: Python interpreter not found.'}), 500
        except Exception as e:
            logging.exception(f'An unexpected error occurred during execution setup or cleanup for {temp_filepath}.')
            return jsonify({'error': f'Server error: {str(e)}'}), 500
        finally:
            if temp_filepath and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                logging.debug(f"Temporary file {temp_filepath} deleted successfully.")
            elif temp_filepath:
                logging.warning(f"Attempted to delete {temp_filepath}, but it did not exist.")
    except json.JSONDecodeError:
        logging.warning("Received /run request with malformed JSON.")
        return jsonify({'error': 'Invalid JSON format.'}), 400
    except Exception as e:
        logging.exception("An unhandled error occurred in the /run route handler.")
        return jsonify({'error': f'An unexpected server error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
