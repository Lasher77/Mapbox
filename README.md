# Mapbox Demo

This repository contains a small Mapbox demo showing German regions with data retrieved from Salesforce. The map now also shows which employees are active in each county based on records from the custom object `Zuordnung_BV_auf_Landkreis__c`. In addition it displays how many companies exist in each district using data from `Potenziale_Lankreise__c`.

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

## Database

The backend stores county assignments in a local SQLite file named
`landkreis_assignments.db`. The file is created automatically the first
time you start `backend/salesforce_api.py` and requires no additional
setup. There are currently no environment variables to change the
database location or name.

## Running the app

1. Start the local HTTP server that serves the static files and GeoJSON:
   ```bash
   python Server.py
   ```
2. In a separate terminal start the Flask backend that connects to Salesforce.
   It now listens on all interfaces on port **5001** so it can be reached from other machines:
   ```bash
   python backend/salesforce_api.py
   ```
3. Open [http://localhost:8000/index.html](http://localhost:8000/index.html) in your browser to view the map.
   To access the map from another computer on the same network, replace
   `localhost` with the IP address of the machine running the server,
   e.g. `http://192.168.0.10:8000/index.html`.
4. The backend exposes `/mitarbeiter_by_landkreis` which the map uses to display the employees active in each county when hovering over a district.
5. The endpoint `/unternehmen_by_landkreis` provides the total number of companies per district, which is also shown in the hover popup.
6. Endpoints handling county assignments:
   - `POST /assignment` stores an assignment record.
   - `GET /assignment/<rs>` retrieves the stored data for a county.
   - `GET /assignments` returns a list of all saved county numbers.
7. Use the dropdown "Ansicht" to switch between **Ist** and **Soll**.
   In **Soll** view, clicking a county opens an info box where you can edit
   the economic region and FKT contacts. The assignments are saved in the
   SQLite database. The checkbox "nach Mitarbeitern" toggles coloring of
   counties based on the number of assigned employees.
