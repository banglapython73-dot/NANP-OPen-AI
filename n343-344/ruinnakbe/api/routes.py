from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
import datetime
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

# Version will be managed in a better way later
__version__ = "0.7.0"

api_bp = Blueprint('api', __name__)

# --- Helper Functions ---
def get_current_timestamp():
    """Gets the current timestamp and formats it."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")

def get_uploaded_files():
    """Gets a list of uploaded files."""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return [f for f in os.listdir(upload_folder) if f != '.gitkeep']

def process_command(command):
    """Processes a user command (will be replaced by AI agent logic)."""
    if command.lower() == 'list files':
        files = get_uploaded_files()
        return "<br>".join(files) if files else "No files found."
    elif command.lower() == 'clear uploads':
        upload_folder = current_app.config['UPLOAD_FOLDER']
        for f in get_uploaded_files():
            os.remove(os.path.join(upload_folder, f))
        return "All uploaded files have been deleted."
    else:
        # This will be the entry point for our "Manager AI"
        return f"Unknown command: {command}"

# --- Template-serving Routes (for testing, will be replaced by Android app) ---
@api_bp.route('/')
def index():
    """Renders the main page."""
    timestamp = get_current_timestamp()
    files = get_uploaded_files()
    return render_template('index.html', timestamp=timestamp, version=__version__, files=files)

@api_bp.route('/drive_files_page') # Renamed to avoid conflict
def drive_files_page():
    """Renders the Google Drive files page."""
    if 'credentials' not in session:
        return redirect(url_for('api.authorize'))
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    drive = build('drive', 'v3', credentials=credentials)
    results = drive.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return render_template('drive_files.html', files=items)

# --- API Endpoints ---
@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # Handle filename conflicts
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_folder, filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1
        file.save(os.path.join(upload_folder, filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    return jsonify({"error": "File upload failed"}), 500

@api_bp.route('/command', methods=['POST'])
def handle_command():
    command = request.json.get('command') if request.json else request.form.get('command')
    if not command:
        return jsonify({"error": "No command provided"}), 400

    # In the future, this will trigger the Manager AI
    response_text = process_command(command)

    if request.is_json:
        return jsonify({"response": response_text})
    else:
        flash(response_text)
        return redirect(url_for('api.index'))


# --- Google Drive OAuth Routes ---
@api_bp.route('/authorize')
def authorize():
    """Redirects to the Google authorization page."""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        current_app.config['CLIENT_SECRETS_FILE'], scopes=current_app.config['SCOPES'])
    flow.redirect_uri = url_for('api.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@api_bp.route('/oauth2callback')
def oauth2callback():
    """Handles the OAuth2 callback."""
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        current_app.config['CLIENT_SECRETS_FILE'], scopes=current_app.config['SCOPES'], state=state)
    flow.redirect_uri = url_for('api.oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    # Redirect to the page that shows the files, or return a JSON response
    return redirect(url_for('api.drive_files_page'))

@api_bp.route('/drive-files')
def list_drive_files():
    """API endpoint to list files from Google Drive."""
    if 'credentials' not in session:
        return jsonify({"error": "Not authorized. Please go to /api/authorize"}), 401
    try:
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        drive = build('drive', 'v3', credentials=credentials)
        results = drive.files().list(
            pageSize=20, fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
        ).execute()
        items = results.get('files', [])
        return jsonify({"files": items})
    except Exception as e:
        # This can happen if the token is expired or invalid
        return jsonify({"error": str(e)}), 500
