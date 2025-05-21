# Mapbox Demo

This repository contains a small Mapbox demo showing German regions with data
from Salesforce.

## Prerequisites

1. Python 3
2. Install dependencies:
   ```bash
   pip install flask flask-cors simple-salesforce
   ```
3. Set the Salesforce credentials as environment variables:
   ```bash
   export SF_USERNAME=your_username
   export SF_PASSWORD=your_password
   export SF_SECURITY_TOKEN=your_token
   ```
4. Ensure `Landkreise.geojson` and `Wirtschaftsregionen_cleaned.geojson` are in
   the project directory. If they are hosted elsewhere download them first.

## Running the app

1. Start the local HTTP server which serves the static files and GeoJSON:
   ```bash
   python Server.py
   ```
2. In a separate terminal start the Flask backend which connects to
   Salesforce:
   ```bash
   python backend/salesforce_api.py
   ```
3. Open your browser at [http://localhost:8000/index.html](http://localhost:8000/index.html)
   to view the map. When hovering over a region the number of accounts is
   displayed.
