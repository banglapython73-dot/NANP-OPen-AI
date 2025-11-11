from flask import Flask, request, jsonify
# Import the core AI logic from our services package
from services.ai_core import generate_response

# Initialize the Flask application
app = Flask(__name__)

# --- Root Endpoint ---
@app.route('/', methods=['GET'])
def index():
    """
    A simple endpoint to confirm that the server is running.
    """
    return jsonify({"status": "success", "message": "Welcome to the Integrated Intelligence Platform API!"})

# --- Main AI Generation Endpoint ---
@app.route('/api/generate', methods=['POST'])
def generate():
    """
    The primary endpoint that connects to our AI Core.
    """
    # Get the user's query from the request
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"status": "error", "message": "Missing 'prompt' in request body"}), 400

    prompt = data.get('prompt')
    # Get mode and custom API key from the request, with defaults
    mode = data.get('mode', 'powerful') # Default to "powerful" if not provided
    custom_api_key = data.get('custom_api_key', None)

    # Call our AI Core with all parameters
    response_text, model_used, diagnostic_report = generate_response(
        prompt=prompt,
        mode=mode,
        custom_api_key=custom_api_key
    )

    # Return the structured response to the client
    return jsonify({
        "status": "success",
        "response": response_text,
        "model_used": model_used,
        "diagnostic_report": diagnostic_report
    })

# --- Main execution block ---
if __name__ == '__main__':
    # Runs the Flask server on port 5000.
    # Note: For production, 'debug=True' should be turned off.
    app.run(host='0.0.0.0', port=5000, debug=True)
