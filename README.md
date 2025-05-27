# Mapbox Demo

This repository contains a small Mapbox demo showing German regions with data retrieved from Salesforce. The map now also shows which employees are active in each county based on records from the custom object `Zuordnung_BV_auf_Landkreis__c`. In addition it displays how many companies exist in each district using data from `Potenziale_Landkreise__c`.

## License

This project is licensed under the [MIT License](LICENSE).

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `config.js` with your Mapbox token. Copy the example and edit it or generate it:
   ```bash
   cp config.example.js config.js
   # replace <YOUR_MAPBOX_TOKEN> in config.js
   # or run
   MAPBOX_TOKEN=<your_token> node generate-config.js
   ```
3. Set the Salesforce credentials as environment variables:
   ```bash
   export SALESFORCE_USERNAME=your_username
   export SALESFORCE_PASSWORD=your_password
   export SALESFORCE_SECURITY_TOKEN=your_token
   ```
   You can create a `.env` file based on `.env.example` and load it before running the API.
4. Ensure `Landkreise.geojson` and `Wirtschaftsregionen_cleaned.geojson` are present in the project directory.

## Running the app

1. Start the local HTTP server that serves the static files and GeoJSON:
   ```bash
   python Server.py
   ```
2. In a separate terminal start the Flask backend that connects to Salesforce:
   ```bash
   python backend/salesforce_api.py
   ```
3. Open [http://localhost:8000/index.html](http://localhost:8000/index.html) in your browser to view the map.
4. The backend exposes `/mitarbeiter_by_landkreis` which the map uses to display the employees active in each county when hovering over a district.
5. The endpoint `/unternehmen_by_landkreis` provides the total number of companies per district, which is also shown in the hover popup.
