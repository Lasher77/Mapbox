
# Mapbox

This repository contains scripts and data for working with Mapbox-related geographic information.

## License

This project is licensed under the [MIT License](LICENSE).
=======

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
=======
# Mapbox


## Installation

Use `pip` to install the required Python packages:

```bash
pip install -r requirements.txt
```
=======

## Mapbox Token Setup

The frontend reads the Mapbox access token from a `config.js` file located in the project root. This file is ignored by git so that your token is not committed.

Create the file by copying `config.example.js` or by using the provided script:

# Option 1: copy the example and edit
cp config.example.js config.js
# then replace <YOUR_MAPBOX_TOKEN> with your token

# Option 2: generate from environment variable
MAPBOX_TOKEN=<your_token> node generate-config.js

After `config.js` is created, start the local server with:

python Server.py

=======
## Environment Variables

The backend connects to Salesforce and expects the credentials to be
available through environment variables:

- `SALESFORCE_USERNAME`
- `SALESFORCE_PASSWORD`
- `SALESFORCE_SECURITY_TOKEN`

You can create a `.env` file based on `.env.example` and load it before
running the API.




