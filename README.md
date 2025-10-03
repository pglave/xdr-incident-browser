```markdown
# Cisco XDR Incident Browser

This repository contains a Flask-based web application designed to browse and display incidents from Cisco XDR. It provides a simple interface to authenticate with the Cisco XDR API, load recent incidents, and view detailed information for a selected incident.

## Table of Contents

- [Cisco XDR Incident Browser](#cisco-xdr-incident-browser)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [File Structure](#file-structure)
  - [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
    - [Cisco XDR API Credentials](#cisco-xdr-api-credentials)
    - [Running the Application](#running-the-application)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Security Considerations](#security-considerations)
  - [License](#license)

## Overview

The Cisco XDR Incident Browser is a lightweight web application that demonstrates how to interact with the Cisco XDR API to retrieve and display security incident data. It's built using Python and the Flask web framework, making it easy to deploy and understand.

## Features

*   **Cisco XDR API Authentication**: Securely authenticate using Client ID and Client Password.
*   **Incident Listing**: Load and display a list of recent incidents (default: last 60 days, up to 30 incidents).
*   **Incident Details**: View comprehensive details for any selected incident.
*   **User-Friendly Interface**: A simple web interface for easy navigation and interaction.

## Technologies Used

*   **Python 3.x**: The core programming language.
*   **Flask**: A micro web framework for Python.
*   **Requests**: An elegant and simple HTTP library for Python, used for API calls.
*   **Cisco XDR API**: The backend for incident data.

## File Structure

*   `xdr-incident-browser.py`: The main Flask application file. It defines the web routes, handles user requests, and orchestrates calls to the `ciscoxdr.py` module.
*   `ciscoxdr.py`: A utility module containing functions to interact with the Cisco XDR API, including authentication, loading incidents, and fetching incident details. It also includes helper functions for date formatting.
*   `templates/index.html`: The HTML template for the web application's user interface.

## Setup and Installation

Follow these steps to get the Cisco XDR Incident Browser up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/xdr-incident-browser.git
cd xdr-incident-browser
```

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install Flask requests
```

### Cisco XDR API Credentials

To use this application, you will need a Client ID and Client Password for your Cisco XDR API integration. These credentials will be entered directly into the web application's authentication form.

### Running the Application

To start the Flask development server, run the `xdr-incident-browser.py` file:

```bash
python xdr-incident-browser.py
```

You should see output similar to this:

```
 * Serving Flask app 'xdr-incident-browser'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

1.  **Access the Application**: Open `http://127.0.0.1:5000` in your web browser.
2.  **Authenticate**: On the main page, you will find fields to enter your Cisco XDR **Client ID** and **Client Password**. Click "Authenticate" to obtain an access token.
3.  **Load Incidents**: Once authenticated, click the "Load Incidents" button. The application will fetch and display a list of recent incidents.
4.  **View Incident Details**: Click on any incident in the list to view its detailed information.

## Configuration

The `ciscoxdr.py` file contains some configurable parameters:

*   **`REGION`**: Specifies the Cisco XDR region (e.g., `'EU'`, `'US'`). This determines the API endpoints used.
    ```python
    REGION = 'EU' # Change to 'US' or other relevant region if needed
    ```
*   **`INCIDENT_N_LIMIT`**: (in `xdr-incident-browser.py`) The maximum number of incidents to retrieve.
*   **`INCIDENT_DAYS_AGO`**: (in `xdr-incident-browser.py`) The number of days back from today to search for incidents.

## Security Considerations

*   **`app.secret_key`**: In `xdr-incident-browser.py`, the `app.secret_key` is set to `'dev_xdr_incident_browser_key'`. **For any production deployment, you MUST change this to a strong, random, and securely stored key.**
*   **Production Deployment**: The Flask development server (`app.run(debug=True)`) is not suitable for production environments. For production, use a robust WSGI server like Gunicorn or uWSGI.
*   **API Credentials**: Ensure that your Cisco XDR API Client ID and Client Password are kept confidential and are not exposed in client-side code or public repositories.

## License

This project is open-source and available under the [MIT License](LICENSE).
```  
 
