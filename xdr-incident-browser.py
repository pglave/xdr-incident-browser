from flask import Flask, render_template, request, jsonify, session
import ciscoxdr

INCIDENT_N_LIMIT = 30
INCIDENT_DAYS_AGO = 60

app = Flask(__name__)
app.secret_key = 'dev_xdr_incident_browser_key' # If in production, change this to a strong, random key

def delete_until_last_slash(input_string):
    """
    Deletes the initial part of a string, including the last occurrence of a slash (/) character.

    Args:
        input_string (str): The string to modify.

    Returns:
        str: The modified string, or the original string if no slash is found.
    """
    last_slash_index = input_string.rfind('/')
    if last_slash_index != -1:
        # Slice the string from the character immediately after the last slash
        return input_string[last_slash_index + 1:]
    else:
        # If no slash is found, return the original string
        return input_string



@app.route('/')
def index():
    """
    Renders the main page of the XDR Incident Browser.
    """
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """
    Handles authentication requests.
    Expects JSON payload with 'client_id' and 'client_password'.
    Puts the token into "session" to make them persistent.
    Returns a JSON response indicating success or failure.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.get_json()
    client_id = data.get('client_id')
    client_password = data.get('client_password')

    # --- Authentication Logic ---
    result_data = ciscoxdr.authenticate(client_id=client_id, client_password=client_password)
    result = result_data['status_code']
    if (result == 200):
        session['access_token'] = result_data['access_token']
        session['access_token_scope'] = result_data['scope']
        session['access_token_expires_in'] = result_data['expires_in']
        return jsonify({"success": True, "message": "Successfully authenticated!"}), 200
    else:
        return jsonify({"success": False, "message": f"Return code: {result}"}), result
    # --- End Authentication Logic ---

@app.route('/load_incidents', methods=['POST'])
def load_incidents():
    """
    Loads the incidents.
    Returns a JSON response indicating success or failure.
    Incident data will be contained in an array inside JSON returned data.
    """
    result_data = ciscoxdr.load_incidents(token=session['access_token'], 
    	limit=INCIDENT_N_LIMIT, days_ago=INCIDENT_DAYS_AGO)
    result = result_data['status_code']
    if (result == 200):
        return jsonify({"success": True,
            "incident_data": result_data['incident_data'],
            "message": "Incidents successfully loaded."}), 200
    else:
        return jsonify({"success": False, "message": f"Return code: {result}"}), result



@app.route('/select_incident', methods=['POST'])
def select_incident():
    """
    Get details on an incident.
    Returns a JSON response indicating success or failure.
    Incident data will be put into JSON returned data.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.get_json()
    incident_id_url = data.get('incident_id')

    # --- XDR Logic ---
    result_data = ciscoxdr.load_incident_details(token=session['access_token'], 
    	inc_id=delete_until_last_slash(incident_id_url))
    result = result_data['status_code']
    if (result == 200):
        return jsonify({"success": True,
            "incident_details": result_data['incident_details'],
            "message": "Incident details successfully loaded."}), 200
    else:
        return jsonify({"success": False, "message": f"Return code: {result}"}), result
    # --- End XDR Logic ---

if __name__ == '__main__':
    # Run the Flask application
    # In a production environment, use a production-ready WSGI server like Gunicorn or uWSGI.
    app.run(debug=True)

