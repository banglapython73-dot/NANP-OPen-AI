from flask import Flask, request, jsonify
# Import the new central controller
from services.main_controller import process_request

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
async def generate():
    """
    The primary endpoint that connects to our AI Core.
    """
    # Get the user's query from the request
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"status": "error", "message": "Missing 'prompt' in request body"}), 400

    prompt = data.get('prompt')
    # Get mode from the request, with a default
    mode = data.get('mode', 'powerful') # Default to "powerful"

    # Placeholder for user preferences which will be expanded later
    # This could include things like preferred data sources (e.g., 'academic_only', 'allow_tor')
    user_preferences = data.get('preferences', {})

    # Call the new central controller
    response_payload, model_used, diagnostic_report = await process_request(
        prompt=prompt,
        mode=mode,
        user_preferences=user_preferences
    )

    # Return the structured response to the client
    return jsonify({
        "status": "success",
        "response": response_payload, # This is now an object with 'text' and 'image_url'
        "model_used": model_used,
        "diagnostic_report": diagnostic_report
    })

# --- Main execution block ---
if __name__ == '__main__':
    # Running without debug mode to prevent path-related restart errors.
    app.run(host='0.0.0.0', port=5000)
